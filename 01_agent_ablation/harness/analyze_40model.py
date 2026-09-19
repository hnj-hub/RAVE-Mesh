"""Analyze 40-model agent experiment results."""
import json
from collections import Counter, defaultdict
from math import sqrt

FAMILY = {}
for mid in open(r"D:\新建文件夹\my-agent\evals_p0_1_agent\run_eval_40model.py", encoding="utf-8"):
    pass  # just use inline
# Hardcode family for quick analysis
def get_family(mid):
    if mid.startswith("i"): return "industrial"
    if mid.startswith("s"): return "basic"
    if mid.startswith("n"): return "topology"
    return "unknown"

with open(r"D:\新建文件夹\my-agent\evals_p0_1_agent\summary_40model.json", encoding="utf-8") as f:
    data = json.load(f)

# 1. Overall by config
print("=== Per-Config Summary ===")
by_config = defaultdict(list)
for r in data:
    by_config[r["config"]].append(r)

for config in ["full", "rag", "skill", "subagent", "budget"]:
    rs = by_config[config]
    ok = sum(1 for r in rs if r["runnable"])
    n = len(rs)
    z = 1.96
    p = ok / n if n > 0 else 0
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    lo = max(0, center - margin)
    hi = min(1, center + margin)
    avg_wall = sum(r["wall_seconds"] for r in rs) / n
    avg_rounds = sum(r["rounds"] for r in rs) / n
    avg_tools = sum(r["tool_calls"] for r in rs) / n
    first_ok = sum(1 for r in rs if r["first_attempt"])
    print(f"  {config:12s}: {ok:2d}/{n} = {ok/n:.0%}  "
          f"Wilson 95% CI [{lo:.1%}, {hi:.1%}]  "
          f"avg_wall={avg_wall:.1f}s  avg_rounds={avg_rounds:.1f}  "
          f"avg_tools={avg_tools:.1f}  first_attempt={first_ok}/{n}")

# 2. Failure reasons
print("\n=== Failure Reasons ===")
for config in ["full", "rag", "skill", "subagent", "budget"]:
    rs = [r for r in by_config[config] if not r["runnable"]]
    reasons = Counter(r["failure_reason"] for r in rs)
    print(f"  {config}: {dict(reasons)}")

# 3. Full config failures detail
print("\n=== Full Config Failures (detail) ===")
full_fails = [r for r in by_config["full"] if not r["runnable"]]
for r in full_fails:
    diag = r.get("mesh_diagnostics")
    if diag:
        print(f"  {r['model']} ({get_family(r['model'])}): {r['failure_reason']}")
        print(f"    nodes={diag.get('node_count')} tets={diag.get('tet_count')} "
              f"degen={diag.get('degenerate_tet_count')} invert={diag.get('inverted_tet_count')} "
              f"violations={diag.get('violations')}")
    else:
        print(f"  {r['model']} ({get_family(r['model'])}): {r['failure_reason']} | {r['detail']}")

# 4. Cross-config failure patterns
print("\n=== Cross-Config Failure Patterns ===")
model_fails = defaultdict(list)
for r in data:
    if not r["runnable"]:
        model_fails[r["model"]].append(r["config"])
for model, configs in sorted(model_fails.items(), key=lambda x: -len(x[1])):
    print(f"  {model} ({get_family(model):12s}): fails in {len(configs)}/5: {configs}")

# 5. Category breakdown
print("\n=== Category Breakdown ===")
for fam in ["industrial", "basic", "topology"]:
    rs = [r for r in data if get_family(r["model"]) == fam]
    ok = sum(1 for r in rs if r["runnable"])
    n = len(rs)
    print(f"  {fam:12s}: {ok}/{n} = {ok/n:.0%}")

# 6. Consistent failures (fail in Full + at least 2 more configs)
print("\n=== Persistently Hard Models (fail Full + >=2 other configs) ===")
hard = {m: cs for m, cs in model_fails.items()
        if "full" in cs and len(cs) >= 3}
for model, configs in sorted(hard.items(), key=lambda x: -len(x[1])):
    print(f"  {model} ({get_family(model)}): fails in {configs}")

# 7. Models that succeed in Full but fail in others
print("\n=== Full-Only Successes (pass Full, fail in others) ===")
full_ok = {r["model"] for r in by_config["full"] if r["runnable"]}
for model, configs in sorted(model_fails.items()):
    if model in full_ok:
        print(f"  {model} ({get_family(model)}): passes Full, fails in {configs}")

# 8. Wall time stats
print("\n=== Wall Time Stats ===")
walls = [r["wall_seconds"] for r in data if r["runnable"]]
if walls:
    print(f"  Successful runs: min={min(walls):.1f}s  max={max(walls):.1f}s  "
          f"mean={sum(walls)/len(walls):.1f}s  median={sorted(walls)[len(walls)//2]:.1f}s")
failed_walls = [r["wall_seconds"] for r in data if not r["runnable"]]
if failed_walls:
    print(f"  Failed runs:     min={min(failed_walls):.1f}s  max={max(failed_walls):.1f}s  "
          f"mean={sum(failed_walls)/len(failed_walls):.1f}s")

# 9. Token estimate (rough: rounds * avg context)
print("\n=== Rough Token Estimate ===")
total_rounds = sum(r["rounds"] for r in data)
total_tools = sum(r["tool_calls"] for r in data)
print(f"  Total LLM rounds: {total_rounds}")
print(f"  Total tool calls: {total_tools}")
print(f"  Avg rounds/run: {total_rounds/len(data):.1f}")
print(f"  Avg tools/run: {total_tools/len(data):.1f}")