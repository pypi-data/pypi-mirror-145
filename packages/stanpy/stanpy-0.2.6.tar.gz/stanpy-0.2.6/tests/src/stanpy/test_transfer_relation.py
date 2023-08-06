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


def test_point_force():
    import sympy as sym
    import matplotlib.pyplot as plt

    E = 2.1e8 # kN/m2
    l1 = 10 # m
    l2 = 4 # m
    P = 10 # kN/m

    b = 0.2 # m
    ha = hb = 0.3 # m
    hc = 0.4 # m 
    xs = sym.symbols("x")
    hx1 = hb+(hc-hb)/l1*xs
    hx2 = hc-(hc-hb)/l2*xs
    cs1 = stp.cs(b=b, h=hx1)
    cs2 = stp.cs(b=b, h=hx2)

    fixed = {"w":0, "phi":0}
    hinged = {"w":0, "M":0, "H":0}

    s1 = {"E":E, "cs":cs1, "l":l1, "bc_i":hinged, "P1":(P, l1/2)}
    s2 = {"E":E, "cs":cs2, "l":l2, "bc_k":fixed, "P1":(P, l2/2)}

    s = [s1, s2]

    # fig, ax = plt.subplots(figsize=(12,5))
    # stp.plot_system(ax, *s, render=True)
    # stp.plot_load(ax, *s, offset=0.1)
    # ax.set_ylim(-1.5, 2)
    # ax.set_aspect("equal")
    # plt.show()

    x = np.linspace(0, l1+l2, 1000)
    x_annoation = [0,l1, l1+l2, (l1+l2)/2]
    x = np.sort(np.append(x, x_annoation))
    Za, Zc = stp.tr_solver(*s)
    print(Za, Zc)
    Fxx = stp.tr(*s, x=x)
    Zx = Fxx.dot(Za)

    # todo: validate results

    # Moment
    # fig, ax = plt.subplots(figsize=(12,5))
    # stp.plot_system(ax, *s)
    # stp.plot_solution(ax, x=x, y=Zx[:,2], annotate_x = [0,x[Zx[:,2]==np.max(Zx[:,2])], l1+l2],flip_y=True, fill_p="red", fill_n="blue", alpha=0.2)
    # ax.set_ylim(-1.5, 2)
    # plt.show()

    # Querkraft
    # fig, ax = plt.subplots(figsize=(12,5))
    # stp.plot_system(ax, *s)
    # stp.plot_solution(ax, x=x, y=Zx[:,3], annotate_x = [0, l1+l2], fill_p="red", fill_n="blue", alpha=0.2)
    # ax.set_ylim(-1.5, 2)
    # ax.set_aspect("equal")
    # plt.show()

    # Biegelinie
    # scale = 0.2
    # fig, ax = plt.subplots(figsize=(12, 5))
    # stp.plot_system(ax, *s, lw=1, linestyle=":", c="#111111")
    # stp.plot_solution(ax, x=x, y=Zx[:,0],annotate_x = [x[Zx[:,0]==np.max(Zx[:,0])]], scale=scale, linestyle="-", flip_y=True, lw=2, round=5)
    # ax.grid(linestyle=":")
    # ax.set_axisbelow(True)
    # ax.set_ylim(-1.5, 1.5)
    # plt.show()

def test_curvature_force():
    import sympy as sym
    import matplotlib.pyplot as plt

    E = 2.1e8 # kN/m2
    l1 = 6 # m
    l2 = 6 # m
    P = 10 # kN/m

    b = 0.2 # m
    xs = sym.symbols("x")
    hx1 = 13.6*(1+xs*0.2941-0.02451*xs**2)/100
    hx2 = 25.6*(1-0.01302*xs**2)/100
    cs1 = stp.cs(b=b, h=hx1, pow_series_trunc=10, l=l1)
    cs2 = stp.cs(b=b, h=hx2, pow_series_trunc=10, l=l2)

    fixed = {"w":0, "phi":0}
    hinged = {"w":0, "M":0, "H":0}

    s1 = {"E":E, "cs":cs1, "l":l1, "bc_i":hinged, "P1":(P, l1/2)}
    s2 = {"E":E, "cs":cs2, "l":l2, "bc_k":fixed, "P1":(P, l2/2)}

    s = [s1, s2]

    fig, ax = plt.subplots(figsize=(12,5))
    stp.plot_system(ax, *s, render=True)
    stp.plot_load(ax, *s, offset=0.1)
    ax.set_ylim(-1.5, 2)
    ax.set_aspect("equal")
    plt.show()

if __name__ == "__main__":
    test_curvature_force()
