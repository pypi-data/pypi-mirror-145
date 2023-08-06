# todo docstrings
import numpy as np
import sympy as sym
import stanpy as stp


def test_basics():
    # todo: docstring and tests

    EI = 32000  # kNm²
    GA = 20000  # kN
    l = 6
    NII = -1500  # kN

    s = {"EI": EI, "GA": GA, "N": NII}

    a_j, b_j = stp.bj_opt2_p89(l, return_aj=True, **s)

    np.testing.assert_allclose(a_j.flatten(), np.array([1.0, 6.0, 18.0, 36.0, 54.0, 64.8]), rtol=1e-5)
    np.testing.assert_allclose(
        b_j.flatten(), np.array([0.218348, 4.335036, 15.424609, 32.855297, 50.821054, 62.05547681]), rtol=1e-5
    )


def test_ex01():

    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp

    EI = 32000  # kNm²
    l = 6  # m
    q = 10  # kN/m

    s = {"EI": EI, "l": l, "q": q, "bc_i": {"w": 0, "M": 0}, "bc_k": {"w": 0, "M": 0, "H": 0}}

    x = np.sort(np.append(np.linspace(0, l, 100), 3))
    Fxa = stp.tr(s, x=x)
    # Z_a, Z_b = stp.solve_tr(Fxa[-1], **s)
    Z_a, Z_b = stp.tr_solver(s)
    Z_x = Fxa.dot(Z_a).round(10)

    wx = Z_x[:, 0]
    phix = Z_x[:, 1]
    Mx = Z_x[:, 2]
    Vx = Z_x[:, 3]

    np.testing.assert_allclose(wx[0], 0, rtol=1e-5)
    np.testing.assert_allclose(wx[-1], 0, rtol=1e-5)
    np.testing.assert_allclose(Mx[x == l / 2], 45, rtol=1e-5)
    np.testing.assert_allclose(Vx[0], 30, rtol=1e-5)
    np.testing.assert_allclose(Vx[-1], -30, rtol=1e-5)

    np.testing.assert_allclose(phix[0], 0.002813, atol=1e-6)
    np.testing.assert_allclose(phix[-1], -0.002813, atol=1e-6)

    # visual plotting test
    # scale = 0.5
    # fig, ax = plt.subplots(figsize=(12, 2.5))
    # stp.plot_system(ax, s, watermark_pos=1)
    # stp.plot_V(ax, x=x, Vx=Vx, annotate_x=[0, l / 2, l], fill_p="red", scale=scale, alpha=0.2)
    # stp.plot_hinged_support(ax, 0, 0)
    # stp.plot_roller_support(ax, l, 0)
    # ax.grid(linestyle=":")
    # ax.set_axisbelow(True)
    # ax.set_ylim(-0.8, 0.1)
    # ax.set_ylabel("M/Mmax*{}".format(scale))
    # ax.set_title("[M] = kNm")
    # plt.show()


def test_ex02():

    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp

    np.set_printoptions(precision=6)

    EI = 32000  # kNm²
    l = 6  # m
    P = 2  # kN

    s = {
        "EI": EI,
        "l": 6,
        "P1": (P, 2),
        "P2": (P + 1, 3),
        "P3": (P + 2, 4),
        "bc_i": {"w": 0, "M": 0},
        "bc_k": {"w": 0, "M": 0, "H": 0},
    }

    dx = 1e-8
    x = np.linspace(0, l, 500)
    annotation = np.array([0, 1, 2.5, 3.5, 5, l - dx, 2, 3, 4])
    x = np.sort(np.append(x, annotation))

    Fxa = stp.tr(s, x=x)
    Z_a, Z_b = stp.tr_solver(s)
    Z_x = Fxa.dot(Z_a).round(10)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    V_x = Z_x[:, 3]

    # check boundary conditions (todo test function for boundary conditions)
    np.testing.assert_allclose(w_x[0], 0, atol=1e-5)
    np.testing.assert_allclose(w_x[-1], 0, atol=1e-5)
    np.testing.assert_allclose(M_x[0], 0, atol=1e-5)
    np.testing.assert_allclose(M_x[-1], 0, atol=1e-5)

    np.testing.assert_allclose(V_x[0], 4.166670, rtol=1e-5)
    np.testing.assert_allclose(V_x[x == annotation[1]], 4.166670, rtol=1e-5)
    np.testing.assert_allclose(V_x[x == annotation[2]], 2.166670, rtol=1e-5)
    np.testing.assert_allclose(V_x[x == annotation[3]], -0.83333, rtol=1e-5)
    np.testing.assert_allclose(V_x[x == annotation[4]], -4.833330, rtol=1e-5)

    np.testing.assert_allclose(M_x[x == annotation[6]], 8.333333, rtol=1e-5)
    np.testing.assert_allclose(M_x[x == annotation[7]], 10.500000, rtol=1e-5)
    np.testing.assert_allclose(M_x[x == annotation[8]], 9.6666670, rtol=1e-5)

    np.testing.assert_allclose(phi_x[0], 0.000572, atol=1e-6)
    np.testing.assert_allclose(phi_x[-1], -0.000600, atol=1e-6)

    # visual plotting test
    # scale = 0.5
    # fig, ax = plt.subplots(figsize=(12, 4))
    # stp.plot_system(ax, s, watermark_pos=1)
    # stp.plot_R(ax, x=x, Rx=V_x, annotate_x=annotation[:6], fill_p="red", fill_n="blue", scale=scale, alpha=0.2)
    # stp.plot_hinged_support(ax, 0, 0)
    # stp.plot_roller_support(ax, l, 0)
    # ax.grid(linestyle=":")
    # ax.set_axisbelow(True)
    # ax.set_ylim(-1.2, 1.2)
    # ax.set_ylabel("V/Vmax*{}".format(scale))
    # ax.set_title("[V] = kN")
    # plt.show()


def test_ex02_02():
    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp

    EI = 32000  # kNm²
    l1 = l4 = 2  # m
    l2 = l3 = 1  # m
    P1, P2, P3 = 2, 3, 4  # kN

    s = {
        "EI": EI,
        "l": 6,
        "P1": (P1, 2),
        "P2": (P2, 3),
        "bc_i": {"w": 0, "M": 0},
        "bc_k": {"w": 0, "M": 0, "H": 0},
    }

    s1_start = {"EI": EI, "l": 2, "bc_i": {"w": 0, "M": 0}}
    s2_start = {"EI": EI, "l": 1, "P1": (P1, 0)}
    s3_start = {"EI": EI, "l": 3, "P2": (P2, 0), "bc_k": {"w": 0, "M": 0, "H": 0}}

    s1_end = {"EI": EI, "l": 2, "P1": (P1, 2), "bc_i": {"w": 0, "M": 0}}
    s2_end = {"EI": EI, "l": 1, "P2": (P2, 1)}
    s3_end = {"EI": EI, "l": 3, "bc_k": {"w": 0, "M": 0, "H": 0}}

    x = np.linspace(0, 6, 10)
    annotation = np.array([2.1])
    x = np.sort(np.append(x, annotation))

    Fxa_xstart = stp.tr(s1_start, s2_start, s3_start, x=x)
    Fxa_xend = stp.tr(s1_end, s2_end, s3_end, x=x)
    Fxa_single = stp.tr(s, x=x)

    np.testing.assert_allclose(Fxa_xstart, Fxa_single)
    np.testing.assert_allclose(Fxa_xend, Fxa_single)


def test_ex04():
    EI, GA = 32000, 20000  # kNm^2, kN
    l = 6  # m
    H = (10, l / 2)  # kN
    P = 1500
    q = 4
    w0 = 0.03
    x = np.array([l, l / 2])
    s = {
        "EI": EI,
        "GA": GA,
        "l": l,
        "N": -P,
        "q": q,
        "w_0": w0,
        "P": H,
        "bc_i": {"w": 0, "phi": 0},
        "bc_k": {"w": 0, "M": 0, "H": 0},
    }

    # gamma, K = gamma_K_function(N=s["N"], GA=s["GA"], EI=s["EI"], l=s["l"])
    gamma, K = stp.gamma_K_function(**s)
    np.testing.assert_allclose(gamma, 108.108 * 10**-2, rtol=1e-05)
    np.testing.assert_allclose(K, -506.757 * 10**-4, rtol=1e-05)

    gamma_star, K_star = stp.gamma_K_function(N=s["N"], GA=s["GA"], EI=s["EI"], l=s["l"] / 2)
    np.testing.assert_allclose(gamma_star, 108.108 * 10**-2, rtol=1e-05)
    np.testing.assert_allclose(K_star, -506.757 * 10**-4, rtol=1e-05)

    bj = stp.bj_opt2_p89(x, 4, **s)

    np.testing.assert_allclose(
        np.round(bj[0], 4),
        np.round(
            np.array(
                [
                    218.348 * 10**-3,
                    433.504 * 10**-2,
                    154.246 * 10**-1,
                    328.553 * 10**-1,
                    508.211 * 10**-1,
                ]
            ),
            4,
        ),
        rtol=1e-04,
    )
    np.testing.assert_allclose(
        np.round(bj[1], 4),
        np.round(
            np.array(
                [
                    780.496 * 10**-3,
                    277.71 * 10**-2,
                    433.155 * 10**-2,
                    439.849 * 10**-2,
                    332.411 * 10**-2,
                ]
            ),
            4,
        ),
        rtol=1e-04,
    )

    q_hat = stp.load_q_hat(**s)
    np.testing.assert_allclose(q_hat, np.array([14.0]))

    load_integral_Q_ql = stp.calc_load_integral_Q(x, **{"EI": EI, "GA": GA, "l": l, "N": -P, "q": q, "w_0": w0})
    np.testing.assert_allclose(
        load_integral_Q_ql[0, :],
        np.array(
            [
                1.23643081e-02,
                1.55396674e-02,
                -2.33453538e02,
                -6.5611350e01,
                1.00000000e00,
            ]
        ),
        rtol=1e-05,
    )

    load_integral_Q_P = stp.calc_load_integral_Q(x, **{"EI": EI, "GA": GA, "l": l, "N": -P, "P": H})
    np.testing.assert_allclose(
        load_integral_Q_P[0, :],
        np.array(
            [
                -1.51610423e-05,
                1.46336103e-03,
                -3.00227416e01,
                -8.43779292e00,
                1.00000000e00,
            ]
        ),
        rtol=1e-05,
    )

    load_integral_Q = stp.calc_load_integral_Q(x, **s)
    np.testing.assert_allclose(
        load_integral_Q[0, :],
        np.array([1.23491471e-02, 1.70030284e-02, -2.63476279e02, -7.40491e01, 1.00000000e00]),
        rtol=1e-05,
    )

    load_integral_R = stp.calc_load_integral_R(x, **s)
    np.testing.assert_allclose(
        load_integral_R[0, :],
        np.array(
            [
                -1.39203527e-02,
                1.36997902e-03,
                -1.22880529e02,
                -3.40000000e01,
                1.00000000e00,
            ]
        ),
        rtol=1e-05,
    )

    Fca = stp.tr_R(x=x[0], **s)
    Fca_sol = np.array(
        [
            [
                1,
                468.653 * 10**-2,
                -521.102 * 10**-6,
                -875.65 * 10**-6,
                -139.204 * 10**-4,
            ],
            [
                0,
                218.348 * 10**-3,
                -135.47 * 10**-6,
                -521.102 * 10**-6,
                136.998 * 10**-5,
            ],
            [0, 7029.79, 218.348 * 10**-3, 468.653 * 10**-2, -122.881],
            [0, 0, 0, 1, -34],
            [0, 0, 0, 0, 1],
        ]
    )

    np.testing.assert_allclose(stp.signif(Fca[0, :], 6), Fca_sol[0, :])
    np.testing.assert_allclose(stp.signif(Fca[1, :], 6), Fca_sol[1, :])
    np.testing.assert_allclose(stp.signif(Fca[2, :], 6), Fca_sol[2, :])
    np.testing.assert_allclose(stp.signif(Fca[3, :], 6), Fca_sol[3, :])
    np.testing.assert_allclose(stp.signif(Fca[4, :], 6), Fca_sol[4, :])

    Fba = stp.tr_R(x=x[1], **s)
    Fba_sol = np.array(
        [
            [
                1,
                300.227 * 10**-2,
                -146.336 * 10**-6,
                151.61 * 10**-8,
                -166.023 * 10**-5,
            ],
            [
                0,
                780.496 * 10**-3,
                -867.845 * 10**-7,
                -146.336 * 10**-6,
                -230.972 * 10**-5,
            ],
            [0, 4503.41, 780.496 * 10**-3, 300.227 * 10**-2, 2.45096505e01],
            [0, 0, 0, 1, -22],
            [0, 0, 0, 0, 1],
        ]
    )

    np.testing.assert_allclose(Fba[0, :], Fba_sol[0, :], rtol=1e-04)
    np.testing.assert_allclose(Fba[1, :], Fba_sol[1, :], rtol=1e-05)
    np.testing.assert_allclose(Fba[2, :], Fba_sol[2, :], rtol=1e-05)
    np.testing.assert_allclose(Fba[3, :], Fba_sol[3, :], rtol=1e-05)
    np.testing.assert_allclose(Fba[4, :], Fba_sol[4, :], rtol=1e-05)

    Za, Zc = stp.solve_tr(Fca, **s)
    Za, Zc = stp.tr_solver(s)

    np.testing.assert_allclose(Za, np.array([0, 0, -76.784, 29.797, 1]), rtol=1e-04)
    np.testing.assert_allclose(Zc, np.array([0, -37.555e-4, 0, -4.203, 1]), rtol=1e-04)


if __name__ == "__main__":
    pass
    # test_ex03()
    # test_ex04()
    # test_basics()
    # ex03()
    # ex01_01_step_by_step()
