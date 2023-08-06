******************************************************************
Der gerade Stab, konstanter Querschnitt Theorie I. und II. Ordnung
******************************************************************

.. jupyter-execute::
    :hide-code:

    import numpy as np
    np.set_printoptions(precision=5)


EX01 Einfeldträger Gleichlast  
=============================
EX01-01 (problem) 
-----------------
.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp

    EI = 32000  # kNm²
    l = 6  # m
    q = 10  # kN/m

    s = {"EI": EI, "l": 6, "q": q, "bc_i":{"w":0, "M":0},  "bc_k":{"w":0, "M":0, "H":0}}

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s)
    stp.plot_load(ax, s)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.75, 1.2)
    plt.show()

EX01-02 (solution) 
------------------
.. jupyter-execute::

    dx = 1e-9
    x = np.linspace(0, l, 100)
    x = np.sort(np.append(x, [l / 2, l / 4, 3 * l / 4, l-dx]))
    Z_a, Z_b  = stp.tr_solver(s)
    Fxa = stp.tr(s, x=x)
    Z_x = Fxa.dot(Z_a)

    print("Z_a =", Z_a)
    print("Z_b =", Z_b)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    V_x = Z_x[:, 3]

EX01-03 (plotting) 
------------------
.. jupyter-execute::

    scale = 0.5
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s)
    stp.plot_M(ax, x=x, Mx=M_x, annotate_x=[0, l / 2, l / 4, 3 * l / 4, l], fill_p="red", scale=scale, alpha=0.2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.8, 0.1)
    ax.set_ylabel("M/Mmax*{}".format(scale))
    ax.set_title("[M] = kNm")
    plt.show()

.. jupyter-execute::

    scale = 0.5
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s, watermark_pos=1)
    stp.plot_solution(ax, x=x, y=V_x, annotate_x=[0, l / 2, l / 4, 3 * l / 4, l-dx], fill_p="red", fill_n="blue", scale=scale, alpha=0.2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.8, 0.8)
    ax.set_ylabel("V/Vmax*{}".format(scale))
    ax.set_title("[V] = kN")
    plt.show()

.. jupyter-execute::

    scale = 0.2
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s, watermark_pos=1, lw=1, linestyle=":", c="#111111")
    stp.plot_w(ax, x=x, wx=w_x, scale=scale, linestyle="-")
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.8, 0.8)
    ax.set_ylabel("w/wmax*{}".format(scale))
    ax.set_title("[w] = m")
    plt.show()

EX02 Einfeldträger Einzellast  
=============================
EX02-01 (problem) 
-----------------
.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp

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

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s)
    stp.plot_load(ax, s)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.75, 1.0)
    plt.show()

EX02-02 (solution) 
------------------
.. jupyter-execute::

    dx = 1e-9
    x = np.linspace(0, l, 500)
    annotation = np.array([2-dx, 2, 3-dx, 3, 4-dx, 4, 6-dx])
    x = np.sort(np.append(x, annotation))

    Fxa = stp.tr(s, x=x)
    Z_a, Z_b = stp.tr_solver(s)
    Z_x = Fxa.dot(Z_a)

    print("Z_a =", Z_a)
    print("Z_b =", Z_b)

EX02-02-02 (solution) 
---------------------
Zusammensetzen von Stäben - Äquivalent zu EX02-02
Kräfte werden jeweils am Stabende angsetzt

.. jupyter-execute::
    
    s1 = {"EI": EI, "l": 2, "P1": (P, 2), "bc_i": {"w": 0, "M": 0}}
    s2 = {"EI": EI, "l": 1, "P2": (P+1, 1)}
    s3 = {"EI": EI, "l": 1, "P3": (P+2, 1)}
    s4 = {"EI": EI, "l": 2, "bc_k": {"w": 0, "M": 0, "H": 0}}

    s = [s1, s2, s3, s4]
    Fxa = stp.tr(*s, x=x)
    Z_a, Z_b = stp.tr_solver(*s)
    Z_x = Fxa.dot(Z_a)

    print("Z_a =", Z_a)
    print("Z_b =", Z_b)

EX02-02-03 (solution) 
---------------------
Zusammensetzen von Stäben - Äquivalent zu EX02-02 
Kräfte werden jeweils am Stabanfang angsetzt

.. jupyter-execute::

    s1 = {"EI": EI, "l": 2, "bc_i": {"w": 0, "M": 0}}
    s2 = {"EI": EI, "l": 1, "P1": (P, 0)}
    s3 = {"EI": EI, "l": 1, "P2": (P+1, 0)}
    s4 = {"EI": EI, "l": 2, "P1": (P+2, 0), "bc_k": {"w": 0, "M": 0, "H": 0}}

    s = [s1, s2, s3, s4]

    Fxa = stp.tr(*s, x=x)
    Z_a, Z_b = stp.tr_solver(*s)
    Z_x = Fxa.dot(Z_a)

    print("Z_a =", Z_a)
    print("Z_b =", Z_b)

EX02-03 (plotting) 
------------------
.. jupyter-execute::

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    V_x = Z_x[:, 3]

    scale = 0.5
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s)
    stp.plot_M(ax, x=x, Mx=M_x, annotate_x=[2, 3, 4], fill_p="red", scale=scale, alpha=0.2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.8, 0.1)
    ax.set_ylabel("M/Mmax*{}".format(scale))
    ax.set_title("[M] = kNm")
    plt.show()

.. jupyter-execute::

    scale = 0.5
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s, watermark_pos=1)
    stp.plot_solution(ax, x=x, y=V_x, annotate_x=[0, [2-dx, 2], 3-dx, 3, [4, 4-dx], 6-dx], fill_p="red", fill_n="blue", scale=scale, alpha=0.2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.5, 1.5)
    ax.set_ylabel("V/Vmax*{}".format(scale))
    ax.set_title("[V] = kN")
    plt.show()

.. jupyter-execute::

    scale = 0.2
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, *s, watermark_pos=1, lw=1, linestyle=":", c="#111111")
    stp.plot_w(ax, x=x, wx=w_x, scale=scale, linestyle="-")
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.8, 0.8)
    ax.set_ylabel("w/wmax*{}".format(scale))
    ax.set_title("[w] = m")
    plt.show()

EX03 (todo: testing)
====================
EX03-01 (problem) 
-----------------
.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp

    EI = 32000  # kNm²
    l = 6  # m
    P = 10  # kN
    q = 10 # kN/m
    N = -1000 # kN

    s = {
        "EI": EI,
        "l": 6,
        "q":q,
        "P1": (P, l/3),
        "N":N,
        "bc_i": {"w": 0, "M": 0},
        "bc_k": {"w": 0, "M": 0, "H": 0},
    }

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s)
    stp.plot_load(ax, s)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.75, 2)
    plt.show()

EX03-02-01 (solution) 
---------------------
.. jupyter-execute::

    dx = 1e-9
    x = np.linspace(0, l, 500)
    annotation = np.array([0, l / 3 - dx, l / 3, l / 2, 2, 3, 4, l-dx])
    x = np.sort(np.append(x, annotation))

    Fxa = stp.tr(s, x=x)
    Z_a, Z_b = stp.tr_solver(s)
    Z_x = Fxa.dot(Z_a)

    print("Z_a =", Z_a)
    print("Z_b =", Z_b)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    R_x = Z_x[:, 3]

    V_x = stp.R_to_Q(x, Z_x, s)

EX03-03 (plotting) 
------------------
.. jupyter-execute::

    scale = 0.5
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s)
    stp.plot_M(ax, x=x, Mx=M_x, annotate_x=[0, l/3, x[M_x==np.max(M_x)], l], fill_p="red", scale=scale, alpha=0.2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1, 0.1)
    ax.set_ylabel("M/Mmax*{}".format(scale))
    ax.set_title("[M] = kNm")
    plt.show()

.. jupyter-execute::

    scale = 0.5
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s, watermark_pos=1)
    stp.plot_R(ax, x=x, Rx=R_x, annotate_x=[0, [l/3-dx, l/3], l/2, l-dx], fill_p="red", fill_n="blue", scale=scale, alpha=0.2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1, 1)
    ax.set_ylabel("R/Rmax*{}".format(scale))
    ax.set_title("[R] = kN")
    plt.show()

.. jupyter-execute::

    scale = 0.5
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s, watermark_pos=1)
    stp.plot_solution(ax, x=x, y=V_x, annotate_x=[0, [l/3-dx, l/3], l/2, l-dx], fill_p="red", fill_n="blue", scale=scale, alpha=0.2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1, 1)
    ax.set_ylabel("V/Vmax*{}".format(scale))
    ax.set_title("[V] = kN")
    plt.show()

.. jupyter-execute::

    scale = 0.2
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s, watermark_pos=1, lw=1, linestyle=":", c="#111111")
    stp.plot_w(ax, x=x, wx=w_x, scale=scale, linestyle="-")
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.8, 0.8)
    ax.set_ylabel("w/wmax*{}".format(scale))
    ax.set_title("[w] = m")
    plt.show()

EX04 Stabkonstruktion Theorie II  
================================
EX04-01 (problem) 
-----------------
.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp

    EI = 32000  # kNm²
    GA = 20000  # kNm²
    l = 6  # m
    H = 10  # kN
    q = 4 # kN/m
    N = -1500 # kN
    w_0 = 0.03 # m

    s = {
        "EI": EI,
        "GA": GA,
        "l": l,
        "q": q,
        "P": (H, l/2),
        "N": N,
        "w_0": w_0,
        "bc_i": {"w": 0, "phi": 0},
        "bc_k": {"w": 0, "M": 0, "H": 0},
    }

    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s)
    stp.plot_load(ax, s)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1.5, 2)
    plt.show()

EX04-02 (solution) 
------------------
.. jupyter-execute::

    dx = 1e-9
    x = np.linspace(0, l, 500)
    annotation = np.array([l / 2 - dx, l / 2, l-dx])
    x = np.sort(np.append(x, annotation))

    Fxa = stp.tr(s, x=x)
    Z_a, Z_b = stp.tr_solver(s)
    Z_x = Fxa.dot(Z_a)

    print("Z_a =", Z_a)
    print("Z_b =", Z_b)

    w_x = Z_x[:, 0]
    phi_x = Z_x[:, 1]
    M_x = Z_x[:, 2]
    R_x = Z_x[:, 3]

    V_x = stp.R_to_Q(x, Z_x, s)

EX04-03 (plotting) 
------------------
.. jupyter-execute::

    scale = 0.5
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s)
    stp.plot_M(ax, x=x, Mx=M_x, annotate_x=[0,x[M_x==np.max(M_x)], l], fill_p="red", fill_n="blue", scale=scale, alpha=0.2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-1, 1.2)
    ax.set_ylabel("M/Mmax*{}".format(scale))
    ax.set_title("[M] = kNm")
    plt.show()

.. jupyter-execute::

    scale = 0.5
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s, watermark_pos=1)
    stp.plot_R(ax, x=x, Rx=R_x, annotate_x=[0, [l/2-dx, l/2], l-dx], fill_p="red", fill_n="blue", scale=scale, alpha=0.2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.8, 1.4)
    ax.set_ylabel("R/Rmax*{}".format(scale))
    ax.set_title("[R] = kN")
    plt.show()

.. jupyter-execute::

    scale = 0.5
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s, watermark_pos=1)
    stp.plot_solution(ax, x=x, y=V_x, annotate_x=[0, [l/2-dx, l/2], l-dx], fill_p="red", fill_n="blue", scale=scale, alpha=0.2)
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.8, 1.2)
    ax.set_ylabel("V/Vmax*{}".format(scale))
    ax.set_title("[V] = kN")
    plt.show()

.. jupyter-execute::

    scale = 0.2
    fig, ax = plt.subplots(figsize=(12, 5))
    stp.plot_system(ax, s, watermark_pos=1, lw=1, linestyle=":", c="#111111")
    stp.plot_w(ax, x=x, wx=w_x, scale=scale, linestyle="-")
    ax.grid(linestyle=":")
    ax.set_axisbelow(True)
    ax.set_ylim(-0.8, 0.8)
    ax.set_ylabel("w/wmax*{}".format(scale))
    ax.set_title("[w] = m")
    plt.show()

Grundlagen
==========
Den Übertragungsbeziehungen liegen die Gleichgewichtsbedingungen sowie die konstitutiven und kinematischen Beziehungen  :eq:`differential_equations` zugrunde.

.. math::
    :label: differential_equations

    \frac{dR(x)}{dx} &= -q(x) \\[1em] 
    \frac{dM(x)}{dx} &= V(x) + m(x)\\[1em]            
    \frac{d\varphi (x)}{dx} &= -\left[\frac{M(x)}{EI}+\kappa^e (x)\right]\\[1em] 
    \frac{dw (x)}{dx} &= \varphi (x)  + \frac{V}{G\tilde{A}}

Zur vollständigen Beschreibung des Problems ergibt sich, als zusätzliche Gleichung, aus einer statischen Äquivalenzbetrachtung 
die Umrechnung :eq:`conversion_V_R` zwischen Querkraft und Transversalkraft.

.. math::
    :label: conversion_V_R

    V(x) = R(x) - N^{II}(x)\left[\frac{dw_v(x)}{dx}+\frac{dw(x)}{dx}\right]

Die oben angeschriebenen gekoppelten Differentialgleichungen können mittels Eliminationsverfahren auf M-Niveau oder w-Niveau eliminert werden.
Nach Anwendung des Eliminationsverfahrens ergibt sich

.. math::
    :label: differential_equations_M_w

    \frac{d^2M(x)}{dx^2} - K M &= -\gamma\sum a_j\bar{q}_j+\sum a_{j-1} m_j-\gamma N^{II}\sum a_j\kappa^e_j\\[1em] 
    \frac{d^2w(x)}{dx^2} - K w &= -K (a_0w_A+a_1w'_A)-\frac{\gamma}{EI}(a_0M_A+a_1Q_A)\\[1em] 
    &+\gamma\sum\left(\frac{a_{j+2}}{EI}-\frac{a_j}{GA}\right)\bar{q}_j
    -\frac{\gamma}{EI}\sum a_{j+1}m_J-\gamma\sum a_j\kappa^e_j

mit 

.. math::
    :label: differential_equations_M_w_with

    \gamma = \frac{1}{1-\frac{N^{II}}{S}}\qquad K = -\gamma\frac{N^{II}}{EI}\qquad\bar{q}_j = q_j - N^{II} w^V_{j+2}


Beide Differentialgleichungen haben die Form allgemeine Form

.. math::
    :label: general_differential_equation

    y'' - K y = \sum_0 a_j k_j

Mit dem in [todo ref: stahlbauhandbuch] vorgestellten Lösungskonzept ergibt sich die allgemeinen Lösung zu:

.. math::
    :label: general_solution

    y = b_0 y_A + b_1 y'_A + \sum b_{j+2} k_j

Diese können entweder analytisch nach folgender Tabelle mittels Fallunterscheidung

+-------------+---------------+------------------------------+-------------------+----------------------------+-----------------------------------------+
| Theorie     |               | Hilfswert                    | :math:`b_0`       | :math:`b_1`                | :math:`b_2, b_3,...`                    |
+=============+===============+==============================+===================+============================+=========================================+
| I. Ordnung  | :math:`N = 0` |                              |:math:`b_j = a_j`                                                                         |
+-------------+---------------+------------------------------+-------------------+----------------------------+-----------------------------------------+
| II. Ordnung | :math:`N < 0` |:math:`\sqrt{\lvert K\rvert}` | :math:`\cos fx`   | :math:`\frac{\sin fx}{f}`  |                                         |
|             +---------------+------------------------------+-------------------+----------------------------+ :math:`b_j = \frac{b_{j-2}-a_{j-2}}{K}` |
|             | :math:`N > 0` |:math:`\sqrt{\lvert K\rvert}` | :math:`\cosh fx`  | :math:`\frac{\sinh fx}{f}` |                                         |
+-------------+---------------+------------------------------+-------------------+----------------------------+-----------------------------------------+

oder numerisch mit der Rekursionsformel :eq:`recursion_solution` berechnet werden. 

.. math::
    :label: recursion_solution

    b_j = \sum_{t=0}^\inf \beta_t\qquad\beta_t = \frac{Kx^2}{(j+2t)(j+2t-1)}\beta_{t-1}


In stanpy können die :math:`b_j` Funktionen für einen konstanten Querschnitt für beliebige :math:`j` und :math:`x` wie folgt berechnet werden

.. jupyter-execute::

    import numpy as np
    import stanpy as stp

    EI = 32000  # kNm²
    GA = 20000  # kN
    l = 6
    NII = -1500  # kN

    s = {"EI": EI, "GA": GA, "N": NII}

    a_j, b_j = stp.bj_opt2_p89(l, return_aj=True, **s)

    print("a_j =", a_j)
    print("b_j =", b_j)

.. .. list-table:: Title
..    :widths: 25 25 50
..    :header-rows: 1

..    * - Theorie
..      - Hilfswert
..      - :math:`b_0`  
..      - :math:`b_1`  
..      - :math:`b_2, b_3,...`  
..    * - I. Ordnung  
..      -
..      - Row 1, column 3
..    * - Row 2, column 1
..      - Row 2, column 2
..      - Row 2, column 3







