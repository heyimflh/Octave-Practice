import math
import unittest

from ode.problem import DEFAULT_B, DEFAULT_N, DEFAULT_X0, DEFAULT_Y0, f, validate_inputs, y_exact
from ode.methods import euler, heun, rk4
from ode.errors import absolute_error, relative_error, relative_error_percent


class TestODESolver(unittest.TestCase):

    def test_t01_y_exact_initial(self):
        self.assertAlmostEqual(y_exact(0.0), 1.0, places=12)

    def test_t02_y_exact_target(self):
        expected = -2.0 + math.sqrt(37.0)
        self.assertAlmostEqual(y_exact(2.0), expected, places=12)

    def test_t03_f_initial(self):
        expected = (4.0 * 0.0 - 2.0 * 0.0 + 1.0) / (2.0 + 1.0)
        self.assertAlmostEqual(f(0.0, 1.0), expected, places=12)
        self.assertAlmostEqual(f(0.0, 1.0), 1.0 / 3.0, places=12)

    def test_t04_euler_single_step(self):
        h = 2.0 / 15.0
        expected_y1 = 1.0 + h * (1.0 / 3.0)
        res = euler(f, 0.0, 1.0, 2.0, 15)
        self.assertAlmostEqual(res[1]["y"], expected_y1, places=12)
        self.assertAlmostEqual(res[0]["k1"], 1.0 / 3.0, places=12)

    def test_t05_reference_values_euler(self):
        res = euler(f, DEFAULT_X0, DEFAULT_Y0, DEFAULT_B, DEFAULT_N)
        y_approx = res[-1]["y"]
        err_abs = absolute_error(y_exact(DEFAULT_B), y_approx)
        err_rel = relative_error(y_exact(DEFAULT_B), y_approx)

        ref_y = 3.873691938989
        ref_err_abs = 0.209070591309
        ref_err_rel = 0.051208119443

        self.assertAlmostEqual(y_approx, ref_y, places=9)
        self.assertAlmostEqual(err_abs, ref_err_abs, places=9)
        self.assertAlmostEqual(err_rel, ref_err_rel, places=9)

    def test_t05_reference_values_heun(self):
        res = heun(f, DEFAULT_X0, DEFAULT_Y0, DEFAULT_B, DEFAULT_N)
        y_approx = res[-1]["y"]
        err_abs = absolute_error(y_exact(DEFAULT_B), y_approx)
        err_rel = relative_error(y_exact(DEFAULT_B), y_approx)

        ref_y = 4.095311545562
        ref_err_abs = 0.012549015264
        ref_err_rel = 0.003073657890

        self.assertAlmostEqual(y_approx, ref_y, places=9)
        self.assertAlmostEqual(err_abs, ref_err_abs, places=9)
        self.assertAlmostEqual(err_rel, ref_err_rel, places=9)

    def test_t05_reference_values_rk4(self):
        res = rk4(f, DEFAULT_X0, DEFAULT_Y0, DEFAULT_B, DEFAULT_N)
        y_approx = res[-1]["y"]
        err_abs = absolute_error(y_exact(DEFAULT_B), y_approx)
        err_rel = relative_error(y_exact(DEFAULT_B), y_approx)

        ref_y = 4.082773474080
        ref_err_abs = 1.0944e-05
        ref_err_rel = 2.6805e-06

        self.assertAlmostEqual(y_approx, ref_y, places=9)
        self.assertAlmostEqual(err_abs, ref_err_abs, delta=1e-8)
        self.assertAlmostEqual(err_rel, ref_err_rel, delta=1e-8)

    def test_t05_error_order_pattern(self):
        res_euler = euler(f, DEFAULT_X0, DEFAULT_Y0, DEFAULT_B, DEFAULT_N)
        res_heun = heun(f, DEFAULT_X0, DEFAULT_Y0, DEFAULT_B, DEFAULT_N)
        res_rk4 = rk4(f, DEFAULT_X0, DEFAULT_Y0, DEFAULT_B, DEFAULT_N)

        exact_val = y_exact(DEFAULT_B)
        err_euler = absolute_error(exact_val, res_euler[-1]["y"])
        err_heun = absolute_error(exact_val, res_heun[-1]["y"])
        err_rk4 = absolute_error(exact_val, res_rk4[-1]["y"])

        self.assertGreater(err_euler, err_heun)
        self.assertGreater(err_heun, err_rk4)

    def test_t06_error_functions(self):
        exact = 4.0
        approx = 3.8
        self.assertAlmostEqual(absolute_error(exact, approx), 0.2, places=12)
        self.assertAlmostEqual(relative_error(exact, approx), 0.05, places=12)
        self.assertAlmostEqual(relative_error_percent(exact, approx), 5.0, places=12)

        self.assertEqual(relative_error(0.0, 0.0), 0.0)
        self.assertEqual(relative_error(0.0, 1.0), float("inf"))

    def test_t07_iteration_length_and_endpoint(self):
        for solver in [euler, heun, rk4]:
            res = solver(f, DEFAULT_X0, DEFAULT_Y0, DEFAULT_B, DEFAULT_N)
            self.assertEqual(len(res), DEFAULT_N + 1)
            self.assertEqual(res[0]["i"], 0)
            self.assertEqual(res[-1]["i"], DEFAULT_N)
            self.assertAlmostEqual(res[0]["x"], 0.0, places=12)
            self.assertAlmostEqual(res[-1]["x"], 2.0, places=12)

    def test_t08_exact_satisfies_ode(self):
        eps = 1e-6
        for x_val in [0.2, 0.5, 1.0, 1.5, 1.8]:
            y_val = y_exact(x_val)
            dy_dx_numerical = (y_exact(x_val + eps) - y_exact(x_val - eps)) / (2.0 * eps)
            dy_dx_ode = f(x_val, y_val)
            self.assertAlmostEqual(dy_dx_numerical, dy_dx_ode, places=6)

    def test_t09_invalid_inputs(self):
        with self.assertRaises(ValueError):
            validate_inputs(0.0, 1.0, 2.0, 0)
        with self.assertRaises(ValueError):
            validate_inputs(0.0, 1.0, 2.0, -5)

        with self.assertRaises(ValueError):
            validate_inputs(1.0, 1.0, 1.0, 15)

        with self.assertRaises(ZeroDivisionError):
            validate_inputs(0.0, -2.0, 2.0, 15)

        with self.assertRaises(ZeroDivisionError):
            f(1.0, -2.0)

    def test_convergence_order(self):
        exact_b = y_exact(DEFAULT_B)
        ns = [15, 30, 60, 120]

        err_euler = []
        err_heun = []
        err_rk4 = []

        for n_val in ns:
            res_e = euler(f, DEFAULT_X0, DEFAULT_Y0, DEFAULT_B, n_val)
            res_h = heun(f, DEFAULT_X0, DEFAULT_Y0, DEFAULT_B, n_val)
            res_r = rk4(f, DEFAULT_X0, DEFAULT_Y0, DEFAULT_B, n_val)

            err_euler.append(absolute_error(exact_b, res_e[-1]["y"]))
            err_heun.append(absolute_error(exact_b, res_h[-1]["y"]))
            err_rk4.append(absolute_error(exact_b, res_r[-1]["y"]))

        ratio_e = err_euler[0] / err_euler[1]
        self.assertGreater(ratio_e, 1.8)
        self.assertLess(ratio_e, 2.3)

        ratio_h = err_heun[0] / err_heun[1]
        self.assertGreater(ratio_h, 3.5)
        self.assertLess(ratio_h, 4.5)

        ratio_r = err_rk4[0] / err_rk4[1]
        self.assertGreater(ratio_r, 14.0)
        self.assertLess(ratio_r, 18.0)


if __name__ == "__main__":
    unittest.main()
