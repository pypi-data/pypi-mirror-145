import stanpy as stp
import numpy as np

# todo: define classes, parametrization


def test_gamma_K_function():
    EI = 32000  # kNm²
    GA = 20000  # kNm²
    l = 6  # m
    H = 10  # kN
    q = 4  # kN/m
    N = -1500  # kN
    w_0 = 0.03  # m

    s = {
        "EI": EI,
        "GA": GA,
        "l": l,
        "q": q,
        "P": (H, l / 2),
        "N": N,
        "w_0": w_0,
        "bc_i": {"w": 0, "phi": 0},
        "bc_k": {"w": 0, "M": 0, "H": 0},
    }

    gamma, K = stp.gamma_K_function(**s)

    np.testing.assert_allclose(gamma, 108.108e-2, atol=1e-5)
    np.testing.assert_allclose(K, -506.757e-4, atol=1e-5)


def test_bj_constant_function():
    pass


def test_load_integral_poly_compare_q_with_qd():
    import sympy as sym

    x = sym.Symbol("x")
    E = 3 * 10**7  # kN/m2
    b = 0.2  # m
    hi = 0.3  # m
    hk = 0.4  # m
    l = 3  # m
    hx = hi + (hk - hi) / l * x

    cs_props = stp.cs(b=b, h=hx)
    s = {"E": E, "cs": cs_props, "l": l, "q": 10}
    load_integral_Q_q = stp.calc_load_integral_Q_poly(x=[0, l / 2, l], **s)

    s = {"E": E, "cs": cs_props, "l": l, "q_d": (10, 0, l)}
    load_integral_Q_qd = stp.calc_load_integral_Q_poly(x=[0, l / 2, l], **s)

    np.testing.assert_allclose(load_integral_Q_q, load_integral_Q_qd)
    np.set_printoptions(precision=6)


if __name__ == "__main__":
    import stanpy as stp
    import sympy as sym

    x = sym.Symbol("x")
    E = 3 * 10**7  # kN/m2
    b = 0.2  # m
    hi = 0.3  # m
    hk = 0.4  # m
    l = 3  # m
    hx = hi + (hk - hi) / l * x

    cs_props = stp.cs(b=b, h=hx)
    s = {"E": E, "cs": cs_props, "l": l, "q": 10}

    Fik = stp.tr_Q_poly(**s)
