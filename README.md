# RAVE-Mesh — paper result package

Consolidated experimental artifacts supporting the manuscript
*RAVE-Mesh: retrieval-augmented multi-agent natural-language-to-mesh automation*,
submitted to *Advanced Engineering Informatics*.

Every number in the paper's Table 2 and Fig. 9 can be re-derived from this repository
alone. Run `python _verify_package.py` to check.

Only material belonging to **this manuscript's two experiments** is included. Pilot-stage
runs, superseded harness versions, and results from other studies in the same working
directory have been deliberately left out (see §4.2).

**Raw mesh geometry is not included.** 7,350 Nastran `.bdf` files (12.2 GB) were
deliberately excluded — see §4.1 for why and how to regenerate them.

---

## 1. Contents

| Folder | Experiment | Paper section |
|---|---|---|
| `01_agent_ablation/` | 40 geometries × 5 configuration arms = **200 runs** | Section 4 (Table 2, Figs. 5–8) |
| `02_optimization_prior/` | 20 geometries × 3 optimizers × 2 conditions × 3 seeds = **360 runs** | Section 6 (Fig. 9) |
| `03_paper_figures/` | the manuscript's 12 figures as PNG | — |

The two studies ran as separate campaigns under separate harnesses. Each folder is
self-contained: it carries its own configuration, run records, and analysis code, and
neither depends on the other.

---

## 2. `01_agent_ablation/` — Section 4 (Table 2, Figs. 5–8)

40 CAD geometries × 5 configuration arms = **200 runs**.

### 2.1 Configuration arms

The arm folder names are internal harness labels and **do not read as the paper's
baseline names**. The mapping below is fixed by matching each arm's failure
signatures against the cases described in Sections 4.2 and 5.1:

| Folder | Validated rate | Paper name |
|---|---|---|
| `runs/rag` | 37/40 = 92.5 % | Baseline 1 — without engineering knowledge retrieval |
| `runs/skill` | 30/40 = 75.0 % | Baseline 2 — without predefined procedural guidance |
| `runs/subagent` | 38/40 = 95.0 % | Baseline 3 — without independent review |
| `runs/budget` | 0/40 = 0.0 % | Baseline 4 — one agent decision round |
| `runs/full` | 40/40 = 100.0 % | RAVE-Mesh (complete framework) |

Identification evidence — the failing geometries and their mesh diagnostics:

* `rag` → i07o_m7 (1,361 nodes / 3,676 tets / 4 boundary non-manifold edges),
  i23o_s31 (390 / 1,038 / 2), i31o_dlr_f6 (623 nodes / 0 tets) — Section 5.1, para. 2.
* `skill` → i23o_s31 (390 / 1,037 / 2), i31o_dlr_f6 (623 / 0) — Section 5.1, para. 3.
* `subagent` → i08o_m8 (287 / 0), i23o_s31 (327 / 875 / 2) — Section 5.1, para. 4.

### 2.2 Layout

```
01_agent_ablation/
  summary_40model.json        per-run records for all 200 runs (model, config,
                              runnable, failure_reason, wall_seconds, rounds,
                              tool_calls, mesh_diagnostics, final_text).
                              THIS is the source of Table 2 and Fig. 7.
  harness/run_eval_40model.py the 40-model evaluation harness that produced the runs
  harness/analyze_40model.py  the analysis script that reads summary_40model.json
  models_40/                  the 40 CAD inputs (STEP/STP/BREP)
  runs/<arm>/<geometry>/      result.json  — metrics + mesh diagnostics
                              run.log      — full agent tool trace
                              script.py    — the generated meshing script
```

`mesh_diagnostics` inside each `result.json` carries `node_count`, `tet_count`,
`degenerate_tet_count`, `inverted_tet_count`, and `violations`.

---

## 3. `02_optimization_prior/` — Section 6 (Fig. 9)

20 geometries × 3 optimizers × 2 initialization conditions × 3 seeds × 20 evaluations
= **360 runs / 7,200 real-software trials**.

Experiment ID: `a0-a0prime-etri-relative-validity-v2-20models-2026-09-07`.

### 3.1 Conditions

Each optimizer appears under two arm prefixes:

| Arm prefix | Condition |
|---|---|
| `random`, `parego`, `qlogehvi_mixed` | A0 — unseeded (random first evaluation) |
| `random_seed`, `parego_seed`, `qlogehvi_mixed_seed` | A0′ — first evaluation replaced by the frozen RAVE-Mesh configuration |

The reported effect is Δ = A0′ − A0.

### 3.2 Key files

```
02_optimization_prior/
  paper_metrics_model_level_tests.csv   <- PRIMARY. Geometry-level paired effects,
                                           bootstrap CI, Wilcoxon, Holm correction.
                                           Source of the paper's three ΔHV-AUC values.
  paper_metrics_paired.csv              per (optimizer, model, seed) deltas
  paper_metrics_per_run.csv             per-run metrics
  paper_metrics_per_model.csv           per-model aggregates
  paper_metrics_overall.csv             per-arm descriptives
  paper_metrics_curves.csv              HV trajectories
  paper_metrics_20models.json           full metrics blob
  paper_metrics_paired_tests.csv
  benchmark_summary.csv / .json         run-level summary records
  figure_20models_*.png / .pdf          convergence / heterogeneity / prior+validity
  config.a0_a0prime_etri_relative_20models.json
                                        THE config this study ran under. Its
                                        experiment_id matches every run_manifest.json.
  config.a0_a0prime_etri_relative_20models.defaults-audit.json
                                        frozen parameter-space audit for the above
  ETRI_RELATIVE_PROTOCOL.md             the ETri relative parameter-space protocol
  runs/<arm>__<geometry>__seed-<n>/     summary.json, config.json, run_manifest.json,
                                        trials.jsonl, trial_NNN.json (20 per run)
  _gen_paper_figures.py                 reads paper_metrics_*.csv -> figures
  实验结果分析.md, 实验策略.md               analysis notes for this study (in Chinese)
```

Each `run_manifest.json` records the harness Python version, the platform, the config
SHA-256, and the SHA-256 of eight harness source modules — sufficient to verify that
the runs were produced by one frozen code state.

### 3.3 Values this package reproduces

| optimizer | ΔHV-AUC | 95 % CI | W/T/L | p (Holm) | in paper |
|---|---|---|---|---|---|
| random | −0.00116 | [−0.0053, +0.0023] | 9/0/11 | 1.000 | −0.00116 |
| parego | −0.00314 | [−0.0087, +0.0016] | 8/0/12 | 1.000 | −0.00314 |
| qlogehvi_mixed | −0.00101 | [−0.0063, +0.0034] | 10/0/10 | 1.000 | −0.00101 |

---

## 4. What is **not** here

### 4.1 Mesh geometry dumps

**7,350 Nastran `.bdf` mesh files, 12.2 GB**, were deliberately not copied. These are
the raw tetrahedral mesh geometry exported by each run (`runs/<arm>/<geometry>/mesh.bdf`
in the ablation, `runs/<arm>__<geometry>__seed-N/trial_NNN.bdf` in the optimization
study). They are bulky and fully regenerable from the retained scripts and
configuration; the derived mesh-quality diagnostics that the paper actually cites are
already stored in every `result.json` / `trial_NNN.json`.

They are not published here and cannot be restored from this repository. They are,
however, fully regenerable: re-run `01_agent_ablation/harness/run_eval_40model.py`
for the ablation, or the Section 6 benchmark harness under `02_optimization_prior/`,
using the frozen configurations included alongside them.

### 4.2 Deliberately excluded as belonging to other work

These sat alongside the paper's data in the source directory but are **not** used by
this manuscript:

* **Superseded pilot runs** — a 10-model / 50-run stage-1 ablation, included in the
  source as `summary.json`, `summary_full_50.json`, `stage1*.log`, `report_stage1.md`.
  Superseded by the 200-run campaign; not the source of any paper number.
* **Superseded harness versions** — `run_eval.py` and `run_eval_parallel.py` are the
  earlier 10-model launchers, replaced by `run_eval_40model.py`.
* **A separate 6-geometry confirmation study** — `analysis_a0_a0prime_2x3/`,
  `config.a0_a0prime_random_parego_qlogehvi_confirm.json`, and
  `A0_A0prime_Random_ParEGO_qLogEHVI_预注册_2026-08-28.md`. Its reported effects
  (+0.0800 / +0.0706 / −0.1115) are on a different scale from the paper's and come
  from 6 geometries, not 20. **Do not confuse its config with this study's** — the
  Section 6 config is `config.a0_a0prime_etri_relative_20models.json`.
* **Retrieval scoring** — `retrieval_score.json`, `score_retrieval.py`. The manuscript
  reports no retrieval-quality metric.
* **Unrelated helper scripts** — `make_result_plots.py` points at a results folder that
  no longer exists; `prior_scores_4exp_v2.json` belongs to a separate 4-experiment
  prior study; `期刊选择.md` is journal-selection strategy, not a result;
  `test_archer_concurrency.py` and `scripts/mesh_i0*.py` are development smoke tests.
* **Campaign console logs** — `run.*.log`, `resume-4w.*.log`, `final-*.log` in
  `20模型/`. These are retry-attempt console output; the authoritative per-run record
  is `runs/*/summary.json` plus `run_manifest.json`.

---

## 5. Caveats

* The commercial **ArcherSimNX** executable and its licence environment cannot be
  redistributed, so the runs are not bit-for-bit reproducible externally. Prompts,
  configuration definitions, generated procedures, logs, mesh diagnostics and
  analysis artifacts are all included to support audit and partial reproduction.
  This is the same limitation stated in the manuscript's Data and Reproducibility
  Statement.
* **The agent-ablation side records no software-version manifest.** The optimization
  study's runs each carry a `run_manifest.json`; the 200 ablation runs do not. The
  ArcherSimNX build cited in the paper (`1.9.6.v1.a797bb1c`) is confirmed by the
  installed directory `D:\ProgramFiles\1.9.6.v1.a797bb1c\`, and the mesher version
  (`ArcherPre 3.1.1118`) by the `$$ Generated by GY.Soft-ArcherPre` header of every
  exported BDF — but neither is a contemporaneous per-run record. If a reviewer asks
  for an exact software-version table covering the ablation, this is the weak point.

---

## 6. License

The harness and analysis code (all `.py` files) is released under the **MIT License**
— see `LICENSE`.

The experimental result data — run records, mesh diagnostics, metrics, analysis
tables, configurations, logs, generated scripts, and figures — is released under
**Creative Commons Attribution 4.0 International (CC BY 4.0)** — see `LICENSE-DATA`.

The commercial ArcherSimNX executable used to produce these results is not
distributed here and remains subject to its own license terms.
