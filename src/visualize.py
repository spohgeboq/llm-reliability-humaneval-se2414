import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics_file", type=str, default="results/task_level_metrics.csv")
    parser.add_argument("--output_dir", type=str, default="results/figures")
    return parser.parse_args()


def plot_fig1(df: pd.DataFrame, output_path: str):
    s42 = df[df["seed"] == 42]
    tiers = ["Easy", "Medium", "Hard"]
    conditions = ["baseline1", "baseline2", "proposed"]
    cond_names = ["B1: Flash-Lite (Zero-Shot)", "B2: 3.5-Lite (Zero-Shot)", "P3: 3.5-Lite (Proposed CoT)"]
    colors = ["#4A90E2", "#50E3C2", "#F5A623"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    x = np.arange(len(tiers))
    width = 0.25

    for idx, (cond, name, color) in enumerate(zip(conditions, cond_names, colors)):
        pass_rates = []
        errors = []
        for tier in tiers:
            sub = s42[(s42["condition"] == cond) & (s42["complexity_tier"] == tier)]["passed"]
            rate = sub.mean() * 100.0
            pass_rates.append(rate)
            err = np.sqrt((rate * (100.0 - rate)) / len(sub)) if len(sub) > 0 else 0.0
            errors.append(err * 1.96)

        offset = (idx - 1) * width
        bars = ax1.bar(x + offset, pass_rates, width, yerr=errors, capsize=4, label=name, color=color, edgecolor="#333333", alpha=0.9)
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f"{height:.1f}%",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 5), textcoords="offset points",
                         ha="center", va="bottom", fontsize=8, fontweight="bold")

    ax1.set_title("A. Functional Correctness (Pass@1) by Complexity Tier", fontsize=12, fontweight="bold", pad=12)
    ax1.set_xlabel("Algorithmic Cyclomatic Complexity Tier", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Pass@1 Correctness Rate (%)", fontsize=11, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(["Easy\n(CC ≤ 3, n=62)", "Medium\n(4 ≤ CC ≤ 6, n=68)", "Hard\n(CC ≥ 7, n=34)"], fontsize=10)
    ax1.set_ylim(0, 115)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right", frameon=True, fontsize=9)

    for idx, (cond, name, color) in enumerate(zip(conditions, cond_names, colors)):
        exp_means = []
        exp_errs = []
        for tier in tiers:
            sub = s42[(s42["condition"] == cond) & (s42["complexity_tier"] == tier)]["explanation_score"]
            exp_means.append(sub.mean())
            exp_errs.append(sub.std() / np.sqrt(len(sub)) * 1.96 if len(sub) > 1 else 0.0)

        offset = (idx - 1) * width
        bars = ax2.bar(x + offset, exp_means, width, yerr=exp_errs, capsize=4, label=name, color=color, edgecolor="#333333", alpha=0.9)
        for bar in bars:
            height = bar.get_height()
            ax2.annotate(f"{height:.2f}",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 5), textcoords="offset points",
                         ha="center", va="bottom", fontsize=8, fontweight="bold")

    ax2.set_title("B. Explanatory Accuracy (1–5 Rubric) by Complexity Tier", fontsize=12, fontweight="bold", pad=12)
    ax2.set_xlabel("Algorithmic Cyclomatic Complexity Tier", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Explanatory Accuracy Score (1 to 5)", fontsize=11, fontweight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(["Easy\n(CC ≤ 3, n=62)", "Medium\n(4 ≤ CC ≤ 6, n=68)", "Hard\n(CC ≥ 7, n=34)"], fontsize=10)
    ax2.set_ylim(1.0, 5.5)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    ax2.legend(loc="lower right", frameon=True, fontsize=9)

    plt.suptitle("Figure 1: Benchmark Comparison Across Model Conditions and Algorithmic Difficulty Tiers (HumanEval, N=164)", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_fig2(df: pd.DataFrame, output_path: str):
    s42 = df[df["seed"] == 42]
    conditions = ["baseline1", "baseline2", "proposed"]
    cond_labels = ["B1: Flash-Lite\n(Zero-Shot)", "B2: 3.5-Lite\n(Zero-Shot)", "P3: 3.5-Lite\n(Proposed CoT)"]

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    plot_data = []
    positions = []
    colors_list = []
    labels = []

    pos = 1
    for cond, label in zip(conditions, cond_labels):
        sub_pass = s42[(s42["condition"] == cond) & (s42["passed"] == 1)]["latency_seconds"].values
        sub_fail = s42[(s42["condition"] == cond) & (s42["passed"] == 0)]["latency_seconds"].values

        plot_data.append(sub_pass)
        positions.append(pos)
        colors_list.append("#4CAF50")
        labels.append(f"{label}\n[Passed]")

        plot_data.append(sub_fail)
        positions.append(pos + 0.8)
        colors_list.append("#E53935")
        labels.append(f"{label}\n[Failed]")

        pos += 2.2

    bplot = ax.boxplot(plot_data, positions=positions, widths=0.55, patch_artist=True,
                       showmeans=True, meanline=True,
                       boxprops=dict(linewidth=1.2),
                       medianprops=dict(color="black", linewidth=2.0),
                       meanprops=dict(color="blue", linewidth=1.8, linestyle="--"))

    for patch, color in zip(bplot['boxes'], colors_list):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)

    for idx, (d, p) in enumerate(zip(plot_data, positions)):
        med = np.median(d)
        ax.annotate(f"med={med:.2f}s", xy=(p, med), xytext=(0, 10),
                    textcoords="offset points", ha="center", fontsize=8, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8))

    ax.set_title("Figure 2: API Generation Latency Distribution by Execution Outcome (Passed vs Failed)", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Per-Task Generation Latency (seconds)", fontsize=11, fontweight="bold")
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=9, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    import matplotlib.patches as mpatches
    pass_patch = mpatches.Patch(color='#4CAF50', label='Passed Unit Tests')
    fail_patch = mpatches.Patch(color='#E53935', label='Failed Unit Tests (Divergence/Hang)')
    ax.legend(handles=[pass_patch, fail_patch], loc="upper left", frameon=True, fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    df = pd.read_csv(args.metrics_file)

    fig1_path = os.path.join(args.output_dir, "fig1_model_comparison.png")
    fig2_path = os.path.join(args.output_dir, "fig2_latency_vs_correctness.png")

    plot_fig1(df, fig1_path)
    plot_fig2(df, fig2_path)


if __name__ == "__main__":
    main()
