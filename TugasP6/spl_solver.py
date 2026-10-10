import time

def gauss_elimination(A, b):
    n = len(A)
    Ac = [row[:] for row in A]
    bc = b[:]
    
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(Ac[k][i]) > abs(Ac[max_row][i]):
                max_row = k
        
        if Ac[max_row][i] == 0:
            raise ValueError("Pivot nol terdeteksi.")
            
        if max_row != i:
            Ac[i], Ac[max_row] = Ac[max_row], Ac[i]
            bc[i], bc[max_row] = bc[max_row], bc[i]
            
        for k in range(i+1, n):
            factor = Ac[k][i] / Ac[i][i]
            for j in range(i, n):
                Ac[k][j] -= factor * Ac[i][j]
            bc[k] -= factor * bc[i]
            
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        s = bc[i]
        for j in range(i+1, n):
            s -= Ac[i][j] * x[j]
        x[i] = s / Ac[i][i]
    return x

def gauss_jordan(A, b):
    n = len(A)
    Ac = [row[:] for row in A]
    bc = b[:]
    
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(Ac[k][i]) > abs(Ac[max_row][i]):
                max_row = k
                
        if Ac[max_row][i] == 0:
            raise ValueError("Pivot nol terdeteksi.")
            
        if max_row != i:
            Ac[i], Ac[max_row] = Ac[max_row], Ac[i]
            bc[i], bc[max_row] = bc[max_row], bc[i]
            
        pivot = Ac[i][i]
        for j in range(i, n):
            Ac[i][j] /= pivot
        bc[i] /= pivot
        
        for k in range(n):
            if k != i:
                factor = Ac[k][i]
                for j in range(i, n):
                    Ac[k][j] -= factor * Ac[i][j]
                bc[k] -= factor * bc[i]
    return bc

def lu_decomposition_solve(A, b):
    n = len(A)
    Ac = [row[:] for row in A]
    bc = b[:]
    P = list(range(n))
    
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(Ac[k][i]) > abs(Ac[max_row][i]):
                max_row = k
                
        if Ac[max_row][i] == 0:
            raise ValueError("Pivot nol terdeteksi.")
            
        if max_row != i:
            Ac[i], Ac[max_row] = Ac[max_row], Ac[i]
            P[i], P[max_row] = P[max_row], P[i]
            
        for k in range(i+1, n):
            Ac[k][i] /= Ac[i][i]
            for j in range(i+1, n):
                Ac[k][j] -= Ac[k][i] * Ac[i][j]
                
    Pb = [bc[P[i]] for i in range(n)]
    y = [0.0] * n
    for i in range(n):
        s = Pb[i]
        for j in range(i):
            s -= Ac[i][j] * y[j]
        y[i] = s
        
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        s = y[i]
        for j in range(i+1, n):
            s -= Ac[i][j] * x[j]
        x[i] = s / Ac[i][i]
    return x

def jacobi(A, b, x0, tol, max_iter):
    n = len(A)
    x = x0[:]
    x_new = [0.0] * n
    
    for iteration in range(1, max_iter + 1):
        max_diff = 0.0
        for i in range(n):
            if A[i][i] == 0:
                raise ValueError("Diagonal utama nol terdeteksi.")
            s = b[i]
            for j in range(n):
                if i != j:
                    s -= A[i][j] * x[j]
            x_new[i] = s / A[i][i]
            max_diff = max(max_diff, abs(x_new[i] - x[i]))
            
        x = x_new[:]
        if max_diff <= tol:
            return x, iteration, "Konvergen"
            
    return x, max_iter, "Belum konvergen"

def gauss_seidel(A, b, x0, tol, max_iter):
    n = len(A)
    x = x0[:]
    
    for iteration in range(1, max_iter + 1):
        max_diff = 0.0
        for i in range(n):
            if A[i][i] == 0:
                raise ValueError("Diagonal utama nol terdeteksi.")
            s = b[i]
            for j in range(n):
                if i != j:
                    s -= A[i][j] * x[j]
            new_val = s / A[i][i]
            max_diff = max(max_diff, abs(new_val - x[i]))
            x[i] = new_val
            
        if max_diff <= tol:
            return x, iteration, "Konvergen"
            
    return x, max_iter, "Belum konvergen"

def benchmark(func, args, reps=1000):
    for _ in range(10):
        func(*args)
    start = time.perf_counter()
    for _ in range(reps):
        func(*args)
    end = time.perf_counter()
    return (end - start) / reps * 1_000_000

def main():
    A = [
        [ 5, -1, -1,  0,  0],
        [-1,  5, -1, -1,  0],
        [-1, -1,  4, -1, -1],
        [ 0,  0,  1,  4, -2],
        [ 0,  1, -1,  1,  4]
    ]
    b = [-1, 2, 6, 2, -1]
    exact = [55/169, 422/507, 70/39, 7/169, -10/507]
    x0 = [0.0] * 5
    tol = 0.001
    max_iter = 20

    sol_g = gauss_elimination(A, b)
    sol_gj = gauss_jordan(A, b)
    sol_lu = lu_decomposition_solve(A, b)
    sol_jac, it_jac, st_jac = jacobi(A, b, x0, tol, max_iter)
    sol_gs, it_gs, st_gs = gauss_seidel(A, b, x0, tol, max_iter)

    err_g = [abs(e - s) for e, s in zip(exact, sol_g)]
    err_gj = [abs(e - s) for e, s in zip(exact, sol_gj)]
    err_lu = [abs(e - s) for e, s in zip(exact, sol_lu)]
    err_jac = [abs(e - s) for e, s in zip(exact, sol_jac)]
    err_gs = [abs(e - s) for e, s in zip(exact, sol_gs)]

    reps = 1000
    t_g = benchmark(gauss_elimination, (A, b), reps)
    t_gj = benchmark(gauss_jordan, (A, b), reps)
    t_lu = benchmark(lu_decomposition_solve, (A, b), reps)
    t_jac = benchmark(jacobi, (A, b, x0, tol, max_iter), reps)
    t_gs = benchmark(gauss_seidel, (A, b, x0, tol, max_iter), reps)

    print("=" * 105)
    print("Bagian A - Solusi SPL")
    print("-" * 105)
    print(f"{'Metode':<15} | {'p':<12} | {'q':<12} | {'r':<12} | {'s':<12} | {'t':<12} | {'Iterasi & Status'}")
    print("-" * 105)
    
    def fmt(sol):
        return " | ".join(f"{v:12.6f}" for v in sol)
        
    print(f"{'Gauss':<15} | {fmt(sol_g)} | - (Langsung)")
    print(f"{'Gauss-Jordan':<15} | {fmt(sol_gj)} | - (Langsung)")
    print(f"{'LU':<15} | {fmt(sol_lu)} | - (Langsung)")
    print(f"{'Jacobi':<15} | {fmt(sol_jac)} | {it_jac} ({st_jac})")
    print(f"{'Gauss-Seidel':<15} | {fmt(sol_gs)} | {it_gs} ({st_gs})")

    print("\n" + "=" * 115)
    print("Bagian B - Galat Absolut")
    print("-" * 115)
    print(f"{'Metode':<15} | {'Galat p':<12} | {'Galat q':<12} | {'Galat r':<12} | {'Galat s':<12} | {'Galat t':<12} | {'Maksimum'}")
    print("-" * 115)
    
    def fmte(err):
        return " | ".join(f"{v:12.2e}" for v in err)
        
    print(f"{'Gauss':<15} | {fmte(err_g)} | {max(err_g):12.2e}")
    print(f"{'Gauss-Jordan':<15} | {fmte(err_gj)} | {max(err_gj):12.2e}")
    print(f"{'LU':<15} | {fmte(err_lu)} | {max(err_lu):12.2e}")
    print(f"{'Jacobi':<15} | {fmte(err_jac)} | {max(err_jac):12.2e}")
    print(f"{'Gauss-Seidel':<15} | {fmte(err_gs)} | {max(err_gs):12.2e}")

    print("\n" + "=" * 80)
    print("Bagian C - Running Time")
    print("-" * 80)
    print(f"{'Metode':<15} | {'Rata-rata Waktu (us)':<25} | {'Pengulangan'}")
    print("-" * 80)
    print(f"{'Gauss':<15} | {t_g:<25.2f} | {reps}")
    print(f"{'Gauss-Jordan':<15} | {t_gj:<25.2f} | {reps}")
    print(f"{'LU':<15} | {t_lu:<25.2f} | {reps}")
    print(f"{'Jacobi':<15} | {t_jac:<25.2f} | {reps}")
    print(f"{'Gauss-Seidel':<15} | {t_gs:<25.2f} | {reps}")
    print("=" * 80)

if __name__ == '__main__':
    main()
