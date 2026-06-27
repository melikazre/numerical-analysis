import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

here = Path(__file__).parent
excel_path = here / "runtime_data.xlsx"
results = here / "results"
results.mkdir(exist_ok=True)


def read_excel_file():
    table = pd.read_excel(excel_path)
    table.columns = [str(name).strip() for name in table.columns]
    table = table.dropna(how="all")
    table = table[table.iloc[:, 0].notna()]
    return table


def draw_bar_chart(table, size_column, algorithm_columns):
    labels = table[size_column].astype(str)
    positions = range(len(labels))
    bar_width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, col in enumerate(algorithm_columns):
        shift = (i - len(algorithm_columns) / 2 + 0.5) * bar_width
        ax.bar(
            [pos + shift for pos in positions],
            table[col],
            bar_width,
            label=col,
        )

    ax.set_xlabel("Data size")
    ax.set_ylabel("Run time")
    ax.set_title("Bar chart - algorithm run times")
    ax.set_xticks(list(positions))
    ax.set_xticklabels(labels, rotation=45)
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(results / "runtime_bar_chart.png", dpi=150)
    plt.close(fig)


def draw_line_chart(table, size_column, algorithm_columns):
    labels = table[size_column].astype(str)

    fig, ax = plt.subplots(figsize=(10, 6))
    for col in algorithm_columns:
        ax.plot(labels, table[col], marker="o", linewidth=2, label=col)

    ax.set_xlabel("Data size")
    ax.set_ylabel("Run time")
    ax.set_title("Line chart - how run time grows")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(results / "runtime_line_chart.png", dpi=150)
    plt.close(fig)


def draw_box_plot(table, algorithm_columns):
    values_per_algorithm = [table[col].dropna() for col in algorithm_columns]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.boxplot(values_per_algorithm, labels=algorithm_columns)
    ax.set_xlabel("Algorithm")
    ax.set_ylabel("Run time")
    ax.set_title("Box plot - spread of run times")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(results / "runtime_box_plot.png", dpi=150)
    plt.close(fig)


def average_alg2_between_100_and_600(table, algorithm_columns):
    size_column = table.columns[0]
    alg2_name = next(col for col in algorithm_columns if "2" in str(col))

    wanted_sizes = ["100KB", "200KB", "300KB", "400KB", "500KB", "600KB"]
    filtered = table[table[size_column].astype(str).isin(wanted_sizes)]
    times = filtered[alg2_name].tolist()
    mean_time = filtered[alg2_name].mean()

    return alg2_name, times, mean_time


if __name__ == "__main__":
    print("Part 2 - runtime analysis from Excel\n")

    table = read_excel_file()
    size_column = table.columns[0]
    algorithm_columns = [col for col in table.columns[1:] if str(col).strip()]

    print(f"File: {excel_path.name}")
    print(f"Rows: {len(table)}\n")
    print(table.to_string(index=False))

    draw_bar_chart(table, size_column, algorithm_columns)
    draw_line_chart(table, size_column, algorithm_columns)
    draw_box_plot(table, algorithm_columns)

    alg2_name, times, mean_time = average_alg2_between_100_and_600(
        table, algorithm_columns
    )

    print(f"\nAverage {alg2_name} for 100-600 KB:")
    print(f"  values: {times}")
    print(f"  mean:   {mean_time:.2f}")

    print("\nCharts saved:")
    print(f"  {results / 'runtime_bar_chart.png'}")
    print(f"  {results / 'runtime_line_chart.png'}")
    print(f"  {results / 'runtime_box_plot.png'}")
