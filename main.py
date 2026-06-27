from pathlib import Path
import runpy

here = Path(__file__).parent

scripts = [
    "lagrange_and_spline.py",
    "runtime_from_excel.py",
    "integrate_exp_square.py",
]

if __name__ == "__main__":
    for script in scripts:
        print("=" * 50)
        runpy.run_path(str(here / script), run_name="__main__")
