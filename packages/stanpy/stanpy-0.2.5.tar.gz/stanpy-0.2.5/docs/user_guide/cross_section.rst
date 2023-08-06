
*****************
Querschnittswerte
*****************
.. Note:: 
    todos: Abbildungen, Definition der Vektoren h und b, Funktion für I, H, HEB, HEA, ...

In diesem Abschnitt werden die Querschnittswerte für verschieden zusammengesetzte Rechtecksquerschnitte berechnet.

EX01 Rechtecksquerschnitt
=========================

.. jupyter-execute::

    import numpy as np
    import stanpy as stp
    import matplotlib.pyplot as plt

    b = 0.2  # m
    h = 0.4 # m
    
    cs_props = stp.cs(b=b,h=h)

    print(cs_props)

    offset = 0.2
    fig, ax = plt.subplots()
    stp.plot_cs(ax, b, h)
    ax.set_xlim(-offset, np.max(b) + offset)
    ax.set_ylim(-offset, np.max(h) + offset)
    ax.grid(linestyle=":")
    ax.axis('equal')
    plt.show()

    

EX02 Zusammengesetzter Rechtecksquerschnitt
===========================================

.. jupyter-execute::

    import numpy as np
    import stanpy as stp
    import matplotlib.pyplot as plt

    s, t = 0.012, 0.02  # m
    b, h = 0.3, 0.4 # m
    b_v = np.array([b, s, b])
    h_v = np.array([t, h - 2 * t, t])
    zsi_v = np.array([t / 2, t + (h - 2 * t) / 2, t + (h - 2 * t) + t / 2])  # von OK
    ysi_v = np.array([b/2, b/2, b/2])  # von Links

    cs_props = stp.cs(b=b_v, h=h_v, y_si=ysi_v, z_si=zsi_v)
    print(cs_props)
    offset = 0.2
    fig, ax = plt.subplots()
    stp.plot_cs(ax, b_v, h_v, ysi_v, zsi_v)
    ax.set_xlim(-offset, np.max(b) + offset)
    ax.set_ylim(-offset, np.max(h) + offset)
    ax.grid(linestyle=":")
    ax.axis('equal')
    plt.show()



EX03 I-Querschnitt
==================

.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt
    import stanpy as stp
    import matplotlib.pyplot as plt

    s, t = 0.012, 0.02  # m
    b, h = 0.3, 0.4 # m
    b_v = np.array([b, s, b])
    h_v = np.array([t, h - 2 * t, t])
    ysi_v = stp.AI_y.dot(b_v) # von OK
    zsi_v = stp.AI_z.dot(h_v) # von Links

    cs_props = stp.cs(b=b_v, h=h_v, y_si=ysi_v, z_si=zsi_v)

    print(cs_props)

    offset = 0.2
    fig, ax = plt.subplots()
    stp.plot_cs(ax, b_v, h_v, ysi_v, zsi_v)
    ax.set_xlim(-offset, np.max(b) + offset)
    ax.set_ylim(-offset, np.max(h) + offset)
    ax.grid(linestyle=":")
    ax.axis('equal')
    plt.show()

    

EX04 H-Querschnitt
==================

.. jupyter-execute::

    import numpy as np
    import stanpy as stp
    import matplotlib.pyplot as plt

    s, t = 0.02, 0.02  # m
    b, h = 0.3, 0.4 # m

    b_v = np.array([t, h - 2 * t, t])
    h_v = np.array([b, s, b])
    ysi_v = stp.AH_y.dot(b_v) # von OK
    zsi_v = stp.AH_z.dot(h_v) # von Links

    cs_props = stp.cs(b=b_v, h=h_v, y_si=ysi_v, z_si=zsi_v)

    print(cs_props)

    offset = 0.2
    fig, ax = plt.subplots()
    stp.plot_cs(ax, b_v, h_v, ysi_v, zsi_v)
    ax.set_xlim(-offset, np.max(b) + offset)
    ax.set_ylim(-offset, np.max(h) + offset)
    ax.grid(linestyle=":")
    ax.axis('equal')
    plt.show()

EX05 Kasten-Querschnitt
=======================

.. jupyter-execute::

    import numpy as np
    import stanpy as stp
    import matplotlib.pyplot as plt

    s, t = 0.012, 0.02  # m
    b, h = 0.3, 0.4 # m

    b_v = np.array([b, s, s, b])
    h_v = np.array([t, h - 2 * t, h - 2 * t, t])
    ysi_v = stp.AK_y.dot(b_v) # von OK
    zsi_v = stp.AK_z.dot(h_v) # von Links

    cs_props = stp.cs(b=b_v, h=h_v, z_si=zsi_v, y_si=ysi_v)

    print(cs_props)

    offset = 0.2
    fig, ax = plt.subplots()
    stp.plot_cs(ax, b_v, h_v, ysi_v, zsi_v)
    ax.set_xlim(-offset, np.max(b) + offset)
    ax.set_ylim(-offset, np.max(h) + offset)
    ax.grid(linestyle=":")
    ax.axis('equal')
    plt.show()

EX06 - Verstärkter I Querschnitt
================================

.. jupyter-execute::

    import numpy as np
    import stanpy as stp
    import matplotlib.pyplot as plt

    s, t = 0.012, 0.02  # m
    b, h = 0.3, 0.4 # m
    h_i = 0.05  # m

    b_v = np.array([b, s, b, s, s, s, s])
    h_v = np.array([t, h - 2 * t, t, h_i, h_i, h_i, h_i])
    ysi_v = stp.AI_yp.dot(b_v) # von OK
    zsi_v = stp.AI_zp.dot(h_v) # von Links

    cs_props = stp.cs(b=b_v, h=h_v, z_si=zsi_v, y_si=ysi_v)
    
    print(cs_props)

    offset = 0.2
    fig, ax = plt.subplots()
    stp.plot_cs(ax, b_v, h_v, ysi_v, zsi_v)
    ax.set_xlim(-offset, np.max(b) + offset)
    ax.set_ylim(-offset, np.max(h) + offset)
    ax.grid(linestyle=":")
    ax.axis('equal')
    plt.show()


.. meta::
    :description lang=de:
        Examples of document structure features in pydata-sphinx-theme.