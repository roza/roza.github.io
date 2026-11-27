"""occ.py OUT DECL CIBLE… : où les constantes CIBLE apparaissent dans la valeur (et le type) de DECL,
avec la tête de l'application englobante. Parcours complet du DAG (mémo par nœud)."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import lexpr
OUT, D, *T = sys.argv[1:]
E = lexpr.load(OUT)
tg = {E.byname[t] for t in T}
def head(e):
    h, a = E.spine(e)
    return h, a
def hname(h):
    return E.cname(h) if E.KIND(h) == 2 else f"<{['bvar','sort','const','app','lam','pi','let','proj','mdata','nat','str'][E.KIND(h)]}>"
def is_t(e):
    return E.KIND(e) == 2 and (E.C1[e] & ~lexpr.CB) in tg
cn = E.byname[D]
seen = set(); out = {}
roots = [('valeur', E.vroot[cn]), ('type', E.troot.get(cn))]
for lab, r in roots:
    if r is None or r < 0: continue
    st = [(r, '⊤', -1)]
    while st:
        e, par, idx = st.pop()
        if e in seen: continue
        seen.add(e)
        k = E.KIND(e)
        if k == 3:
            h, a = head(e)
            hn = hname(h)
            if is_t(h):
                key = (lab, E.cname(h), 'tête', par, idx, len(a)); out[key] = out.get(key, 0) + 1
            for i, x in enumerate(a):
                hx, _ = head(x)
                if is_t(hx):
                    key = (lab, E.cname(hx), 'argument', hn, i, len(_)); out[key] = out.get(key, 0) + 1
                st.append((x, hn, i))
            if E.KIND(h) != 2: st.append((h, par, idx))
        elif k in (4, 5):
            st.append((E.C1[e], par, idx)); st.append((E.C2[e], par, idx))
        elif k == 6:
            st.append((E.lets[e], par, idx)); st.append((E.C1[e], 'let', -1)); st.append((E.C2[e], par, idx))
        elif k in (7, 8):
            st.append((E.C1[e], par, idx))
        elif is_t(e):
            key = (lab, E.cname(e), 'nue', par, idx, 0); out[key] = out.get(key, 0) + 1
for k, v in sorted(out.items()):
    print(v, '\t'.join(map(str, k)), sep='\t')
print('# nœuds', len(seen), file=sys.stderr)
