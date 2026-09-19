"""Re-derive the paper's headline numbers from the consolidated package alone."""
import os, json, csv, collections

P = os.path.dirname(os.path.abspath(__file__))

print("=" * 70)
print("TABLE 2 — validated runnable rate (Section 4)")
print("=" * 70)
MAP = {
    "rag":      "Baseline 1 (without knowledge retrieval)",
    "skill":    "Baseline 2 (without procedural guidance)",
    "subagent": "Baseline 3 (without independent review)",
    "budget":   "Baseline 4 (one decision round)",
    "full":     "RAVE-Mesh (complete)",
}
for cfg in ["rag", "skill", "subagent", "budget", "full"]:
    d = os.path.join(P, "01_agent_ablation", "runs", cfg)
    ok = tot = 0
    for g in sorted(os.listdir(d)):
        rj = os.path.join(d, g, "result.json")
        if not os.path.isfile(rj):
            continue
        tot += 1
        with open(rj, encoding="utf-8") as f:
            if json.load(f).get("runnable") is True:
                ok += 1
    print(f"  {MAP[cfg]:<44} {ok:>2}/{tot}  = {100*ok/tot:.1f}%")

print()
print("=" * 70)
print("FIG 9 / Section 6 — paired effect of the agent prior")
print("=" * 70)
f = os.path.join(P, "02_optimization_prior", "paper_metrics_model_level_tests.csv")
with open(f, encoding="utf-8-sig") as fh:
    rows = [r for r in csv.DictReader(fh) if r["metric"] == "delta_hv_auc_mean"]
paper = {"random": "-0.00116", "parego": "-0.00314", "qlogehvi_mixed": "-0.00101"}
for r in rows:
    o = r["optimizer"]
    print(f"  {o:<16} dHV-AUC={float(r['mean']):+.5f}  CI=[{float(r['ci95_low']):+.4f}, {float(r['ci95_high']):+.4f}]"
          f"  W/T/L={r['wins']}/{r['ties']}/{r['losses']}  p_holm={float(r['p_holm']):.3f}"
          f"   (paper: {paper[o]})")

print()
print("=" * 70)
print("PACKAGE INVENTORY")
print("=" * 70)
for top in sorted(os.listdir(P)):
    p = os.path.join(P, top)
    if os.path.isdir(p):
        n = sum(len(fs) for _, _, fs in os.walk(p))
        sz = sum(os.path.getsize(os.path.join(r, x)) for r, _, fs in os.walk(p) for x in fs)
        print(f"  {top:<24} {n:>6} files  {sz/1e6:>8.1f} MB")
