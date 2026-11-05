"""Apply update files ([{id, set, evidenceAdd, delete}]) and new-item files to data.json.
usage: python3 apply_updates.py --updates a.json b.json --new c.json d.json [--dry]
"""
import json, sys, argparse
p = argparse.ArgumentParser()
p.add_argument("--updates", nargs="*", default=[])
p.add_argument("--new", nargs="*", default=[])
p.add_argument("--dry", action="store_true")
p.add_argument("--date", default="2026-11-05")
a = p.parse_args()
PATH = "/Users/mon/Developer/NamaOnsen/data.json"
d = json.load(open(PATH))
items = d["items"]; byid = {x["id"]: x for x in items}
CL = {"なし（公式）", "なし（口コミ）", "不明", "あり"}
log = []
for f in a.updates:
    for u in json.load(open(f)):
        x = byid.get(u["id"])
        if not x:
            log.append(f"MISSING {u['id']} {u.get('name')} ({f})"); continue
        if u.get("delete"):
            items.remove(x); del byid[u["id"]]; log.append(f"DELETE {x['name']}: {u.get('reason')}"); continue
        s = u.get("set", {})
        if "chlorine" in s and s["chlorine"] not in CL:
            log.append(f"BADCL {x['name']} {s['chlorine']}"); continue
        for k, v in s.items():
            if k == "chlorine" and x.get(k) != v:
                log.append(f"CL {x['name']}: {x.get(k)} -> {v}")
            x[k] = v
        ev = u.get("evidenceAdd")
        if ev:
            ev = ev.strip()
            if not ev.startswith("- "): ev = "- " + ev
            x["evidence"] = (x.get("evidence", "").rstrip() + "\n" + ev).strip()
        x["checkedAt"] = a.date
seen_names = {(x["name"], x.get("address")) for x in items}
for f in a.new:
    for n in json.load(open(f)):
        if n["id"] in byid:
            log.append(f"DUPID {n['id']} {n['name']} ({f})"); continue
        need = ["id", "name", "prefecture", "address", "lat", "lng", "kakenagashi", "chlorine", "url", "evidence"]
        miss = [k for k in need if not n.get(k)]
        if miss or n["chlorine"] not in CL:
            log.append(f"BADNEW {n.get('name')} missing={miss} cl={n.get('chlorine')} ({f})"); continue
        if n.get("hasSauna") not in ("あり", "なし"):
            log.append(f"NOSAUNA {n['id']} {n['name']} (fill hasSauna!)")
        items.append(n); byid[n["id"]] = n; log.append(f"NEW {n['prefecture']} {n['name']} [{n['chlorine']}]")
d["updated"] = a.date
print("\n".join(log)); print("total", len(items))
if not a.dry:
    json.dump(d, open(PATH, "w"), ensure_ascii=False, indent=0)
