import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy import integrate
from pathlib import Path

results = Path(__file__).parent / "results"
results.mkdir(exist_ok=True)


def f(x):
    return np.exp(x ** 2)


def trapezoid_rule(start, end, pieces=1000):
    x = np.linspace(start, end, pieces + 1)
    y = f(x)
    step = (end - start) / pieces
    return step * (0.5 * y[0] + y[1:-1].sum() + 0.5 * y[-1])


def simpson_rule(start, end, pieces=1000):
    if pieces % 2 == 1:
        pieces += 1

    x = np.linspace(start, end, pieces + 1)
    y = f(x)
    step = (end - start) / pieces
    return step / 3 * (
        y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-2:2].sum()
    )


def gauss_quadrature(start, end, points=10):
    nodes, weights = leggauss(points)
    mapped_x = 0.5 * (end - start) * nodes + 0.5 * (end + start)
    return 0.5 * (end - start) * (weights * f(mapped_x)).sum()


if __name__ == "__main__":
    start, end = 0.0, 1.0
    pieces = 1000

    print("Part 3 - integrating f(x) = e^(x^2) on (0, 1)\n")

    by_trapezoid = trapezoid_rule(start, end, pieces)
    by_simpson = simpson_rule(start, end, pieces)
    by_gauss = gauss_quadrature(start, end, points=10)
    reference, _ = integrate.quad(f, start, end)

    print(f"Trapezoidal (n={pieces}):  {by_trapezoid:.10f}")
    print(f"Simpson (n={pieces}):       {by_simpson:.10f}")
    print(f"Gauss (10 points):          {by_gauss:.10f}")
    print(f"Reference (scipy):          {reference:.10f}")

    print("\nError vs reference:")
    print(f"  trapezoidal: {abs(by_trapezoid - reference):.2e}")
    print(f"  simpson:     {abs(by_simpson - reference):.2e}")
    print(f"  gauss:       {abs(by_gauss - reference):.2e}")

    output_file = results / "integration_results.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Integral of e^(x^2) on [0, 1]\n")
        file.write("-" * 40 + "\n")
        file.write(f"Trapezoidal: {by_trapezoid:.10f}\n")
        file.write(f"Simpson:     {by_simpson:.10f}\n")
        file.write(f"Gauss:       {by_gauss:.10f}\n")
        file.write(f"Reference:   {reference:.10f}\n")

    print(f"\nResults saved to: {output_file}")
