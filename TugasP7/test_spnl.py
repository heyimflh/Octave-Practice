"""
Unit Test dan Verifikasi Acceptance Criteria PRD.md (TC-01 sampai TC-09)
untuk Program SPNL (spnl.py).
"""

import os
import unittest
from spnl import (
    PROBLEMS,
    bisection,
    regula_falsi,
    f1_residual,
    f1_original,
    f2_residual,
    f3_residual,
    scan_graphic_roots,
    plot_single_graph,
    plot_double_graph,
    run_all_problems
)


class TestSPNL(unittest.TestCase):

    def test_tc01_transformation_problem_1(self):
        """TC-01: Transformasi persamaan soal 1 (residual f1(x) = 3x^3 - 5x^2 + 4x - 8)."""
        # Pada x = 1: 3(1) - 5(1) + 4(1) - 8 = -6
        self.assertEqual(f1_residual(1.0), -6.0)
        # Pada x = 2: 3(8) - 5(4) + 4(2) - 8 = 24 - 20 + 8 - 8 = 4
        self.assertEqual(f1_residual(2.0), 4.0)
        # f1_original(1.0) harus 3(1) - 5(1) + 4(1) - 7 = -5
        self.assertEqual(f1_original(1.0), -5.0)

    def test_tc02_target_graphic_problem_1(self):
        """TC-02: Target grafik soal 1 memiliki kurva asli dan target y = 1."""
        prob1 = PROBLEMS[1]
        self.assertEqual(prob1.single_target_val, 1.0)
        self.assertEqual(prob1.double_func2(1.0), 1.0)
        self.assertEqual(prob1.double_func2(2.5), 1.0)

    def test_tc03_multiple_intervals_problem_2(self):
        """TC-03: Soal 2 memproses interval terpisah dan memvalidasi masing-masing."""
        prob2 = PROBLEMS[2]
        # Interval valid: [-1, 0]
        res_valid = bisection(prob2.func, -1.0, 0.0, tol=1e-4, max_iter=20)
        self.assertTrue(res_valid.converged)
        self.assertIsNotNone(res_valid.root)
        self.assertAlmostEqual(res_valid.root, -0.703467, places=3)

        # Interval lain yang tidak mengurung akar: [1, 2]
        res_invalid = bisection(prob2.func, 1.0, 2.0, tol=1e-4, max_iter=20)
        self.assertFalse(res_invalid.converged)
        self.assertIn("TIDAK MENGURUNG AKAR", res_invalid.stopping_reason)

    def test_tc04_domain_problem_3(self):
        """TC-04: Domain Soal 3 (x > -2) menolak x <= -2."""
        prob3 = PROBLEMS[3]
        # Evaluasi langsung x = -2 harus raise ValueError
        with self.assertRaises(ValueError):
            f3_residual(-2.0)
        with self.assertRaises(ValueError):
            f3_residual(-2.5)

        # Metode numerik dengan batas <= -2 harus ditolak
        res = bisection(prob3.func, -3.0, 0.0, tol=1e-4, max_iter=20,
                        domain_validator=prob3.domain_validator)
        self.assertFalse(res.converged)
        self.assertIn("domain", res.stopping_reason.lower())

    def test_tc05_interval_not_bracketing_root(self):
        """TC-05: Interval tidak mengurung akar (f(a) * f(b) > 0) ditolak."""
        # Pada f1, interval [2, 3] bernilai f1(2)=4 > 0, f1(3)=40 > 0
        res = bisection(f1_residual, 2.0, 3.0, tol=1e-4, max_iter=20)
        self.assertFalse(res.converged)
        self.assertIn("TIDAK MENGURUNG AKAR", res.stopping_reason)

        res_rf = regula_falsi(f1_residual, 2.0, 3.0, tol=1e-4, max_iter=20)
        self.assertFalse(res_rf.converged)
        self.assertIn("TIDAK MENGURUNG AKAR", res_rf.stopping_reason)

    def test_tc06_max_iterations(self):
        """TC-06: Iterasi tidak pernah melebihi 20."""
        for pid in [1, 2, 3]:
            prob = PROBLEMS[pid]
            a, b = prob.default_intervals[0]
            res_bi = bisection(prob.func, a, b, tol=1e-4, max_iter=20, domain_validator=prob.domain_validator)
            res_rf = regula_falsi(prob.func, a, b, tol=1e-4, max_iter=20, domain_validator=prob.domain_validator)
            self.assertLessEqual(res_bi.iterations, 20)
            self.assertLessEqual(res_rf.iterations, 20)

    def test_tc07_tolerance_and_convergence(self):
        """TC-07: Status konvergen tercapai dan toleransi <= 0.0001."""
        for pid in [1, 2, 3]:
            prob = PROBLEMS[pid]
            a, b = prob.default_intervals[0]
            res_bi = bisection(prob.func, a, b, tol=1e-4, max_iter=20, domain_validator=prob.domain_validator)
            res_rf = regula_falsi(prob.func, a, b, tol=1e-4, max_iter=20, domain_validator=prob.domain_validator)

            self.assertTrue(res_bi.converged)
            self.assertTrue(res_rf.converged)
            self.assertIsNotNone(res_bi.root)
            self.assertIsNotNone(res_rf.root)

            # Verifikasi nilai fungsi pada akar mendekati nol atau error selisih < tol
            self.assertTrue((res_bi.final_error is not None and res_bi.final_error < 1e-4) or abs(res_bi.f_root) < 1e-4)
            self.assertTrue((res_rf.final_error is not None and res_rf.final_error < 1e-4) or abs(res_rf.f_root) < 1e-4)

    def test_tc08_graphics_generation(self):
        """TC-08: Menghasilkan grafik tunggal dan ganda untuk ketiga soal."""
        for pid in [1, 2, 3]:
            prob = PROBLEMS[pid]
            single_path = f"test_soal{pid}_tunggal.png"
            double_path = f"test_soal{pid}_ganda.png"

            plot_single_graph(prob, estimated_root=1.0, save_path=single_path, show_plot=False)
            plot_double_graph(prob, estimated_root=1.0, save_path=double_path, show_plot=False)

            self.assertTrue(os.path.exists(single_path))
            self.assertTrue(os.path.exists(double_path))

            # Bersihkan file uji sementara
            os.remove(single_path)
            os.remove(double_path)

    def test_tc09_run_all_problems(self):
        """TC-09: Jalankan seluruh soal tanpa error."""
        run_all_problems(show_plots=False)
        self.assertTrue(os.path.exists("grafik_semua_soal.png"))


if __name__ == "__main__":
    unittest.main()
