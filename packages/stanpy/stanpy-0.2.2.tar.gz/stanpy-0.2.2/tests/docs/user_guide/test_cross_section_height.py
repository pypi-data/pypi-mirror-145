# todo: tests


def test_ex_01():

    import sympy as sym
    import stanpy as stp
    import matplotlib.pyplot as plt

    x = sym.Symbol("x")
    l = 4  # m
    b, ha, hb = 0.2, 0.3, 0.4  # m
    hx = ha + (hb - ha) / l * x  # m

    cs_props = stp.cs(b=b, h=hx)


def test_ex_02():

    import numpy as np
    import sympy as sym
    import stanpy as stp

    x = sym.Symbol("x")
    l = 4  # m
    s, t = 0.012, 0.02  # m
    b, ha, hb = 0.2, 0.3, 0.4  # m
    hx = ha + (hb - ha) / l * x  # m

    b_v = np.array([b, s, b])
    h_v = np.array([t, hx, t])
    zsi_v = np.array([t / 2, t + (hx - 2 * t) / 2, t + (hx - 2 * t) + t / 2])  # von OK

    cs_props = stp.cs(b=b_v, h=h_v, zsi=zsi_v)


def test_ex_03():

    import numpy as np
    import sympy as sym
    import stanpy as stp

    x = sym.Symbol("x")
    l = 4  # m
    s, t = 0.012, 0.02  # m
    b, ha, hb = 0.2, 0.3, 0.4  # m
    hx = ha + (hb - ha) / l * x  # m

    b_v = np.array([b, s, b])
    h_v = np.array([t, hx - 2 * t, t])

    cs_props = stp.cs(b=b_v, h=h_v)


def test_ex_04():

    import numpy as np
    import sympy as sym
    import stanpy as stp

    x = sym.Symbol("x")
    l = 4  # m
    s, t = 0.012, 0.02  # m
    ba, bb, ha, hb = 0.3, 0.4, 0.3, 0.4  # m
    hx = ha + (hb - ha) / l * x  # m
    bx = ba + (bb - ba) / l * x  # m

    b_v = np.array([bx, s, bx])
    h_v = np.array([t, hx - 2 * t, t])

    Ay = np.array(
        [
            [1 / 2, 0, 0],
            [1, 1 / 2, 0],
            [1, 1, 1 / 2],
        ]
    )

    y_si = Ay.dot(b_v)

    cs_props = stp.cs(b=b_v, h=h_v, y_si=y_si)


def test_ex_05():

    import numpy as np
    import sympy as sym
    import stanpy as stp

    x = sym.Symbol("x")
    l = 4  # m
    s, t = 0.012, 0.02  # m
    b, ha, hb = 0.3, 0.3, 0.4  # m
    hx = ha + (hb - ha) / l * x  # m

    b_v = np.array([b, s, s, b])
    h_v = np.array([t, hx - 2 * t, hx - 2 * t, t])

    Az = np.array(
        [
            [1 / 2, 0, 0, 0],
            [1, 1 / 2, 0, 0],
            [1, 0, 1 / 2, 0],
            [1, 0, 1, 1 / 2],
        ]
    )

    z_si = Az.dot(h_v)

    Ay = np.array(
        [
            [1 / 2, 0, 0, 0],
            [0, 1 / 2, 0, 0],
            [1, 0, -1 / 2, 0],
            [0, 0, 0, 1 / 2],
        ]
    )

    y_si = Ay.dot(b_v)

    cs_props = stp.cs(b=b_v, h=h_v, z_si=z_si, y_si=y_si)


def test_ex_06():

    import numpy as np
    import sympy as sym
    import stanpy as stp

    x = sym.Symbol("x")
    l = 4  # m
    s, t = 0.012, 0.02  # m
    b, ha, hb = 0.3, 0.3, 0.4  # m
    hx = ha + (hb - ha) / l * x  # m

    b_v = np.array([b, s, s, b])
    h_v = np.array([t, hx - 2 * t, hx - 2 * t, t])
    h_i = 0.05

    b_v = np.array([b, s, b, s, s, s, s])
    h_v = np.array([t, hx - 2 * t, t, h_i, h_i, h_i, h_i])

    Az = np.array(
        [
            [1 / 2, 0, 0, 0, 0, 0, 0],
            [1, 1 / 2, 0, 0, 0, 0, 0],
            [1, 1, 1 / 2, 0, 0, 0, 0],
            [1, 0, 0, 0, 1 / 2, 0, 0],
            [1, 0, 0, 0, 0, 1 / 2, 0],
            [1, 1, 0, 0, 0, -1 / 2, 0],
            [1, 1, 0, 0, 0, 0, -1 / 2],
        ]
    )

    z_si = Az.dot(h_v)

    cs_props = stp.cs(b=b_v, h=h_v, z_si=z_si)


if __name__ == "__main__":
    # test_ex_01()
    test_ex_02()
