****************************************************
Reduktionsverfahren (Übertragungsmatrizenverfahren)
****************************************************

.. jupyter-execute::
    :hide-code:

    import numpy as np
    np.set_printoptions(precision=5)


EX01 Stabkonstruktion
=====================
EX01-01 (problem) 
-----------------

.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp

    EI = 32000  # kN/m2
    l = 6  # m

    hinged_support = {"w": 0, "M": 0}
    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}

    s1 = {"EI": EI, "l": l, "bc_i": hinged_support, "bc_k": {"w": 0}, "q": 10}
    s2 = {"EI": EI, "l": l, "bc_k": roller_support}

    s = [s1, s2]

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s)
    stp.plot_load(ax, *s)
    ax.set_ylim(-0.5,1)
    plt.show()

EX01-02 (solution) 
------------------
.. jupyter-execute::

    dx = 1e-9
    x_annotate = np.array([l - dx, l, 2 * l])
    x = np.sort(np.append(np.linspace(0, 2 * l, 1000), x_annotate))
    Zi, Zk = stp.tr_solver(*s)
    Fxx = stp.tr(*s, x=x)
    Z_x = Fxx.dot(Zi).round(10)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    V_x = Z_x[:, 3]

EX01-03 (plotting) 
------------------

.. jupyter-execute::

    scale = 0.5

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s)
    stp.plot_solution(
        ax,
        x=x,
        y=M_x,
        annotate_x=[0, x[M_x == np.max(M_x)], l, 2 * l],
        fill_p="red",
        fill_n="blue",
        scale=scale,
        alpha=0.2,
        flip_y=True
    )

    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.0, 0.8)
    ax.set_ylabel("M/Mmax*{}".format(scale))
    ax.set_title("[M] = kNm")
    plt.show()

.. jupyter-execute::

    scale = 0.5

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s)
    stp.plot_solution(
        ax,
        x=x,
        y=V_x,
        annotate_x=[0, l,l-dx, 2 * l],
        fill_p="red",
        fill_n="blue",
        scale=scale,
        alpha=0.2,
    )

    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.0, 0.8)
    ax.set_ylabel("V/Vmax*{}".format(scale))
    ax.set_title("[V] = kN")
    plt.show()


.. jupyter-execute::

    scale = 0.2
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s, lw=1, linestyle=":", c="#111111")
    stp.plot_solution(ax, x=x, y=w_x, scale=scale, linestyle="-", flip_y=True, lw=2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.5, 1.5)
    ax.set_ylabel("w/wmax*{}".format(scale))
    ax.set_title("[w] = m")
    plt.show()


EX02 Stabkonstruktion
=====================
EX02-01 (problem) 
-----------------

.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp

    EI = 32000  # kN/m2
    P = 4  # kN
    l = 6  # m

    hinged_support = {"w": 0, "M": 0}
    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}

    s1 = {"EI": EI, "l": l, "bc_i": fixed_support, "bc_k": {"w": 0}, "q": 10, "P": (P, l / 2)}
    s2 = {"EI": EI, "l": l, "bc_k": roller_support}

    s = [s1, s2]

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s)
    stp.plot_load(ax, *s)
    ax.set_ylim(-0.5,1.5)
    plt.show()

EX01-02 (solution) 
------------------
.. jupyter-execute::

    dx = 1e-9
    x_annotate = np.array([l/2, l/2-dx, l - dx, l, 2*l])
    x = np.sort(np.append(np.linspace(0, 2 * l, 1000), x_annotate))
    print(x[x==l/2])
    Zi, Zk = stp.tr_solver(*s)
    Fxx = stp.tr(*s, x=x)
    Z_x = Fxx.dot(Zi).round(10)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    V_x = Z_x[:, 3]

EX01-03 (plotting) 
------------------

.. jupyter-execute::

    scale = 0.5

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s)
    stp.plot_solution(
        ax,
        x=x,
        y=M_x,
        annotate_x=[0, x[M_x == np.max(M_x)], l, 2 * l],
        fill_p="red",
        fill_n="blue",
        scale=scale,
        alpha=0.2,
        flip_y=True
    )

    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.0, 1)
    ax.set_ylabel("M/Mmax*{}".format(scale))
    ax.set_title("[M] = kNm")
    plt.show()

.. jupyter-execute::

    scale = 0.5

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s)
    stp.plot_solution(
        ax,
        x=x,
        y=V_x,
        annotate_x=[0, [l/2-dx, l/2], l - dx, l, 2*l],
        fill_p="red",
        fill_n="blue",
        scale=scale,
        alpha=0.2,
    )

    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.0, 1)
    ax.set_ylabel("V/Vmax*{}".format(scale))
    ax.set_title("[V] = kN")
    plt.show()

.. jupyter-execute::

    scale = 0.2
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s, lw=1, linestyle=":", c="#111111")
    stp.plot_solution(ax, x=x, y=w_x, scale=scale, linestyle="-", lw="2", flip_y=True)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.5, 1.5)
    ax.set_ylabel("w/wmax*{}".format(scale))
    ax.set_title("[w] = m")
    plt.show()

EX03 Stabkonstruktion
=====================
EX03-01 (problem) 
-----------------

.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp

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

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s)
    stp.plot_load(ax, *s)
    ax.set_ylim(-0.5,1)
    plt.show()

EX03-02 (solution) 
------------------
.. jupyter-execute::
    
    dx = 1e-9
    x_annotate = np.array([dx, l-dx, l, 2 * l, 5 * l / 2 - dx, 5 * l / 2])
    x = np.sort(np.append(np.linspace(0, 3 * l, 1000), x_annotate))
    Zi, Zk = stp.tr_solver(*s)
    Fxx = stp.tr(*s, x=x)
    Z_x = Fxx.dot(Zi).round(10)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    V_x = Z_x[:, 3]

EX03-03 (plotting) 
------------------

.. jupyter-execute::

    scale = 0.5

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s)
    stp.plot_solution(
        ax,
        x=x,
        y=M_x,
        annotate_x=[0, l, 2 * l, 5 * l/2],
        fill_p="red",
        fill_n="blue",
        scale=scale,
        alpha=0.2,
        flip_y=True
    )

    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.0, 1)
    ax.set_ylabel("M/Mmax*{}".format(scale))
    ax.set_title("[M] = kNm")
    plt.show()

.. jupyter-execute::

    scale = 0.5

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s)
    stp.plot_solution(
        ax,
        x=x,
        y=V_x,
        annotate_x=[dx, l-dx, l, 2*l, 5*l/2-dx, 5*l/2, 3*l],
        fill_p="red",
        fill_n="blue",
        scale=scale,
        alpha=0.2,
    )

    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.0, 1)
    ax.set_ylabel("V/Vmax*{}".format(scale))
    ax.set_title("[V] = kN")
    plt.show()

.. jupyter-execute::

    scale = 0.2
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s, lw=1, linestyle=":", c="#111111")
    stp.plot_w(ax, x=x, wx=w_x, scale=scale, linestyle="-")
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.5, 1.5)
    ax.set_ylabel("w/wmax*{}".format(scale))
    ax.set_title("[w] = m")
    plt.show()

Grundlagen
==========

todo















