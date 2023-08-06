import numpy as np
import stanpy as stp
import matplotlib.pyplot as plt


def test_ex01():
    EI = 32000  # kN/m2
    l = 6  # m

    hinged_support = {"w": 0, "M": 0}
    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}

    s1 = {"EI": EI, "l": l, "bc_i": hinged_support, "bc_k": {"w": 0}, "q": 10}
    s2 = {"EI": EI, "l": l, "bc_k": roller_support}

    s = [s1, s2]

    x_annotate = np.array([l, 2 * l])
    x = np.sort(np.append(np.linspace(0, 2 * l, 1000), x_annotate))
    x, Z_x = stp.solve_system(s1, s2, x=x)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    V_x = Z_x[:, 3]

    # test boundary conditions
    np.testing.assert_allclose(w_x[0], 0)
    np.testing.assert_allclose(w_x[x == l], 0)
    np.testing.assert_allclose(w_x[-1], 0)
    np.testing.assert_allclose(M_x[0], 0)
    np.testing.assert_allclose(M_x[-1], 0)

    np.testing.assert_allclose(M_x[x == l], -22.5)
    np.testing.assert_allclose(V_x[0], 26.25)
    np.testing.assert_allclose(np.max(V_x[x == l]), 3.75)
    np.testing.assert_allclose(np.min(V_x[x == l]), -33.75)
    np.testing.assert_allclose(V_x[-1], 3.75)


def test_ex02():
    EI = 32000  # kN/m2
    P = 4  # kN
    l = 6  # m

    hinged_support = {"w": 0, "M": 0}
    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}

    s1 = {"EI": EI, "l": l, "bc_i": fixed_support, "bc_k": {"w": 0}, "q": 10, "P": (P, l / 2)}
    s2 = {"EI": EI, "l": l, "bc_k": roller_support}

    s = [s1, s2]

    x_annotate = np.array([l, 2 * l])
    x = np.sort(np.append(np.linspace(0, 2 * l, 1000), x_annotate))
    x, Z_x = stp.solve_system(s1, s2, x=x)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    V_x = Z_x[:, 3]

    # test boundary conditions
    np.testing.assert_allclose(stp.signif(w_x[0], 6), 0)
    np.testing.assert_allclose(stp.signif(w_x[x == l], 6), 0)
    np.testing.assert_allclose(stp.signif(w_x[-1], 6), 0)
    np.testing.assert_allclose(stp.signif(phi_x[0], 6), 0)
    np.testing.assert_allclose(stp.signif(M_x[-1], 6), 0)

    np.testing.assert_allclose(stp.signif(M_x[0], 6), -42.428600)
    np.testing.assert_allclose(stp.signif(np.max(M_x[x == l]), 6), -14.1429)
    np.testing.assert_allclose(stp.signif(V_x[0], 6), 36.71430)
    np.testing.assert_allclose(stp.signif(np.max(V_x[x == l]), 6), 2.357140)
    np.testing.assert_allclose(stp.signif(np.min(V_x[x == l]), 6), -27.285700)
    np.testing.assert_allclose(stp.signif(V_x[-1], 6), 2.357140)


def test_ex03():
    EI = 32000  # kN/m2
    P = 5  # kN
    q = 4  # kN/m
    l = 4  # m

    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}
    hinge = {"M": 0}

    s1 = {"EI": EI, "l": l, "bc_i": fixed_support, "bc_k": {"w": 0}}
    s2 = {"EI": EI, "l": l, "bc_k": hinge, "q": q}
    s3 = {"EI": EI, "l": l, "bc_k": roller_support, "P": (P, l / 2)}

    s = [s1, s2, s3]

    x_annotate = np.array([l, 2 * l, 5 * l / 2])
    x = np.sort(np.append(np.linspace(0, 3 * l, 1000), x_annotate))
    x, Z_x = stp.solve_system(*s, x=x)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    V_x = Z_x[:, 3]

    # test boundary conditions
    np.testing.assert_allclose(stp.signif(w_x[0], 6), 0)
    np.testing.assert_allclose(stp.signif(w_x[x == l], 6), 0)
    np.testing.assert_allclose(stp.signif(w_x[-1], 6), 0)
    np.testing.assert_allclose(stp.signif(M_x[l == 2 * l], 6), 0)
    np.testing.assert_allclose(stp.signif(phi_x[0], 6), 0)
    np.testing.assert_allclose(stp.signif(M_x[-1], 6), 0)

    np.testing.assert_allclose(stp.signif(M_x[0], 6), 21)
    np.testing.assert_allclose(stp.signif(M_x[x == l], 6), -42)
    np.testing.assert_allclose(stp.signif(M_x[x == 5 * l / 2], 6), 5)

    np.testing.assert_allclose(stp.signif(V_x[0], 6), -15.75)
    np.testing.assert_allclose(stp.signif(np.max(V_x[x == l]), 6), 18.50)
    np.testing.assert_allclose(stp.signif(np.min(V_x[x == l]), 6), -15.75)
    np.testing.assert_allclose(stp.signif(V_x[x == 2 * l], 6), 2.5)
    # np.testing.assert_allclose(stp.signif(np.max(V_x[x == 5 * l / 2]), 6), 2.5)
    np.testing.assert_allclose(stp.signif(np.min(V_x[x == 5 * l / 2]), 6), -2.5)
    np.testing.assert_allclose(stp.signif(np.min(V_x[x == 3 * l]), 6), -2.5)
    # np.testing.assert_allclose(stp.signif(np.max(M_x[x == l]), 6), -14.1429)
    # np.testing.assert_allclose(stp.signif(V_x[0], 6), 36.71430)
    # np.testing.assert_allclose(stp.signif(np.max(V_x[x == l]), 6), 2.357140)
    # np.testing.assert_allclose(stp.signif(np.min(V_x[x == l]), 6), -27.285700)
    # np.testing.assert_allclose(stp.signif(V_x[-1], 6), 2.357140)


if __name__ == "__main__":
    test_ex01()
