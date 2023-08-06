# todo: tests

def test_ex_01():

    import numpy as np
    import stanpy as stp

    b = 0.2
    h = 0.4

    cs_props = stp.cs(b=b, h=h)

    print("I_y = ", cs_props["I_y"])
    print("I_z = ", cs_props["I_z"])
    print("A = ", cs_props["A"])
    print("z_s = ", cs_props["z_s"])


def test_ex_02():

    import numpy as np
    import stanpy as stp

    s, t = 0.012, 0.02  # m
    b, h = 0.5, 0.39
    b_v = np.array([b, s, b])
    h_v = np.array([t, h - 2 * t, t])
    z_siv = np.array([t / 2, t + (h - 2 * t) / 2, t + (h - 2 * t) + t / 2])  # von OK

    cs_props = stp.cs(b=b_v, h=h_v, z_si=z_siv)

    print(cs_props)


def test_ex_03():

    import numpy as np
    import stanpy as stp

    s, t = 0.012, 0.02  # m
    b, h = 0.5, 0.39
    b_v = np.array([b, s, b])
    h_v = np.array([t, h - 2 * t, t])

    cs_props = stp.cs(b=b_v, h=h_v)

    print(cs_props)


def test_ex_04():

    import numpy as np
    import stanpy as stp

    s, t = 0.012, 0.02  # m
    b, h = 0.5, 0.39

    b_v = np.array([b, s, b])
    h_v = np.array([t, h - 2 * t, t])

    Ay = np.array(
        [
            [1 / 2, 0, 0],
            [1, 1 / 2, 0],
            [1, 1, 1 / 2],
        ]
    )

    y_si = Ay.dot(b_v)

    cs_props = stp.cs(b=b_v, h=h_v, y_si=y_si)

    print(cs_props)


def test_ex_05():

    import numpy as np
    import stanpy as stp

    s, t = 0.012, 0.02  # m
    b, h = 0.5, 39.4

    b_v = np.array([b, s, s, b])
    h_v = np.array([t, h - 2 * t, h - 2 * t, t])

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

    print(cs_props)


def test_ex_06():

    import numpy as np
    import stanpy as stp

    s, t = 0.012, 0.02  # m
    b, h = 0.5, 0.39
    h_i = 0.05

    b_v = np.array([b, s, b, s, s, s, s])
    h_v = np.array([t, h - 2 * t, t, h_i, h_i, h_i, h_i])

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
    
    print(cs_props)


if __name__ == "__main__":
    test_ex_06()
