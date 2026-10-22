"""Acrescenta vagas novas a vagas.json sem repetir.

Uso:  python add_vagas.py novas.json [--push]

novas.json = lista de objetos {t, e, d, s, u, r, dt, p, c}
  t título | e empresa | d descrição | s nota (0-100) | u link | r dicas
  dt data (AAAA-MM-DD) | p plataforma | c (opcional) já candidatou
Dedupe por link e por título+empresa. Nunca apaga nem altera vagas existentes.
"""
import json, subprocess, sys, pathlib

base = pathlib.Path(__file__).parent
path = base / "vagas.json"
cur = json.loads(path.read_text(encoding="utf-8"))
new = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))

seen = set()
for x in cur:
    seen.add(x["u"])
    seen.add((x["t"].lower().strip(), x["e"].lower().strip()))

added = 0
for x in new:
    k = (x["t"].lower().strip(), x["e"].lower().strip())
    if not x.get("u") or x["u"] in seen or k in seen:
        continue
    x.setdefault("c", False)
    cur.append({k2: x[k2] for k2 in ("t", "e", "d", "s", "u", "r", "dt", "p", "c")})
    seen.add(x["u"]); seen.add(k)
    added += 1

path.write_text(json.dumps(cur, ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{added} vagas novas; total {len(cur)}")

if "--push" in sys.argv and added:
    def git(*a): subprocess.run(["git", "-C", str(base), *a], check=True)
    git("add", "vagas.json")
    git("commit", "-m", f"Vagas: +{added}")
    git("push")
