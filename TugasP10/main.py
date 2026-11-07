import argparse
import os
import sys
from typing import Any, Dict, List

from ode.problem import (
    DEFAULT_B,
    DEFAULT_N,
    DEFAULT_PRECISION,
    DEFAULT_X0,
    DEFAULT_Y0,
    f,
    validate_inputs,
    y_exact,
)
from ode.methods import euler, heun, rk4
from ode.errors import absolute_error, relative_error, relative_error_percent
from ode.report import (
    export_iteration_csv,
    export_summary_csv,
    print_analysis,
    print_header,
    print_iteration_table,
    print_summary_table,
)
from ode.plotting import is_matplotlib_available, plot_comparison, plot_errors


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Program Penyelesaian Persamaan Diferensial Biasa (PDB) - Metode Numerik",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--n", type=int, default=DEFAULT_N, help="Jumlah langkah iterasi (sub-interval)")
    parser.add_argument("--x0", type=float, default=DEFAULT_X0, help="Titik awal integrasi x0")
    parser.add_argument("--y0", type=float, default=DEFAULT_Y0, help="Kondisi awal y(x0)")
    parser.add_argument("--b", type=float, default=DEFAULT_B, help="Titik target integrasi x = b")
    parser.add_argument("--precision", type=int, default=DEFAULT_PRECISION, help="Jumlah digit desimal tampilan")
    parser.add_argument("--output-dir", type=str, default="output", help="Direktori penyimpanan file keluaran")
    parser.add_argument("--no-plot", action="store_true", help="Lewati pembuatan berkas gambar grafik")
    parser.add_argument("--verify", action="store_true", help="Bandingkan dengan scipy.integrate.solve_ivp (jika terpasang)")

    return parser.parse_args()


def verify_with_scipy(x0: float, y0: float, b: float) -> None:
    try:
        import importlib
        scipy_integrate = importlib.import_module("scipy.integrate")
        solve_ivp = getattr(scipy_integrate, "solve_ivp")
    except ImportError:
        print("[VERIFIKASI SCIPY]: Pustaka 'scipy' tidak terpasang. Verifikasi silang dilewati.")
        return

    def odefunc(t, y_val):
        return f(t, y_val[0])

    sol = solve_ivp(odefunc, [x0, b], [y0], method="RK45", rtol=1e-12, atol=1e-12)
    y_scipy = float(sol.y[0][-1])
    print("------------------------- VERIFIKASI DENGAN SCIPY RK45 -------------------------")
    print(f"Hasil solve_ivp (RK45, toleransi 1e-12): y({b}) = {y_scipy:.12f}")
    print(f"Solusi Eksak Analitik                 : y({b}) = {y_exact(b):.12f}")
    print(f"Selisih Scipy vs Eksak                : {abs(y_exact(b) - y_scipy):.12e}")
    print("--------------------------------------------------------------------------------\n")


def main() -> int:
    args = parse_arguments()

    try:
        validate_inputs(args.x0, args.y0, args.b, args.n)
    except Exception as e:
        print(f"[ERROR VALIDASI]: {e}", file=sys.stderr)
        return 1

    h = (args.b - args.x0) / args.n

    print_header(args.x0, args.y0, args.b, args.n, h)

    y_target_exact = y_exact(args.b)

    iter_euler = euler(f, args.x0, args.y0, args.b, args.n)
    iter_heun = heun(f, args.x0, args.y0, args.b, args.n)
    iter_rk4 = rk4(f, args.x0, args.y0, args.b, args.n)

    print_iteration_table("Euler", iter_euler, y_exact, args.precision)
    print_iteration_table("Heun", iter_heun, y_exact, args.precision)
    print_iteration_table("Runge-Kutta Orde-4", iter_rk4, y_exact, args.precision)

    methods_results = [
        ("Euler", iter_euler[-1]["y"]),
        ("Heun", iter_heun[-1]["y"]),
        ("Runge-Kutta 4", iter_rk4[-1]["y"]),
    ]

    summary_data: List[Dict[str, Any]] = [
        {
            "method": "Eksak",
            "y_approx": y_target_exact,
            "err_abs": None,
            "err_rel": None,
            "err_rel_pct": None,
        }
    ]

    for name, y_approx in methods_results:
        err_abs = absolute_error(y_target_exact, y_approx)
        err_rel = relative_error(y_target_exact, y_approx)
        err_pct = relative_error_percent(y_target_exact, y_approx)
        summary_data.append({
            "method": name,
            "y_approx": y_approx,
            "err_abs": err_abs,
            "err_rel": err_rel,
            "err_rel_pct": err_pct,
        })

    print_summary_table(summary_data, args.b, args.precision)
    print_analysis(summary_data)

    if args.verify:
        verify_with_scipy(args.x0, args.y0, args.b)

    os.makedirs(args.output_dir, exist_ok=True)
    csv_summary_path = os.path.join(args.output_dir, "ringkasan.csv")
    csv_euler_path = os.path.join(args.output_dir, "iterasi_euler.csv")
    csv_heun_path = os.path.join(args.output_dir, "iterasi_heun.csv")
    csv_rk4_path = os.path.join(args.output_dir, "iterasi_rk4.csv")

    export_summary_csv(csv_summary_path, summary_data, args.b)
    export_iteration_csv(csv_euler_path, iter_euler, y_exact)
    export_iteration_csv(csv_heun_path, iter_heun, y_exact)
    export_iteration_csv(csv_rk4_path, iter_rk4, y_exact)
    print(f"[BERHASIL]: File CSV berhasil disimpan ke direktori '{args.output_dir}/'.")

    if not args.no_plot:
        plot_dict = {
            "Euler": iter_euler,
            "Heun": iter_heun,
            "Runge-Kutta 4": iter_rk4,
        }
        fig_comparison_path = os.path.join(args.output_dir, "grafik_perbandingan.png")
        fig_error_path = os.path.join(args.output_dir, "grafik_galat.png")

        c_ok = plot_comparison(y_exact, plot_dict, args.x0, args.b, fig_comparison_path)
        e_ok = plot_errors(y_exact, plot_dict, fig_error_path)
        if c_ok and e_ok:
            print(f"[BERHASIL]: Grafik visualisasi berhasil disimpan ke '{args.output_dir}/'.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
