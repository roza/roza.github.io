// deps.c — passe 1 : lecture en flux d'un export lean4export 3.1.0 (NDJSON) sur stdin.
// Produit, dans le répertoire OUT (argv[1]) :
//   decls.tsv   : d kind name_id lines_own type_dag value_dag type_root value_root
//   members.tsv : d name_id        (toutes les constantes définies par le nœud d ; blocs inductifs)
//   edges.bin   : pour chaque d : uint32 d, uint32 n, n × uint32 name_id (constantes référencées)
//   names.tsv   : name_id \t nom complet   (noms de déclarations seulement)
//   c1.u32, c2.u32, islet.bits, lets.bin : DAG des expressions (pour la passe 2)
// Compilation : cc -O2 -o deps deps.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

#define NONE 0xFFFFFFFFu
#define CB 0x80000000u
#define CAP (1ull << 31)

static void die(const char *m) { fprintf(stderr, "FATAL: %s\n", m); exit(1); }

/* ---------- mini-DOM JSON ---------- */
typedef struct { char t; long long n; const char *s; int sl; const char *k; int kl; int child, next; } J;
static J *P; static int pn, pcap;
static const char *cur;
static int newj(void) {
  if (pn == pcap) { pcap = pcap ? pcap * 2 : 4096; P = realloc(P, (size_t)pcap * sizeof(J)); if (!P) die("oom"); }
  memset(&P[pn], 0, sizeof(J)); P[pn].child = P[pn].next = -1; return pn++;
}
static void ws(void) { while (*cur == ' ' || *cur == '\t' || *cur == '\r' || *cur == '\n') cur++; }
static void pstr(const char **s, int *l) {
  if (*cur != '"') die("expected string");
  cur++; *s = cur;
  while (*cur != '"') { if (!*cur) die("eol in string"); if (*cur == '\\') cur++; cur++; }
  *l = (int)(cur - *s); cur++;
}
static int pval(void) {
  ws(); int id = newj(); char c = *cur;
  if (c == '{' || c == '[') {
    int isobj = c == '{'; P[id].t = isobj ? 'o' : 'a'; cur++; ws();
    if (*cur == (isobj ? '}' : ']')) { cur++; return id; }
    int last = -1;
    for (;;) {
      const char *k = 0; int kl = 0;
      ws();
      if (isobj) { pstr(&k, &kl); ws(); if (*cur != ':') die("expected :"); cur++; }
      int v = pval(); P[v].k = k; P[v].kl = kl;
      if (last < 0) P[id].child = v; else P[last].next = v;
      last = v; ws();
      if (*cur == ',') { cur++; continue; }
      if (*cur != (isobj ? '}' : ']')) die("expected close");
      cur++; break;
    }
  } else if (c == '"') { P[id].t = 's'; pstr(&P[id].s, &P[id].sl); }
  else if (c == 't') { P[id].t = 'b'; P[id].n = 1; cur += 4; }
  else if (c == 'f') { P[id].t = 'b'; cur += 5; }
  else if (c == 'n') { P[id].t = 'z'; cur += 4; }
  else { char *e; P[id].t = 'n'; P[id].n = strtoll(cur, &e, 10); if (e == cur) die("bad number"); cur = e;
         if (*cur == '.' || *cur == 'e' || *cur == 'E') { strtod(cur - 0, &e); cur = e; } }
  return id;
}
static int get(int o, const char *k) {
  if (o < 0) return -1;
  size_t kl = strlen(k);
  for (int c = P[o].child; c >= 0; c = P[c].next)
    if ((size_t)P[c].kl == kl && memcmp(P[c].k, k, kl) == 0) return c;
  return -1;
}
static long long num(int o) { if (o < 0 || P[o].t != 'n') die("expected number"); return P[o].n; }

/* ---------- noms ---------- */
static uint32_t *NPRE; static uint64_t *NOFF; static uint8_t *NISNUM; static uint64_t ncap;
static char *SP; static uint64_t spn, spcap;
static void name_reserve(uint64_t n) {
  if (n < ncap) return;
  uint64_t nc = ncap ? ncap : 1 << 20; while (nc <= n) nc *= 2;
  NPRE = realloc(NPRE, nc * 4); NOFF = realloc(NOFF, nc * 8); NISNUM = realloc(NISNUM, nc);
  if (!NPRE || !NOFF || !NISNUM) die("oom names");
  memset(NPRE + ncap, 0, (nc - ncap) * 4); memset(NOFF + ncap, 0xff, (nc - ncap) * 8); memset(NISNUM + ncap, 0, nc - ncap);
  ncap = nc;
}
static uint64_t sp_add(const char *s, int l) {
  if (spn + l + 1 > spcap) { while (spn + l + 1 > spcap) spcap = spcap ? spcap * 2 : 1 << 24; SP = realloc(SP, spcap); if (!SP) die("oom sp"); }
  uint64_t o = spn; memcpy(SP + spn, s, l); SP[spn + l] = 0; spn += l + 1; return o;
}
static void name_print(FILE *f, uint32_t n) {
  if (n == 0 || n >= ncap || NOFF[n] == (uint64_t)-1) { if (n) fprintf(f, "?%u", n); return; }
  if (NPRE[n]) { name_print(f, NPRE[n]); fputc('.', f); }
  fputs(SP + NOFF[n], f);
}

/* ---------- expressions ---------- */
static uint32_t *C1, *C2, *AUX; static uint8_t *ISLET, *VIS; static uint64_t nexpr;
static FILE *FLIT, *FLEV;
static uint32_t binfo(int lam) { int b = get(lam, "binderInfo"); if (b < 0) return 0; const char *s = P[b].s; int l = P[b].sl;
  if (l == 8 && !memcmp(s, "implicit", 8)) return 1; if (l == 14 && !memcmp(s, "strictImplicit", 14)) return 2; if (l == 12 && !memcmp(s, "instImplicit", 12)) return 3; return 0; }
#define MKAUX(k, bi, pay) ((uint32_t)(k) | ((uint32_t)(bi) << 4) | ((uint32_t)((pay) > 0x3FFFFFF ? 0x3FFFFFF : (pay)) << 6))

static uint32_t *LK, *LV; static uint64_t lcap = 1 << 16, lcnt;
static void let_put(uint32_t k, uint32_t v) {
  if (2 * (lcnt + 1) > lcap) {
    uint64_t oc = lcap; uint32_t *ok = LK, *ov = LV; lcap *= 2;
    LK = malloc(lcap * 4); LV = malloc(lcap * 4); memset(LK, 0xff, lcap * 4);
    lcnt = 0;
    for (uint64_t i = 0; i < oc; i++) if (ok[i] != NONE) let_put(ok[i], ov[i]);
    free(ok); free(ov);
  }
  uint64_t h = ((uint64_t)k * 0x9E3779B97F4A7C15ull) & (lcap - 1);
  while (LK[h] != NONE) h = (h + 1) & (lcap - 1);
  LK[h] = k; LV[h] = v; lcnt++;
}
static uint32_t let_get(uint32_t k) {
  uint64_t h = ((uint64_t)k * 0x9E3779B97F4A7C15ull) & (lcap - 1);
  while (LK[h] != NONE) { if (LK[h] == k) return LV[h]; h = (h + 1) & (lcap - 1); }
  die("let missing"); return 0;
}
static void *mapfile(const char *dir, const char *fn, uint64_t sz) {
  char p[4096]; snprintf(p, sizeof p, "%s/%s", dir, fn);
  int fd = open(p, O_RDWR | O_CREAT | O_TRUNC, 0644); if (fd < 0) die(p);
  if (ftruncate(fd, (off_t)sz)) die("ftruncate");
  void *m = mmap(0, sz, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0); if (m == MAP_FAILED) die("mmap");
  close(fd); return m;
}

/* ---------- parcours ---------- */
static uint32_t *STK; static uint64_t stn, stcap;
static uint32_t *VL; static uint64_t vln, vlcap;      // nœuds visités (pour effacer le bitmap)
static uint32_t *NST; static uint64_t nstcap; static uint32_t stamp; // tampons sur les noms
static uint32_t *DC; static uint64_t dcn, dccap;       // constantes de la décl courante

static void addconst(uint32_t n) {
  if (n >= nstcap) { uint64_t nc = nstcap ? nstcap : 1 << 20; while (nc <= n) nc *= 2; NST = realloc(NST, nc * 4); memset(NST + nstcap, 0, (nc - nstcap) * 4); nstcap = nc; }
  if (NST[n] == stamp) return;
  NST[n] = stamp;
  if (dcn == dccap) { dccap = dccap ? dccap * 2 : 1024; DC = realloc(DC, dccap * 4); }
  DC[dcn++] = n;
}
static void push(uint32_t v) {
  if (v == NONE) return;
  if (v & CB) { addconst(v & ~CB); return; }
  if (v >= nexpr) die("dangling expr ref");
  if (VIS[v >> 3] & (1 << (v & 7))) return;
  VIS[v >> 3] |= (1 << (v & 7));
  if (vln == vlcap) { vlcap = vlcap ? vlcap * 2 : 1 << 20; VL = realloc(VL, vlcap * 4); }
  VL[vln++] = v;
  if (stn == stcap) { stcap = stcap ? stcap * 2 : 1 << 20; STK = realloc(STK, stcap * 4); }
  STK[stn++] = v;
}
static uint64_t walk(uint32_t root) {     // renvoie le nombre de nouveaux nœuds visités
  uint64_t before = vln;
  push(root);
  while (stn) {
    uint32_t v = STK[--stn];
    push(C1[v]); push(C2[v]);
    if (ISLET[v >> 3] & (1 << (v & 7))) push(let_get(v));
  }
  return vln - before;
}
static void walk_reset(void) {
  for (uint64_t i = 0; i < vln; i++) VIS[VL[i] >> 3] &= ~(1 << (VL[i] & 7));
  vln = 0; dcn = 0; stamp++;
  if (stamp == 0) { memset(NST, 0, nstcap * 4); stamp = 1; }
}

/* ---------- main ---------- */
static FILE *FD, *FM, *FE; static uint64_t ndecl, lines_since;
static uint32_t *DN; static uint64_t dnn, dncap;   // noms de déclarations à résoudre
static void note_name(uint32_t n) { if (dnn == dncap) { dncap = dncap ? dncap * 2 : 1 << 20; DN = realloc(DN, dncap * 4); } DN[dnn++] = n; }
static void member(uint64_t d, uint32_t n, long long troot) { fprintf(FM, "%llu\t%u\t%lld\n", (unsigned long long)d, n, troot); note_name(n); }

static void emit(const char *kind, uint32_t name, uint64_t tdag, uint64_t vdag, long long troot, long long vroot) {
  uint32_t hdr[2] = { (uint32_t)ndecl, (uint32_t)dcn };
  fwrite(hdr, 4, 2, FE); fwrite(DC, 4, dcn, FE);
  fprintf(FD, "%llu\t%s\t%u\t%llu\t%llu\t%llu\t%lld\t%lld\n", (unsigned long long)ndecl, kind, name,
          (unsigned long long)lines_since, (unsigned long long)tdag, (unsigned long long)vdag, troot, vroot);
  member(ndecl, name, troot);
  ndecl++; lines_since = 0; walk_reset();
}

int main(int argc, char **argv) {
  if (argc < 2) die("usage: deps OUTDIR < export.ndjson");
  const char *out = argv[1]; char p[4096];
  C1 = mapfile(out, "c1.u32", CAP * 4); C2 = mapfile(out, "c2.u32", CAP * 4); AUX = mapfile(out, "aux.u32", CAP * 4);
  snprintf(p, sizeof p, "%s/lits.tsv", out); FLIT = fopen(p, "w"); snprintf(p, sizeof p, "%s/levels.tsv", out); FLEV = fopen(p, "w");
  ISLET = mapfile(out, "islet.bits", CAP / 8);
  VIS = calloc(CAP / 8, 1); LK = malloc(lcap * 4); LV = malloc(lcap * 4); memset(LK, 0xff, lcap * 4);
  stamp = 1;
  snprintf(p, sizeof p, "%s/decls.tsv", out); FD = fopen(p, "w");
  snprintf(p, sizeof p, "%s/members.tsv", out); FM = fopen(p, "w");
  snprintf(p, sizeof p, "%s/edges.bin", out); FE = fopen(p, "wb");
  if (!FD || !FM || !FE) die("open out");
  name_reserve(1); NOFF[0] = sp_add("", 0);

  char *line = 0; size_t lcap_ = 0; ssize_t len; uint64_t ln = 0, nonseq = 0;
  while ((len = getline(&line, &lcap_, stdin)) > 0) {
    ln++;
    if ((ln & ((1 << 24) - 1)) == 0) fprintf(stderr, "lines %lluM exprs %lluM decls %llu\n", (unsigned long long)(ln >> 20), (unsigned long long)(nexpr >> 20), (unsigned long long)ndecl);
    pn = 0; cur = line; int r = pval(); if (P[r].t != 'o') die("not object");
    int x;
    if ((x = get(r, "ie")) >= 0) {
      uint64_t ie = (uint64_t)num(x); if (ie >= CAP) die("ie too large");
      if (ie != nexpr) nonseq++;
      if (ie >= nexpr) nexpr = ie + 1;
      uint32_t a = NONE, b = NONE, aux = 15; int y;
      lines_since++;
      if ((y = get(r, "app")) >= 0) { a = (uint32_t)num(get(y, "fn")); b = (uint32_t)num(get(y, "arg")); aux = 3; }
      else if ((y = get(r, "lam")) >= 0 || (y = get(r, "forallE")) >= 0) { a = (uint32_t)num(get(y, "type")); b = (uint32_t)num(get(y, "body"));
        aux = MKAUX(get(r, "lam") >= 0 ? 4 : 5, binfo(y), (uint64_t)num(get(y, "name"))); }
      else if ((y = get(r, "letE")) >= 0) { a = (uint32_t)num(get(y, "value")); b = (uint32_t)num(get(y, "body")); let_put((uint32_t)ie, (uint32_t)num(get(y, "type"))); ISLET[ie >> 3] |= 1 << (ie & 7);
        aux = MKAUX(6, 0, (uint64_t)num(get(y, "name"))); }
      else if ((y = get(r, "const")) >= 0) { a = CB | (uint32_t)num(get(y, "name")); aux = 2; }
      else if ((y = get(r, "proj")) >= 0) { a = (uint32_t)num(get(y, "struct")); b = CB | (uint32_t)num(get(y, "typeName")); aux = MKAUX(7, 0, (uint64_t)num(get(y, "idx"))); }
      else if ((y = get(r, "mdata")) >= 0) { a = (uint32_t)num(get(y, "expr")); aux = 8; }
      else if ((y = get(r, "bvar")) >= 0) { aux = MKAUX(0, 0, (uint64_t)num(y)); }
      else if ((y = get(r, "sort")) >= 0) { aux = MKAUX(1, 0, (uint64_t)num(y)); }
      else if ((y = get(r, "natVal")) >= 0) { aux = 9; fprintf(FLIT, "%llu\tn\t%.*s\n", (unsigned long long)ie, P[y].sl > 200 ? 200 : P[y].sl, P[y].s); }
      else if ((y = get(r, "strVal")) >= 0) { aux = 10; fprintf(FLIT, "%llu\ts\t%.*s\n", (unsigned long long)ie, P[y].sl > 200 ? 200 : P[y].sl, P[y].s); }
      else { fprintf(stderr, "unknown expr line %llu: %.200s\n", (unsigned long long)ln, line); die("unknown expr"); }
      AUX[ie] = aux;
      C1[ie] = a; C2[ie] = b;
    } else if ((x = get(r, "in")) >= 0) {
      uint64_t n = (uint64_t)num(x); name_reserve(n); int y;
      if ((y = get(r, "str")) >= 0) { int s = get(y, "str"); NPRE[n] = (uint32_t)num(get(y, "pre")); NOFF[n] = sp_add(P[s].s, P[s].sl); }
      else if ((y = get(r, "num")) >= 0) { char b[32]; int l = snprintf(b, sizeof b, "%lld", num(get(y, "i"))); NPRE[n] = (uint32_t)num(get(y, "pre")); NOFF[n] = sp_add(b, l); NISNUM[n] = 1; }
      else die("bad name");
    } else if ((x = get(r, "il")) >= 0) {
      int y; long long il = num(x);
      if ((y = get(r, "param")) >= 0) fprintf(FLEV, "%lld\tp\t%lld\t0\n", il, num(y));
      else if ((y = get(r, "succ")) >= 0) fprintf(FLEV, "%lld\ts\t%lld\t0\n", il, num(y));
      else if ((y = get(r, "max")) >= 0 || (y = get(r, "imax")) >= 0) fprintf(FLEV, "%lld\t%s\t%lld\t%lld\n", il, get(r, "max") >= 0 ? "m" : "i", num(P[y].child), num(P[P[y].child].next));
      else die("bad level");
    } else if (get(r, "meta") >= 0) {
    } else {
      const char *kinds[] = { "thm", "def", "opaque", "axiom", "quot" }; int done = 0;
      for (int k = 0; k < 5 && !done; k++) if ((x = get(r, kinds[k])) >= 0) {
        uint32_t nm = (uint32_t)num(get(x, "name")); long long tr = num(get(x, "type")); int vv = get(x, "value");
        long long vr = vv >= 0 ? num(vv) : -1;
        uint64_t td = walk((uint32_t)tr), vd = vr >= 0 ? walk((uint32_t)vr) : 0;
        emit(kinds[k], nm, td, vd, tr, vr); done = 1;
      }
      if (!done && (x = get(r, "inductive")) >= 0) {
        int ts = get(x, "types"), cs = get(x, "ctors"), rs = get(x, "recs");
        uint32_t nm = 0; long long tr = -1; uint64_t td = 0, vd = 0;
        for (int t = ts >= 0 ? P[ts].child : -1; t >= 0; t = P[t].next) {
          uint32_t n = (uint32_t)num(get(t, "name")); long long ty = num(get(t, "type"));
          if (!nm) { nm = n; tr = ty; } else member(ndecl, n, ty);
          td += walk((uint32_t)ty);
        }
        for (int c = cs >= 0 ? P[cs].child : -1; c >= 0; c = P[c].next) { long long ct = num(get(c, "type")); member(ndecl, (uint32_t)num(get(c, "name")), ct); vd += walk((uint32_t)ct); }
        for (int c = rs >= 0 ? P[rs].child : -1; c >= 0; c = P[c].next) {
          { long long ct = num(get(c, "type")); member(ndecl, (uint32_t)num(get(c, "name")), ct); vd += walk((uint32_t)ct); }
          int ru = get(c, "rules");
          for (int q = ru >= 0 ? P[ru].child : -1; q >= 0; q = P[q].next) vd += walk((uint32_t)num(get(q, "rhs")));
        }
        if (!nm) die("inductive without type");
        emit("inductive", nm, td, vd, tr, -1); done = 1;
      }
      if (!done) { fprintf(stderr, "unknown line %llu: %.300s\n", (unsigned long long)ln, line); die("unknown"); }
    }
  }
  fclose(FD); fclose(FM); fclose(FE);
  snprintf(p, sizeof p, "%s/names.tsv", out); FILE *fn = fopen(p, "w");
  for (uint64_t i = 0; i < dnn; i++) { fprintf(fn, "%u\t", DN[i]); name_print(fn, DN[i]); fputc('\n', fn); }
  fclose(fn);
  { uint64_t nn = ncap; while (nn > 1 && NOFF[nn - 1] == (uint64_t)-1) nn--;
    snprintf(p, sizeof p, "%s/names_pre.u32", out); FILE *f1 = fopen(p, "wb"); fwrite(NPRE, 4, nn, f1); fclose(f1);
    snprintf(p, sizeof p, "%s/names_off.u64", out); f1 = fopen(p, "wb"); fwrite(NOFF, 8, nn, f1); fclose(f1);
    snprintf(p, sizeof p, "%s/names_pool.bin", out); f1 = fopen(p, "wb"); fwrite(SP, 1, spn, f1); fclose(f1);
    fprintf(stderr, "names %llu pool %llu\n", (unsigned long long)nn, (unsigned long long)spn); }
  fclose(FLIT); fclose(FLEV);
  snprintf(p, sizeof p, "%s/lets.bin", out); FILE *fl = fopen(p, "wb");
  for (uint64_t i = 0; i < lcap; i++) if (LK[i] != NONE) { fwrite(&LK[i], 4, 1, fl); fwrite(&LV[i], 4, 1, fl); }
  fclose(fl);
  snprintf(p, sizeof p, "%s/stats.txt", out); FILE *fs = fopen(p, "w");
  fprintf(fs, "lines %llu\nexprs %llu\nnonseq_ie %llu\ndecls %llu\nnames_cap %llu\nlets %llu\n", (unsigned long long)ln,
          (unsigned long long)nexpr, (unsigned long long)nonseq, (unsigned long long)ndecl, (unsigned long long)ncap, (unsigned long long)lcnt);
  fclose(fs);
  msync(C1, nexpr * 4, MS_ASYNC); msync(C2, nexpr * 4, MS_ASYNC);
  msync(AUX, nexpr * 4, MS_ASYNC); munmap(C1, CAP * 4); munmap(C2, CAP * 4); munmap(AUX, CAP * 4); munmap(ISLET, CAP / 8);
  snprintf(p, sizeof p, "%s/c1.u32", out); truncate(p, (off_t)(nexpr * 4));
  snprintf(p, sizeof p, "%s/c2.u32", out); truncate(p, (off_t)(nexpr * 4));
  snprintf(p, sizeof p, "%s/aux.u32", out); truncate(p, (off_t)(nexpr * 4));
  fprintf(stderr, "done: lines %llu exprs %llu decls %llu nonseq %llu\n", (unsigned long long)ln, (unsigned long long)nexpr, (unsigned long long)ndecl, (unsigned long long)nonseq);
  return 0;
}
