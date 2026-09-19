# -*- coding: utf-8 -*-
"""P0-1 智能体定量评估 — 40 模型版：40 模型 × 5 消融配置 = 200 run。

与 10 模型版 run_eval_parallel.py 的核心差异：
  1. 模型集从 10 → 40（Industrial 28 + Basic 9 + Topology 3）
  2. NL 模板从中文 → 英文统一模板（skill 已覆盖技术细节，NL 只说做什么）
  3. Mesh 判定从简单 check_bdf() → validate_bdf_tetra_mesh()（与主实验一致）
  4. 新增指标：first_attempt、tool_calls、mesh_validation 诊断

口径（与预注册 §3.1 一致）：
  可运行 = validate_bdf_tetra_mesh() 返回 mesh_valid=True
  config ∈ {full, rag, skill, subagent, budget}

用法：
  # Pilot（5 模型）
  python run_eval_40model.py --workers 5 --pilot

  # 全量 40 模型
  python run_eval_40model.py --workers 8

  # 单模型冒烟
  python run_eval_40model.py --model i01o_m1 --config full
"""
import argparse
import contextlib
import json
import multiprocessing
import shutil
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

# ── 路径（适配 D: 盘实际环境） ──────────────────────────────────
MODEL_DIR = Path(r"D:\新建文件夹\论文\LLM闭环网格优化方法包\tests\hex-me-if-you-can-main\original")
EVAL_DIR = REPO / "evals_p0_1_agent"
MODELS_DIR = EVAL_DIR / "models_40"
MESH_PACKAGE_DIR = Path(r"D:\新建文件夹\论文\LLM闭环网格优化方法包")
sys.path.insert(0, str(MESH_PACKAGE_DIR / "src"))  # 让 worker 能 import mesh_optimization

# ── 40 模型清单 ──────────────────────────────────────────────────
# 排除 .geo 文件（ArcherSimNX 不兼容）和 3 个超大复杂模型
MODELS = {
    # Industrial（28 个）
    "i01o_m1": "i01o_m1.step",
    "i02o_m2": "i02o_m2.step",
    "i03o_m3": "i03o_m3.step",
    "i04o_m4": "i04o_m4.step",
    "i05o_m5": "i05o_m5.step",
    "i06o_m6": "i06o_m6.step",
    "i07o_m7": "i07o_m7.step",
    "i08o_m8": "i08o_m8.step",
    "i09o_m9": "i09o_m9.step",
    "i10o_simp": "i10o_simp.step",
    "i11o_s1": "i11o_s1.step",
    "i12o_s5": "i12o_s5.step",
    "i13o_s6": "i13o_s6.step",
    "i14o_s7": "i14o_s7.step",
    "i15o_s8": "i15o_s8.step",
    "i16o_s9": "i16o_s9.step",
    "i17o_s20": "i17o_s20.step",
    "i18o_s22": "i18o_s22.step",
    "i19o_s24": "i19o_s24.step",
    "i20o_s25": "i20o_s25.step",
    "i21o_s26": "i21o_s26.step",
    "i22o_s27": "i22o_s27.step",
    "i23o_s31": "i23o_s31.step",
    "i24o_s34": "i24o_s34.step",
    "i25o_s40": "i25o_s40.step",
    "i29o_bracket": "i29o_bracket.step",
    "i30o_9858_screw": "i30o_9858_screw.step",
    "i31o_dlr_f6": "i31o_dlr_f6.brep",
    # Basic（9 个）
    "s09o_bridge": "s09o_bridge.step",
    "s10o_cyl_cutsphere": "s10o_cyl_cutsphere.stp",
    "s11o_cube_cyl": "s11o_cube_cyl.stp",
    "s12o_cube_rounded_1": "s12o_cube_rounded_1.stp",
    "s13o_cube_rounded_2": "s13o_cube_rounded_2.stp",
    "s14o_cube_corner_sub_sphere": "s14o_cube_corner_sub_sphere.stp",
    "s15o_cylinder": "s15o_cylinder.stp",
    "s16o_torus": "s16o_torus.stp",
    "s17o_sphere": "s17o_sphere.stp",
    # Topology（3 个）
    "n10o_qtorus_cyl": "n10o_qtorus_cyl.step",
    "n11o_limit_cycle": "n11o_limit_cycle.stp",
    "n12o_limit_cycle_genus0": "n12o_limit_cycle_genus0.stp",
}

# Pilot 模型（每类 1-2 个代表，4 个已知稳定 + 1 个新模型）
PILOT_MODELS = ["i01o_m1", "i09o_m9", "s16o_torus", "n10o_qtorus_cyl", "i30o_9858_screw"]

FAMILY = {}
for _mid in MODELS:
    if _mid.startswith("i"):
        FAMILY[_mid] = "industrial"
    elif _mid.startswith("s"):
        FAMILY[_mid] = "basic"
    elif _mid.startswith("n"):
        FAMILY[_mid] = "topology"

CONFIGS = ["full", "rag", "skill", "subagent", "budget"]
CONFIG_ABLATION = {
    "full": None, "rag": "rag", "skill": "skill",
    "subagent": "subagent", "budget": "budget",
}

# ── 模型复制 ────────────────────────────────────────────────────
def copy_models():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    for model_id, fname in MODELS.items():
        src = MODEL_DIR / fname
        dst = MODELS_DIR / fname
        if not src.exists():
            print(f"[FATAL] 模型源不存在: {src}")
            sys.exit(1)
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
    print(f"[models] {len(MODELS)} 模型就绪于 {MODELS_DIR}")


# ── NL 模板（英文统一，技术细节由 skill 注入） ──────────────────
def build_prompt(model_id, model_path, bdf_path, script_path):
    script_dir = str(Path(script_path).parent)
    return (
        f"Generate a tetrahedral mesh for the CAD model at \"{model_path}\".\n"
        f"Export the result as a Nastran BDF file to \"{bdf_path}\".\n"
        f"The BDF must contain GRID nodes and CTETRA elements with element count > 0.\n"
        f"Do NOT report success unless the exported BDF passes validation.\n"
        f"\n"
        f"CRITICAL: Use write_file to create the mesh script, then run_archer_script to execute it.\n"
        f"DO NOT use bash to explore directories, list files, find Python/ArcherPre paths, "
        f"or run ArcherSimNX directly. DO NOT use bash unless absolutely necessary.\n"
        f"Use read_file to read the skill file (already loaded), "
        f"write_file to write the script to \"{script_path}\", "
        f"then run_archer_script to execute it. "
        f"Work efficiently — you have limited rounds."
    )


# ── Mesh 判定（升级为 validate_bdf_tetra_mesh） ──────────────────
def validate_mesh(bdf_path: Path, run_dir: Path) -> dict:
    """返回 {runnable, failure_reason, detail, mesh_diagnostics}。"""
    # 先找 BDF 文件
    candidates = [bdf_path] if bdf_path.exists() else []
    if not candidates:
        candidates = sorted(run_dir.rglob("*.bdf"), key=lambda p: p.stat().st_size, reverse=True)
    if not candidates:
        return {
            "runnable": False, "failure_reason": "no_bdf",
            "detail": "未生成任何 .bdf", "mesh_diagnostics": None,
        }
    # 对每个候选 BDF 跑 validate_bdf_tetra_mesh
    from mesh_optimization.mesh_validation import validate_bdf_tetra_mesh

    for cand in candidates:
        if cand.stat().st_size <= 1024:
            continue
        try:
            diag = validate_bdf_tetra_mesh(cand)
        except Exception as exc:
            return {
                "runnable": False, "failure_reason": "validation_error",
                "detail": f"{type(exc).__name__}: {exc}", "mesh_diagnostics": None,
            }
        if diag["mesh_valid"]:
            return {
                "runnable": True, "failure_reason": None,
                "detail": f"OK({cand.name}, {cand.stat().st_size} bytes, "
                          f"{diag['node_count']} nodes, {diag['tet_count']} tets)",
                "mesh_diagnostics": diag,
            }
        # BDF 存在但 mesh 无效，记录原因
        violations_str = ", ".join(
            f"{k}={v}" for k, v in diag.get("violations", {}).items()
        )
        return {
            "runnable": False, "failure_reason": "MESH_INVALID",
            "detail": f"{cand.name}: {diag['node_count']} nodes, {diag['tet_count']} tets — "
                      f"violations: {violations_str or 'none'}",
            "mesh_diagnostics": diag,
        }
    # 有文件但都不达标
    if candidates:
        try:
            size = candidates[0].stat().st_size
        except Exception:
            size = 0
        return {
            "runnable": False, "failure_reason": "bdf_invalid",
            "detail": f"{candidates[0].name}: {size} bytes, 不满足验证标准",
            "mesh_diagnostics": None,
        }
    return {
        "runnable": False, "failure_reason": "bdf_invalid",
        "detail": "bdf 存在但不达标", "mesh_diagnostics": None,
    }


# ── 辅助 ────────────────────────────────────────────────────────
def _final_text(history):
    for msg in reversed(history):
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content", "")
        if isinstance(content, list):
            joined = "".join(b.text for b in content if hasattr(b, "text")).strip()
            if joined:
                return joined
        elif isinstance(content, str) and content.strip():
            return content.strip()
    return ""


def _count_tool_calls(history):
    """统计 history 中所有 tool_use 块的数量。"""
    n = 0
    for msg in history:
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content", "")
        if isinstance(content, list):
            n += sum(1 for b in content if hasattr(b, "type") and b.type == "tool_use")
    return n


# ── Worker ──────────────────────────────────────────────────────
def _worker(task):
    """跑一个 (model_id, config)。顶层函数，供 Pool 跨进程 pickle。

    已有完整 result.json 的 run 直接复用（resume），不重跑。
    """
    model_id, config = task
    run_dir = EVAL_DIR / config / model_id
    cached = run_dir / "result.json"
    if cached.exists():
        try:
            prev = json.loads(cached.read_text(encoding="utf-8"))
            # 必须包含所有新字段才复用；旧缓存缺字段则重跑
            if "tool_calls" in prev and "mesh_diagnostics" in prev:
                return prev
        except Exception:
            pass

    # ⚠️ 环境变量必须在 import harness 之前设置（harness 在模块加载时读取）
    import os
    os.environ["MESH_PACKAGE_DIR"] = str(MESH_PACKAGE_DIR)
    # mesh_optimization 包路径（validate_bdf_tetra_mesh 依赖）
    sys.path.insert(0, str(MESH_PACKAGE_DIR / "src"))

    from myagent import harness

    harness.set_ablation(CONFIG_ABLATION[config])
    run_dir.mkdir(parents=True, exist_ok=True)
    model_path = (MODELS_DIR / MODELS[model_id]).resolve().as_posix()
    bdf_path = (run_dir / "mesh.bdf").resolve()
    script_path = (run_dir / "script.py").resolve()
    prompt = build_prompt(model_id, model_path, bdf_path.as_posix(), script_path.as_posix())

    history = [{"role": "user", "content": prompt}]
    started = time.perf_counter()
    exc_info = ""
    with open(run_dir / "run.log", "w", encoding="utf-8", errors="replace") as logf:
        with contextlib.redirect_stdout(logf):
            try:
                harness.agent_loop(history, system=harness.SYSTEM)
            except Exception as exc:
                exc_info = f"{type(exc).__name__}: {exc}"
    wall = round(time.perf_counter() - started, 2)
    final_text = _final_text(history)
    n_rounds = sum(1 for m in history if m.get("role") == "assistant")
    n_tool_calls = _count_tool_calls(history)

    if exc_info:
        runnable, reason, detail = False, f"agent_exc:{exc_info.split(':')[0]}", exc_info
        mesh_diag = None
    else:
        validation = validate_mesh(bdf_path, run_dir)
        runnable = validation["runnable"]
        reason = validation["failure_reason"]
        detail = validation["detail"]
        mesh_diag = validation["mesh_diagnostics"]

    # 提取 mesh 诊断摘要（避免序列化过大）
    mesh_summary = None
    if mesh_diag:
        mesh_summary = {
            "node_count": mesh_diag.get("node_count"),
            "tet_count": mesh_diag.get("tet_count"),
            "degenerate_tet_count": mesh_diag.get("degenerate_tet_count"),
            "inverted_tet_count": mesh_diag.get("inverted_tet_count"),
            "violations": mesh_diag.get("violations"),
        }

    result = {
        "model": model_id, "family": FAMILY[model_id], "config": config,
        "runnable": runnable, "failure_reason": reason, "detail": detail,
        "wall_seconds": wall, "rounds": n_rounds, "tool_calls": n_tool_calls,
        "first_attempt": (n_rounds <= 2 and runnable),
        "mesh_diagnostics": mesh_summary,
        "final_text": final_text[:2000],
    }
    (run_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


# ── Main ────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="40-Model Domain-Coding Agent Evaluation")
    parser.add_argument("--workers", type=int, default=2, help="并行 worker 进程数（默认 2，避免 API 限流）")
    parser.add_argument("--model", default=None, help="只跑指定 model（冒烟）")
    parser.add_argument("--config", default=None, help="只跑指定 config（冒烟）")
    parser.add_argument("--pilot", action="store_true", help="只跑 5 个 pilot 模型")
    parser.add_argument("--order", default="full,rag,skill,subagent,budget",
                        help="config 执行顺序（默认 full 优先，重要的先跑）")
    args = parser.parse_args()

    copy_models()

    if args.model:
        models = [args.model]
    elif args.pilot:
        models = PILOT_MODELS
    else:
        models = list(MODELS)

    configs = args.order.split(",")
    if args.config:
        configs = [args.config]

    tasks = [(m, c) for c in configs for m in models]

    print(f"[launch] {len(tasks)} 任务 × {args.workers} workers", flush=True)
    if args.pilot:
        print(f"[pilot] 模型: {models}", flush=True)
    t0 = time.time()
    results = []
    with multiprocessing.Pool(args.workers) as pool:
        for r in pool.imap_unordered(_worker, tasks):
            results.append(r)
            print(f"[{r['config']}/{r['model']}] runnable={r['runnable']} "
                  f"reason={r['failure_reason']} wall={r['wall_seconds']}s "
                  f"rounds={r['rounds']} tools={r['tool_calls']}", flush=True)

    summary_path = EVAL_DIR / "summary_40model.json"
    summary_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    elapsed = time.time() - t0
    print(f"\n写入 {summary_path}, 共 {len(results)} 条, 总耗时 {elapsed:.0f}s ({elapsed/60:.1f}min)", flush=True)

    for config in configs:
        rs = [r for r in results if r["config"] == config]
        if not rs:
            continue
        ok = sum(1 for r in rs if r["runnable"])
        print(f"  {config}: {ok}/{len(rs)} = {ok/len(rs):.0%}", flush=True)

    # 按类别汇总
    for family in ("industrial", "basic", "topology"):
        rs = [r for r in results if r["family"] == family]
        if not rs:
            continue
        ok = sum(1 for r in rs if r["runnable"])
        print(f"  [{family}] {ok}/{len(rs)} = {ok/len(rs):.0%}", flush=True)


if __name__ == "__main__":
    main()