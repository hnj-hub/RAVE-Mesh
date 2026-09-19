#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate all paper figures from 20-model experiment data for AEinfo submission."""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Config ---
DATA_DIR = r"D:\新建文件夹\论文\LLM闭环网格优化方法包\20模型"
OUT_DIR  = r"D:\新建文件夹\论文\LLM闭环网格优化方法包\figs_20model"
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 10, 'axes.titlesize': 12, 'axes.labelsize': 11,
    'xtick.labelsize': 9, 'ytick.labelsize': 9,
    'legend.fontsize': 9, 'figure.dpi': 150, 'savefig.dpi': 300,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.05,
})

# Color palette
C_RANDOM   = '#7f7f7f'
C_PAREGO   = '#ff7f0e'
C_QLOGEHVI = '#1f77b4'
C_A0       = '#2ca02c'
C_A0PRIME  = '#d62728'
POLICY_COLORS = {
    'random': C_RANDOM, 'random_seed': C_RANDOM,
    'parego': C_PAREGO, 'parego_seed': C_PAREGO,
    'qlogehvi_mixed': C_QLOGEHVI, 'qlogehvi_mixed_seed': C_QLOGEHVI,
}
POLICY_LABELS = {
    'random': 'Random', 'random_seed': 'Random (A0\')',
    'parego': 'ParEGO', 'parego_seed': 'ParEGO (A0\')',
    'qlogehvi_mixed': 'qLogEHVI', 'qlogehvi_mixed_seed': 'qLogEHVI (A0\')',
}
OPT_LABEL = {'random': 'Random', 'parego': 'ParEGO', 'qlogehvi_mixed': 'qLogEHVI'}
OPTIMIZER_ORDER = ['random', 'parego', 'qlogehvi_mixed']

# --- Load data ---
overall   = pd.read_csv(os.path.join(DATA_DIR, 'paper_metrics_overall.csv'))
per_run   = pd.read_csv(os.path.join(DATA_DIR, 'paper_metrics_per_run.csv'))
per_model = pd.read_csv(os.path.join(DATA_DIR, 'paper_metrics_per_model.csv'))
paired    = pd.read_csv(os.path.join(DATA_DIR, 'paper_metrics_paired.csv'))
curves    = pd.read_csv(os.path.join(DATA_DIR, 'paper_metrics_curves.csv'))
paired_t  = pd.read_csv(os.path.join(DATA_DIR, 'paper_metrics_paired_tests.csv'))
model_t   = pd.read_csv(os.path.join(DATA_DIR, 'paper_metrics_model_level_tests.csv'))

# --- Helpers ---
def mean_ci(x, ci=95):
    m = np.mean(x); n = len(x)
    if n < 5: return m, m, m
    bs = np.array([np.mean(np.random.choice(x, size=n, replace=True)) for _ in range(10000)])
    lo = np.percentile(bs, (100-ci)/2)
    hi = np.percentile(bs, 100-(100-ci)/2)
    return m, lo, hi

def set_grid(ax, axis='y'):
    ax.grid(True, axis=axis, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

# ============================================================
# Figure 2: Agent runnable rate + ablation
# ============================================================
def fig2_agent_ablation():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={'width_ratios': [1, 1.5]})

    # Left: runnable rate by category
    categories = ['Industrial\n(10/10)', 'Basic\n(6/6)', 'Topology\n(4/4)', 'Overall\n(20/20)']
    rates = [100, 100, 100, 100]
    cis_lo = [72.2, 60.7, 47.3, 86.1]  # Wilson CI lower bounds
    cis_hi = [100, 100, 100, 100]

    colors_cat = ['#2c3e50', '#34495e', '#2c3e50', '#1a5276']
    ax1.bar(range(4), rates, color=colors_cat, edgecolor='white', linewidth=0.8, width=0.6)
    ax1.errorbar(range(4), rates, yerr=[np.array(rates)-np.array(cis_lo), np.array(cis_hi)-np.array(rates)],
                 fmt='none', ecolor='black', capsize=4, capthick=1.2, linewidth=1.2)
    ax1.set_xticks(range(4))
    ax1.set_xticklabels(categories, fontsize=8)
    ax1.set_ylabel('Runnable Rate (%)', fontsize=11)
    ax1.set_ylim(0, 115)
    ax1.axhline(y=60, color='red', linestyle='--', linewidth=1, alpha=0.6, label='Go/No-Go threshold (60%)')
    ax1.legend(fontsize=8, loc='lower right')
    ax1.set_title('(a) Runnable Rate by Category', fontsize=12, fontweight='bold')
    set_grid(ax1)

    # Right: ablation
    ablations = ['Full', '−RAG', '−Subagent', '−Skill', '−Budget']
    ablation_rates = [100, 100, 100, 80, 0]
    delta_pp = [0, 0, 0, -20, -100]
    colors_abl = ['#1a5276', '#7f8c8d', '#7f8c8d', '#e74c3c', '#c0392b']

    ax2.bar(range(5), ablation_rates, color=colors_abl, edgecolor='white', linewidth=0.8, width=0.6)
    ax2.set_xticks(range(5))
    ax2.set_xticklabels(ablations, fontsize=9)
    ax2.set_ylabel('Runnable Rate (%)', fontsize=11)
    ax2.set_ylim(0, 115)

    for i, (rate, delta) in enumerate(zip(ablation_rates, delta_pp)):
        if delta == 0 and i > 0:
            ax2.annotate('Δ = 0 pp', (i, rate + 2), ha='center', fontsize=8, color='#555')
        elif delta < 0:
            ax2.annotate(f'Δ = {delta} pp', (i, rate + 2), ha='center', fontsize=8, color='#c0392b', fontweight='bold')
    ax2.set_title('(b) Ablation Analysis', fontsize=12, fontweight='bold')
    set_grid(ax2)

    fig.suptitle('Figure 2: Domain-Coding Agent — Runnable Rate and Ablation', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    for ext in ['png', 'pdf']:
        fig.savefig(os.path.join(OUT_DIR, f'fig2_agent_ablation.{ext}'), facecolor='white')
    plt.close()
    print("  ✓ fig2_agent_ablation")

# ============================================================
# Figure 3: Three-optimizer evaluation (20 models)
# ============================================================
def fig3_optimizer_evaluation():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    # Panel (a): HV trajectories
    ax = axes[0]
    for policy in OPTIMIZER_ORDER:
        pc = curves[curves['policy'] == policy]
        g = pc.groupby('round')['hv']
        r = g.mean().index.values
        m = g.mean().values
        s = g.std().values
        n = g.count().values
        se = s / np.sqrt(n)
        color = POLICY_COLORS[policy]
        label = POLICY_LABELS[policy].replace(' (A0\')', '')
        ax.plot(r, m, color=color, linewidth=2, label=label)
        ax.fill_between(r, m - 1.96*se, m + 1.96*se, color=color, alpha=0.12)
    ax.set_xlabel('Evaluation Round', fontsize=11)
    ax.set_ylabel('Hypervolume', fontsize=11)
    ax.set_title('(a) Cumulative HV Trajectories', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, framealpha=0.9)
    ax.set_xlim(0, 20)
    set_grid(ax)

    # Panel (b): Per-model ΔHV-AUC (qLogEHVI vs baselines)
    ax = axes[1]
    # Compute per-model mean HV-AUC and then delta
    model_hv = per_run.groupby(['model_id', 'policy'])['hv_auc'].mean().reset_index()
    deltas_vs_random = []
    deltas_vs_parego = []
    for mid in model_hv['model_id'].unique():
        mh = model_hv[model_hv['model_id'] == mid].set_index('policy')
        qlog = mh.loc['qlogehvi_mixed', 'hv_auc']
        rnd  = mh.loc['random', 'hv_auc']
        par  = mh.loc['parego', 'hv_auc']
        deltas_vs_random.append(qlog - rnd)
        deltas_vs_parego.append(qlog - par)

    baselines = [('vs Random', deltas_vs_random, C_RANDOM, 0),
                 ('vs ParEGO', deltas_vs_parego, C_PAREGO, 1)]
    for label, deltas, color, pos in baselines:
        jitter = np.random.RandomState(42).uniform(-0.12, 0.12, len(deltas))
        ax.scatter(np.full(len(deltas), pos) + jitter, deltas, alpha=0.5, s=20, color=color,
                   edgecolors='white', linewidth=0.3)
        m, lo, hi = mean_ci(np.array(deltas))
        ax.errorbar(pos, m, yerr=[[m-lo], [hi-m]], fmt='o', color='black', capsize=6,
                    capthick=2, markersize=10, linewidth=2, zorder=10)
        # Get p-value from paired_tests
        opt_data = paired_t[(paired_t['optimizer'] == 'qlogehvi_mixed') & (paired_t['metric'] == 'delta_hv_auc')]
        # Actually, model-level comparison uses model-level tests
        # Use the Wilcoxon model-level test results from the analysis
        if pos == 0:  # vs Random
            p_str = 'p < 0.0001'  # from analysis
        else:
            p_str = 'p = 0.033'  # from analysis
        ax.annotate(p_str, (pos, m + (hi-m) + 0.005), ha='center', fontsize=9,
                    fontweight='bold', color='#1a5276')

    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['vs Random', 'vs ParEGO'], fontsize=10)
    ax.set_ylabel('ΔHV-AUC (qLogEHVI − Baseline)', fontsize=11)
    ax.set_title('(b) Per-Model ΔHV-AUC', fontsize=12, fontweight='bold')
    ax.set_xlim(-0.5, 1.5)
    set_grid(ax)

    # Panel (c): Win/loss counts
    ax = axes[2]
    wins = [19, 13]
    losses = [1, 7]
    x = np.arange(2)
    width = 0.35
    ax.bar(x - width/2, wins, width, color='#27ae60', edgecolor='white', label='qLogEHVI better')
    ax.bar(x + width/2, losses, width, color='#e74c3c', edgecolor='white', label='Baseline better')
    ax.set_xticks(x)
    ax.set_xticklabels(['vs Random', 'vs ParEGO'], fontsize=10)
    ax.set_ylabel('Number of Models (out of 20)', fontsize=11)
    ax.set_title('(c) Model-Level Win/Loss', fontsize=12, fontweight='bold')
    ax.legend(fontsize=8)
    for i, (w, l) in enumerate(zip(wins, losses)):
        ax.text(i - width/2, w + 0.3, str(w), ha='center', fontsize=10, fontweight='bold')
        ax.text(i + width/2, l + 0.3, str(l), ha='center', fontsize=10, fontweight='bold')
    set_grid(ax)

    fig.suptitle('Figure 3: Mixed-Variable MOBO — 20-Model Evaluation', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    for ext in ['png', 'pdf']:
        fig.savefig(os.path.join(OUT_DIR, f'fig3_optimizer_evaluation.{ext}'), facecolor='white')
    plt.close()
    print("  ✓ fig3_optimizer_evaluation")

# ============================================================
# Figure 4: AISW Forest Plot + Budget-Node Effects
# ============================================================
def fig4_aisw_forest():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={'width_ratios': [1.5, 1]})

    # Panel (a): Forest plot (model-cluster inference)
    ax = ax1
    mt = model_t[model_t['metric'] == 'delta_hv_auc_mean']

    optimizers = ['random', 'parego', 'qlogehvi_mixed']
    opt_labels = ['Random', 'ParEGO', 'qLogEHVI']
    colors_opt = [C_RANDOM, C_PAREGO, C_QLOGEHVI]
    y_positions = [2.5, 1.5, 0.5]

    x_min, x_max = 0, 0
    for i, (opt, label, color, y) in enumerate(zip(optimizers, opt_labels, colors_opt, y_positions)):
        row = mt[mt['optimizer'] == opt]
        if len(row) == 0: continue
        row = row.iloc[0]
        mean_val = row['mean']
        ci_lo = row['ci95_low']
        ci_hi = row['ci95_high']
        p_holm = row['p_holm']

        ax.errorbar(mean_val, y, xerr=[[mean_val-ci_lo], [ci_hi-mean_val]], fmt='o', color=color,
                    capsize=6, capthick=2, markersize=12, linewidth=2.5, zorder=10)
        ax.plot([ci_lo, ci_hi], [y, y], color=color, linewidth=3, alpha=0.7)

        p_str = f'Holm p = {p_holm:.3f}'
        ax.annotate(f'{label}\n{mean_val:+.5f}  {p_str}', (ci_hi + 0.002, y),
                    fontsize=10, va='center', color=color, fontweight='bold')
        x_min = min(x_min, ci_lo)
        x_max = max(x_max, ci_hi)

    ax.axvline(x=0, color='black', linestyle='-', linewidth=1.2)
    ax.set_xlabel('ΔHV-AUC (A0′ − A0)', fontsize=11)
    ax.set_yticks([])
    ax.set_title('(a) Model-Cluster Forest Plot', fontsize=12, fontweight='bold')
    ax.set_xlim(x_min - 0.005, x_max + 0.025)
    set_grid(ax)

    # Panel (b): Budget-node effects
    ax = ax2
    rounds = [5, 10, 20]
    for opt, label, color in zip(optimizers, opt_labels, colors_opt):
        pm_opt = per_model[per_model['optimizer'] == opt]
        vals = []
        for r in [5, 10, 20]:
            col = f'delta_hv_{r}_mean'
            if col in pm_opt.columns:
                vals.append(pm_opt[col].mean())
            else:
                vals.append(0)
        ax.plot(rounds, vals, 'o-', color=color, linewidth=2, markersize=8, label=label)

    ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.set_xlabel('Evaluation Round', fontsize=11)
    ax.set_ylabel('Mean ΔHV (A0′ − A0)', fontsize=11)
    ax.set_title('(b) Budget-Node Effects', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xticks(rounds)
    set_grid(ax)

    fig.suptitle('Figure 4: AISW Boundary Characterization', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    for ext in ['png', 'pdf']:
        fig.savefig(os.path.join(OUT_DIR, f'fig4_aisw_forest.{ext}'), facecolor='white')
    plt.close()
    print("  ✓ fig4_aisw_forest")

# ============================================================
# Figure 5: Model × Optimizer Heterogeneity Heatmap
# ============================================================
def fig5_heterogeneity():
    fig, ax = plt.subplots(figsize=(12, 6))

    optimizers = ['random', 'parego', 'qlogehvi_mixed']
    opt_labels = ['Random', 'ParEGO', 'qLogEHVI']

    pm = per_model.copy()
    model_means = pm.groupby('model_id')['delta_hv_auc_mean'].mean().sort_values()
    model_order = model_means.index.tolist()

    matrix = np.zeros((len(model_order), 3))
    for i, model in enumerate(model_order):
        for j, opt in enumerate(optimizers):
            row = pm[(pm['model_id'] == model) & (pm['optimizer'] == opt)]
            if len(row) > 0:
                matrix[i, j] = row['delta_hv_auc_mean'].values[0]

    vmax = max(abs(matrix.min()), abs(matrix.max()), 0.001)
    im = ax.imshow(matrix, cmap='RdBu_r', aspect='auto', vmin=-vmax, vmax=vmax)

    ax.set_xticks(range(3))
    ax.set_xticklabels(opt_labels, fontsize=10)
    ax.set_yticks(range(len(model_order)))
    ax.set_yticklabels(model_order, fontsize=7, fontfamily='monospace')

    for i in range(len(model_order)):
        for j in range(3):
            val = matrix[i, j]
            text_color = 'white' if abs(val) > vmax * 0.5 else 'black'
            ax.text(j, i, f'{val:+.4f}', ha='center', va='center', fontsize=7,
                    color=text_color, fontweight='bold')

    cbar = plt.colorbar(im, ax=ax, shrink=0.85)
    cbar.set_label('ΔHV-AUC (A0′ − A0)', fontsize=10)

    ax.set_title('Figure 5: Model × Optimizer Heterogeneity of AISW Effect', fontsize=13, fontweight='bold')
    plt.tight_layout()
    for ext in ['png', 'pdf']:
        fig.savefig(os.path.join(OUT_DIR, f'fig5_heterogeneity.{ext}'), facecolor='white')
    plt.close()
    print("  ✓ fig5_heterogeneity")

# ============================================================
# Figure 6: Feasibility and Timing
# ============================================================
def fig6_feasibility_timing():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    policies = ['random', 'random_seed', 'parego', 'parego_seed', 'qlogehvi_mixed', 'qlogehvi_mixed_seed']
    labels = ['Random\nA0', 'Random\nA0′', 'ParEGO\nA0', 'ParEGO\nA0′', 'qLogEHVI\nA0', 'qLogEHVI\nA0′']
    colors = [C_RANDOM, C_RANDOM, C_PAREGO, C_PAREGO, C_QLOGEHVI, C_QLOGEHVI]
    hatches = ['', '//', '', '//', '', '//']

    ov = overall.set_index('policy')

    # Feasibility
    ax = ax1
    valid_rates = [ov.loc[p, 'valid_rate_mean'] * 100 for p in policies]
    invalid_trials = [int(ov.loc[p, 'invalid_trials_total']) for p in policies]

    x = np.arange(len(policies))
    bars = ax.bar(x, valid_rates, color=colors, edgecolor='black', linewidth=0.8, width=0.6)
    for bar, hatch in zip(bars, hatches):
        if hatch: bar.set_hatch(hatch)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('Feasibility Rate (%)', fontsize=11)
    ax.set_ylim(90, 100.5)
    ax.set_title('(a) Mesh Feasibility Rate', fontsize=12, fontweight='bold')
    for i, (rate, inv) in enumerate(zip(valid_rates, invalid_trials)):
        ax.annotate(f'{rate:.1f}%\n({inv} invalid)', (i, rate + 0.1), ha='center', fontsize=7, va='bottom')
    set_grid(ax)

    # Timing
    ax = ax2
    wall_times = [ov.loc[p, 'wall_seconds_mean'] for p in policies]
    wall_sds = [ov.loc[p, 'wall_seconds_sd'] for p in policies]

    bars = ax.bar(x, wall_times, color=colors, edgecolor='black', linewidth=0.8, width=0.6,
                  yerr=wall_sds, capsize=3, error_kw={'linewidth': 1})
    for bar, hatch in zip(bars, hatches):
        if hatch: bar.set_hatch(hatch)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('Mean Wall Time (s)', fontsize=11)
    ax.set_title('(b) Mean Cumulative Wall Time per Run', fontsize=12, fontweight='bold')
    for i, (t, sd) in enumerate(zip(wall_times, wall_sds)):
        ax.annotate(f'{t:.0f}s', (i, t + sd + 2), ha='center', fontsize=7)
    set_grid(ax)

    fig.suptitle('Figure 6: Feasibility and Computational Cost', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    for ext in ['png', 'pdf']:
        fig.savefig(os.path.join(OUT_DIR, f'fig6_feasibility_timing.{ext}'), facecolor='white')
    plt.close()
    print("  ✓ fig6_feasibility_timing")

# ============================================================
# Figure 7: Budget-Node Dynamics — qLogEHVI Detail
# ============================================================
def fig7_budget_dynamics():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Panel (a): qLogEHVI ΔHV per round
    ax = ax1
    qc = curves[curves['policy'].isin(['qlogehvi_mixed', 'qlogehvi_mixed_seed'])]
    hv_a0  = qc[qc['policy'] == 'qlogehvi_mixed'].groupby('round')['hv'].mean()
    hv_a0p = qc[qc['policy'] == 'qlogehvi_mixed_seed'].groupby('round')['hv'].mean()
    rounds = hv_a0.index.values
    delta_hv = (hv_a0p - hv_a0).values

    colors_delta = ['#e74c3c' if d < 0 else '#27ae60' for d in delta_hv]
    ax.bar(rounds, delta_hv, color=colors_delta, edgecolor='white', linewidth=0.5, width=0.7)
    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.set_xlabel('Evaluation Round', fontsize=11)
    ax.set_ylabel('ΔHV (A0′ − A0)', fontsize=11)
    ax.set_title('(a) qLogEHVI: Per-Round ΔHV', fontsize=12, fontweight='bold')
    set_grid(ax)

    # Panel (b): Convergence comparison
    ax = ax2
    for policy, color, label, ls in [
        ('qlogehvi_mixed', C_A0, 'qLogEHVI A0', '-'),
        ('qlogehvi_mixed_seed', C_A0PRIME, 'qLogEHVI A0′', '--')]:
        pc = curves[curves['policy'] == policy]
        hv_mean = pc.groupby('round')['hv'].mean()
        ax.plot(hv_mean.index, hv_mean.values, color=color, linewidth=2, linestyle=ls, label=label)

    ax.axvspan(0, 4, alpha=0.08, color='gray', label='Warmup (rounds 1–4)')
    ax.axvspan(4, 20, alpha=0.04, color='blue', label='BO (rounds 5–20)')
    ax.set_xlabel('Evaluation Round', fontsize=11)
    ax.set_ylabel('Mean Hypervolume', fontsize=11)
    ax.set_title('(b) qLogEHVI: A0 vs A0′ Convergence', fontsize=12, fontweight='bold')
    ax.legend(fontsize=8, ncol=2)
    set_grid(ax)

    fig.suptitle('Figure 7: Budget-Node Dynamics — qLogEHVI Detail', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    for ext in ['png', 'pdf']:
        fig.savefig(os.path.join(OUT_DIR, f'fig7_budget_dynamics.{ext}'), facecolor='white')
    plt.close()
    print("  ✓ fig7_budget_dynamics")

# ============================================================
# Figure 8: Per-Category Analysis
# ============================================================
def fig8_category_analysis():
    fig, ax = plt.subplots(figsize=(10, 5))

    def get_category(mid):
        if mid.startswith('i'): return 'Industrial'
        elif mid.startswith('s'): return 'Basic'
        elif mid.startswith('n'): return 'Topology'
        return 'Unknown'

    per_run_copy = per_run.copy()
    per_run_copy['category'] = per_run_copy['model_id'].apply(get_category)

    categories = ['Industrial', 'Basic', 'Topology']
    optimizers = ['random', 'parego', 'qlogehvi_mixed']
    opt_labels = ['Random', 'ParEGO', 'qLogEHVI']
    colors = [C_RANDOM, C_PAREGO, C_QLOGEHVI]

    x = np.arange(len(categories))
    width = 0.25

    for i, (opt, label, color) in enumerate(zip(optimizers, opt_labels, colors)):
        means, sems = [], []
        for cat in categories:
            cat_data = per_run_copy[(per_run_copy['category'] == cat) & (per_run_copy['policy'] == opt)]['hv_auc']
            means.append(cat_data.mean())
            sems.append(cat_data.std() / np.sqrt(len(cat_data)))
        ax.bar(x + i*width, means, width, color=color, label=label, edgecolor='white', linewidth=0.5)
        ax.errorbar(x + i*width, means, yerr=sems, fmt='none', ecolor='black', capsize=3, linewidth=1)

    ax.set_xticks(x + width)
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylabel('HV-AUC', fontsize=11)
    ax.set_title('Figure 8: HV-AUC by Geometry Category', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    set_grid(ax)

    plt.tight_layout()
    for ext in ['png', 'pdf']:
        fig.savefig(os.path.join(OUT_DIR, f'fig8_category_analysis.{ext}'), facecolor='white')
    plt.close()
    print("  ✓ fig8_category_analysis")

# ============================================================
# Tables (LaTeX format)
# ============================================================
def generate_tables():
    ov = overall.set_index('policy')

    # Table 1: Overall optimizer performance
    t1 = r"""\begin{table}[htbp]
\centering
\caption{Overall optimizer performance (20 models $\times$ 3 seeds, mean $\pm$ SD).}
\label{tab:overall}
\begin{tabular}{lcccc}
\toprule
Policy & HV-AUC & Final HV & Final IGD & Feasibility (\%) \\
\midrule
"""
    for policy in ['random', 'parego', 'qlogehvi_mixed']:
        row = ov.loc[policy]
        label = OPT_LABEL[policy]
        t1 += f"{label} & {row['hv_auc_mean']:.4f} $\\pm$ {row['hv_auc_sd']:.4f} & {row['hv_final_mean']:.4f} $\\pm$ {row['hv_final_sd']:.4f} & {row['igd_final_mean']:.4f} $\\pm$ {row['igd_final_sd']:.4f} & {row['valid_rate_mean']*100:.1f} \\\\\n"
    t1 += r"""\bottomrule
\end{tabular}
\end{table}
"""

    # Table 2: AISW effects (model-cluster inference)
    mt = model_t[model_t['metric'] == 'delta_hv_auc_mean']
    t2 = r"""\begin{table}[htbp]
\centering
\caption{AISW effect on HV-AUC (20 models, model-cluster sign-flip permutation with Holm correction).}
\label{tab:aisw}
\begin{tabular}{lccccc}
\toprule
Optimizer & Mean $\Delta$HV-AUC & Bootstrap 95\% CI & Raw $p$ & Holm $p$ & Wins/Ties/Losses \\
\midrule
"""
    for opt in ['random', 'parego', 'qlogehvi_mixed']:
        row = mt[mt['optimizer'] == opt]
        if len(row) == 0: continue
        row = row.iloc[0]
        label = OPT_LABEL[opt]
        t2 += f"{label} & {row['mean']:+.5f} & [{row['ci95_low']:+.4f}, {row['ci95_high']:+.4f}] & {row['p_value']:.3f} & {row['p_holm']:.3f} & {int(row['wins'])}/{int(row['ties'])}/{int(row['losses'])} \\\\\n"
    t2 += r"""\bottomrule
\end{tabular}
\end{table}
"""

    # Table 3: Budget-node dynamics
    t3 = r"""\begin{table}[htbp]
\centering
\caption{Budget-node dynamics of AISW effect ($\Delta$HV = A0$'$ $-$ A0).}
\label{tab:budget}
\begin{tabular}{lccc}
\toprule
Round & Random $\Delta$HV & ParEGO $\Delta$HV & qLogEHVI $\Delta$HV \\
\midrule
"""
    for r in [5, 10, 20]:
        col = f'delta_hv_{r}_mean'
        vals = []
        for opt in ['random', 'parego', 'qlogehvi_mixed']:
            pm_opt = per_model[per_model['optimizer'] == opt]
            vals.append(pm_opt[col].mean() if col in pm_opt.columns else 0)
        t3 += f"Round {r} & {vals[0]:+.5f} & {vals[1]:+.5f} & {vals[2]:+.5f} \\\\\n"
    t3 += r"""\bottomrule
\end{tabular}
\end{table}
"""

    # Table 4: Ablation
    t4 = r"""\begin{table}[htbp]
\centering
\caption{Agent ablation: runnable rate and contribution of each component.}
\label{tab:ablation}
\begin{tabular}{lcccl}
\toprule
Configuration & Runnable Rate & $\Delta$ vs Full & Interpretation \\
\midrule
Full & 100\% & -- & Baseline \\
$-$RAG & 100\% & 0 pp & Retrieval not needed for runnability \\
$-$Subagent & 100\% & 0 pp & Sub-agents not needed for runnability \\
$-$Skill & 80\% & $-$20 pp & \textbf{Domain skill necessary} \\
$-$Budget & 0\% & $-$100 pp & \textbf{Iterative budget necessary and sufficient} \\
\bottomrule
\end{tabular}
\end{table}
"""

    # Table 5: Pairwise statistical tests (qLogEHVI vs baselines)
    t5 = r"""\begin{table}[htbp]
\centering
\caption{Pairwise statistical tests: qLogEHVI vs baselines (model-level Wilcoxon signed-rank, N=20 models).}
\label{tab:pairwise}
\begin{tabular}{lcccc}
\toprule
Comparison & Mean $\Delta$HV-AUC & Wilcoxon $W$ & Raw $p$ & Significant? \\
\midrule
"""
    # These are from the paper analysis - hardcoded from results
    t5 += r"qLogEHVI vs Random & +0.0232 & -- & $3.8\times10^{-6}$ & Yes \\" + "\n"
    t5 += r"qLogEHVI vs ParEGO & +0.0068 & -- & 0.033 & Yes \\" + "\n"
    t5 += r"ParEGO vs Random & +0.0164 & -- & -- & -- \\" + "\n"
    t5 += r"""\bottomrule
\end{tabular}
\end{table}
"""

    tables = [('table1_overall', t1), ('table2_aisw', t2), ('table3_budget', t3),
              ('table4_ablation', t4), ('table5_pairwise', t5)]
    for name, tex in tables:
        with open(os.path.join(OUT_DIR, f'{name}.tex'), 'w', encoding='utf-8') as f:
            f.write(tex)
    print(f"  ✓ Generated {len(tables)} LaTeX tables")

# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("Generating figures for AEinfo paper (20-model experiment)...\n")
    fig2_agent_ablation()
    fig3_optimizer_evaluation()
    fig4_aisw_forest()
    fig5_heterogeneity()
    fig6_feasibility_timing()
    fig7_budget_dynamics()
    fig8_category_analysis()
    generate_tables()
    print(f"\nAll done! Figures saved to: {OUT_DIR}")