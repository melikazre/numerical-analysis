# Lagrange and spline interpolation — Project 3, Part 1

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, lagrange
import sympy as sp
from pathlib import Path

# where plots get saved
results = Path(__file__).parent / "results"
results.mkdir(exist_ok=True)

# given data points
x_data = np.array([1, 2, 3, 4, 5, 6], dtype=float)
y_data = np.array([1, 3, 5, 8, 5, 2], dtype=float)


def get_lagrange_formula():
    """Build the exact Lagrange polynomial with sympy."""
    x = sp.Symbol("x")
    n = len(x_data)
    polynomial = 0

    for i in range(n):
        basis = y_data[i]
        for j in range(n):
            if i != j:
                basis *= (x - x_data[j]) / (x_data[i] - x_data[j])
        polynomial += basis

    return sp.expand(polynomial)


def show_spline_pieces():
    """Print each piece of the natural cubic spline."""
    spline = CubicSpline(x_data, y_data, bc_type="natural")
    pieces = []

    for i in range(len(x_data) - 1):
        a, b, c, d = spline.c[:, i]
        x_start = x_data[i]
        text = (
            f"S{i + 1}(x) = {a:.4f} + {b:.4f}(x-{x_start})"
            f" + {c:.4f}(x-{x_start})^2 + {d:.4f}(x-{x_start})^3"
        )
        pieces.append((x_start, x_data[i + 1], text))

    return pieces


def draw_plot():
    x_smooth = np.linspace(x_data[0], x_data[-1], 300)

    lagrange_curve = lagrange(x_data, y_data)(x_smooth)
    spline_curve = CubicSpline(x_data, y_data, bc_type="natural")(x_smooth)

    plt.figure(figsize=(10, 6))
    plt.plot(x_smooth, lagrange_curve, label="Lagrange", linewidth=2)
    plt.plot(x_smooth, spline_curve, "--", label="Cubic spline", linewidth=2)
    plt.scatter(x_data, y_data, color="crimson", s=70, zorder=5, label="Data points")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Lagrange vs cubic spline interpolation")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    chart_path = results / "interpolation_plot.png"
    plt.savefig(chart_path, dpi=150)
    plt.close()
    return chart_path


if __name__ == "__main__":
    print("Part 1 — Lagrange and spline interpolation\n")

    print("Data points:")
    for x, y in zip(x_data, y_data):
        print(f"  ({int(x)}, {int(y)})")

    formula = get_lagrange_formula()
    print("\nLagrange formula:")
    print(f"  L(x) = {formula}")

    print("\nSpline pieces:")
    for start, end, piece in show_spline_pieces():
        print(f"  interval [{int(start)}, {int(end)}]: {piece}")

    saved = draw_plot()
    print(f"\nPlot saved to: {saved}")
