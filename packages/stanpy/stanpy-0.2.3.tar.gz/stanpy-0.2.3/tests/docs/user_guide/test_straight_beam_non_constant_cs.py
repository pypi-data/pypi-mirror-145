# todo docstrings
import numpy as np
import sympy as sym
import stanpy as stp
import matplotlib.pyplot as plt


def signif(x, p):
    x = np.asarray(x)
    x_positive = np.where(np.isfinite(x) & (x != 0), np.abs(x), 10 ** (p - 1))
    mags = 10 ** (p - 1 - np.floor(np.log10(x_positive)))
    return np.round(x * mags) / mags


def test_ex01():
    x_sym = sym.Symbol("x")
    E = 3e7  # kN/m2
    b = 0.2  # m
    ha = hb = 0.3  # m
    hc = 0.4  # m
    l1 = 4  # m
    l2 = 3  # m
    hx = ha + (hc - hb) / l2 * x_sym

    cs_props1 = stp.cs(b=b, h=ha)
    s1 = {"E": E, "cs": cs_props1, "q": 10, "l": l1, "bc_i": {"w": 0, "M": 0, "H": 0}}

    cs_props2 = stp.cs(b=b, h=hx)
    s2 = {"E": E, "cs": cs_props2, "q": 10, "l": l2, "bc_k": {"w": 0, "phi": 0}}

    gamma, K = stp.gamma_K_function(**s2)

    bj2 = stp.bj_p119(K, l2, 2, 0, cs_props2["eta_y"])
    bj2s = stp.bj_p119(K, l2, 2, 1, cs_props2["eta_y"])
    bj3 = stp.bj_p119(K, l2, 3, 0, cs_props2["eta_y"])
    bj3s = stp.bj_p119(K, l2, 3, 1, cs_props2["eta_y"])
    bj4 = stp.bj_p119(K, l2, 4, 0, cs_props2["eta_y"])
    bj4s = stp.bj_p119(K, l2, 4, 1, cs_props2["eta_y"])

    bj = stp.bj(x=l2, **s2)
    bj_sol = np.array([[3.375, 2.905, 1.991], [1.969, 2.531, 2.344]])

    np.testing.assert_allclose(bj[0, 0, 2:5], np.array([bj2, bj3, bj4]))
    np.testing.assert_allclose(bj[0, 1, 2:5], np.array([bj2s, bj3s, bj4s]))
    np.testing.assert_allclose(signif(bj[0, :, 2:5], 4), bj_sol)

    x = np.linspace(0, l1 + l2, 500)
    Fxa = stp.tr(s1, s2, x=x)
    Za, Zc = stp.solve_tr(Fxa[-1], bc_i=s1["bc_i"], bc_k=s2["bc_k"])

    np.testing.assert_allclose(signif(Za, 5), np.array([0, 43.161e-4, 0, 24.292, 1]))
    np.testing.assert_allclose(signif(Zc, 5), np.array([0, 0, -74.954, -45.708, 1]))

    Z_x = Fxa.dot(Za).round(10)

    np.testing.assert_allclose(Z_x[-1], Zc)
    np.testing.assert_allclose(Z_x[0], Za)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    R_x = Z_x[:, 3]

    # scale = 0.5
    # fig, ax = plt.subplots(figsize=(12, 5))
    # stp.plot_system(ax, s1, s2)
    # stp.plot_M(ax, x=x, Mx=M_x, fill_p="red", fill_n="blue", scale=scale, alpha=0.2)
    # ax.grid(linestyle=":")
    # ax.set_axisbelow(True)
    # ax.set_ylim(-0.8, 0.8)
    # ax.set_ylabel("R/Rmax*{}".format(scale))
    # ax.set_title("[R] = kN")
    # plt.show()


def test_ex02():

    E = 21e7  # kN/m^2
    l1, l3 = 0.99, 0.99  # m
    l2 = 0.51  # m
    ha, hb, hd = 0.25, 0.25, 0.25  # m
    hc = 0.15  # m
    b = 0.2  # m
    t = 0.02  # m
    s = 0.015  # m
    q = 3.04  # kN/m
    P = 9.96  # kN
    Ag = b * t

    x_sym = sym.Symbol("x")

    hx2 = hb - (hb - hc) / l2 * x_sym
    hx3 = hc + (hd - hc) / l3 * x_sym

    b_vec = np.array([b, s, b])
    h1_vec = np.array([t, ha - t, t])
    h2_vec = np.array([t, hx2 - t, t])
    h3_vec = np.array([t, hx3 - t, t])

    cs_props1 = stp.cs(b=b_vec, h=h1_vec)
    s1 = {"E": E, "cs": cs_props1, "l": l1, "P": (P, l1), "bc_i": {"w": 0, "M": 0, "H": 0}}

    cs_props2 = stp.cs(b=b_vec, h=h2_vec)
    s2 = {"E": E, "cs": cs_props2, "q": q, "l": l2}

    cs_props3 = stp.cs(b=b_vec, h=h3_vec)
    s3 = {"E": E, "cs": cs_props3, "q": q, "l": l3, "bc_k": {"w": 0, "phi": 0}}

    np.set_printoptions(precision=6)

    np.testing.assert_allclose(cs_props1["I_y"], cs_props2["I_y"](0))
    np.testing.assert_allclose(cs_props2["I_y"](l2), cs_props3["I_y"](0))

    x_annotate = np.cumsum(np.array([0, l1, l2, l3]))
    x = np.linspace(0, l1 + l2 + l3, 500)
    x = np.sort(np.append(x, x_annotate))
    Fxa = stp.tr(s1, s2, s3, x=x)

    F_ba_sol = np.array(
        [
            [1, 0.99, -1.6612e-5, -5.4819e-6, 0],
            [0, 1, -3.356e-5, -1.6612e-5, 0],
            [0, 0, 1, 0.99, 0],
            [0, 0, 0, 1, -9.96],
            [0, 0, 0, 0, 1],
        ]
    )

    F_ba = stp.tr(s1)
    np.testing.assert_allclose(signif(F_ba, 5), F_ba_sol)

    F_cb_sol = np.array(
        [
            [1, 0.51, -6.235e-6, -1.2529e-6, 5.375e-7],
            [0, 1, -2.9715e-5, -8.9197e-6, 5.0102e-6],
            [0, 0, 1, 0.51, -0.39535],
            [0, 0, 0, 1, -1.5504],
            [0, 0, 0, 0, 1],
        ]
    )
    F_cb = stp.tr(s2)
    np.testing.assert_allclose(signif(F_cb, 5), F_cb_sol)

    F_dc_sol = np.array(
        [
            [1, 0.99, -3.3611e-5, -9.1645e-6, 6.1588e-6],
            [0, 1, -5.7682e-5, -2.3494e-5, 2.1424e-5],
            [0, 0, 1, 0.99, -1.4898],
            [0, 0, 0, 1, -3.0096],
            [0, 0, 0, 0, 1],
        ]
    )
    F_dc = stp.tr(s3)
    np.testing.assert_allclose(signif(F_dc, 5), F_dc_sol)

    F_dc_sol = np.array(
        [
            [1, 2.49, -0.00013622, -0.00013536, 0.00040159],
            [0, 1, -0.00012096, -0.00016497, 0.00070151],
            [0, 0, 1, 2.49, -18.36],
            [0, 0, 0, 1, -14.52],
            [0, 0, 0, 0, 1],
        ]
    )
    F_da = F_dc.dot(F_cb).dot(F_ba)
    np.testing.assert_allclose(signif(F_da, 5), F_dc_sol)
    np.testing.assert_allclose(signif(Fxa[-1], 5), F_dc_sol)
    Za, Zd = stp.solve_tr(Fxa[-1], bc_i=s1["bc_i"], bc_k=s3["bc_k"])
    Z_x = Fxa.dot(Za).round(10)

    np.testing.assert_allclose(signif(Z_x[-1], 5), signif(Zd, 5))
    np.testing.assert_allclose(signif(Z_x[0], 5), signif(Za, 5))


if __name__ == "__main__":
    test_ex01()
