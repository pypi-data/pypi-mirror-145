import stanpy as stp
import numpy as np
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def test_multiple_w0():

    EI = 32000  # kN/m2
    l = 3  # m

    hinged_support = {"w": 0, "M": 0}
    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}

    s1 = {"EI": EI, "l": l, "bc_i": hinged_support, "bc_k": {"w": 0}, "q": 10}
    s2 = {"EI": EI, "l": l, "bc_k": {"w": 0}, "q": 10}
    # s2 = {"EI": EI, "l": l, "q": 10}
    s3 = {"EI": EI, "l": l, "bc_k": {"w": 0}, "q": 10}
    s4 = {"EI": EI, "l": l, "bc_k": roller_support}

    s = [s1, s2, s3, s4]

    x = np.linspace(0,4*l,5)
    Zi, Zk = stp.tr_solver(*s)
    Fx = stp.tr(*s, x=x)
    Zx = Fx.dot(Zi)

    path = os.path.join(dir_path, "reduction_method_npz", "test_multiple_w0.npz")
    # np.savez_compressed(path, Fx=Fx, Zx=Zx)
    npz = np.load(path)
    Zx_test = npz["Zx"]
    Fx_test = npz["Fx"]

    np.testing.assert_allclose(Fx, Fx_test,rtol=1e-5)
    np.testing.assert_allclose(Zx, Zx_test,rtol=1e-5)

def test_multiple_w0_M0():

    import numpy as np
    np.set_printoptions(precision=6, threshold=5000)
    import matplotlib.pyplot as plt
    import stanpy as stp

    EI = 32000  # kN/m2
    l = 3  # m

    hinged_support = {"w": 0, "M": 0}
    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}

    s1 = {"EI": EI, "l": l, "bc_i": hinged_support, "bc_k": {"w": 0}, "q": 10}
    s2 = {"EI": EI, "l": l, "bc_k": {"M": 0}, "q": 8}
    # s2 = {"EI": EI, "l": l, "q": 10}
    s3 = {"EI": EI, "l": l, "bc_k": {"w": 0}, "q": 6}
    s4 = {"EI": EI, "l": l, "bc_k": roller_support}

    s = [s1, s2, s3, s4]


    x = np.sort(np.append(np.linspace(0,4*l,4000), [l,2*l, 3*l, 4*l]))

    Zi, Zk = stp.tr_solver(*s)
    Fx = stp.tr(*s, x=x)
    Zx = Fx.dot(Zi).round(10)
  
    path = os.path.join(dir_path, "reduction_method_npz", "test_multiple_w0_M0.npz")
    # np.savez_compressed(path, Fx=Fx, Zx=Zx)
    npz = np.load(path)
    Zx_test = npz["Zx"]
    Fx_test = npz["Fx"]

    np.testing.assert_allclose(Fx, Fx_test,rtol=1e-5)
    np.testing.assert_allclose(Zx, Zx_test,rtol=1e-5)

def test_multiple_w0_combination():
    """testet einwertige Bindungen mit zusammengesetzten Stäben
    """

    import numpy as np
    np.set_printoptions(precision=6, threshold=5000)
    import matplotlib.pyplot as plt
    import stanpy as stp

    EI = 32000  # kN/m2
    l = 3  # m

    hinged_support = {"w": 0, "M": 0}
    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}

    s1 = {"EI": EI, "l": l, "bc_i": hinged_support, "bc_k": {"w": 0}, "q": 10}
    # s2 = {"EI": EI, "l": l, "bc_k": {"M": 0}, "q": 10}
    s2 = {"EI": EI, "l": l, "q": 8}
    s3 = {"EI": EI, "l": l, "bc_k": {"w": 0}, "q": 6}
    s4 = {"EI": EI, "l": l, "bc_k": roller_support}

    s = [s1, s2, s3, s4]

    x = np.sort(np.append(np.linspace(0,4*l,4000), [l,2*l, 3*l, 4*l]))

    Zi, Zk = stp.tr_solver(*s)
    Fx = stp.tr(*s, x=x)
    Zx = Fx.dot(Zi).round(10)
  
    path = os.path.join(dir_path, "reduction_method_npz", "test_multiple_w0_combination.npz")
    # np.savez_compressed(path, Fx=Fx, Zx=Zx)

    npz = np.load(path)
    Zx_test = npz["Zx"]
    Fx_test = npz["Fx"]

    np.testing.assert_allclose(Fx, Fx_test,rtol=1e-5)
    np.testing.assert_allclose(Zx, Zx_test,rtol=1e-5)

def test_large_system():
    import numpy as np
    import sympy as sym
    import stanpy as stp
    import matplotlib.pyplot as plt

    EI = 32000  # kN/m2
    P = 5  # kN
    q = 4  # kN/m
    l = 3  # m

    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}
    hinge = {"M": 0}

    s0 = {"EI": EI, "l": l, "bc_i": fixed_support, "bc_k": {"w": 0}}
    s1 = {"EI": EI, "l": l, "bc_k": {"w": 0}, "q": q}
    s2 = {"EI": EI, "l": l, "bc_k": {"w": 0}}
    s3 = {"EI": EI, "l": l, "bc_k": hinge, "q": q, "P": (P, l)}
    s4 = {"EI": EI, "l": l, "bc_k": {"w": 0}}
    s5 = {"EI": EI, "l": l, "bc_k": hinge}
    s6 = {"EI": EI, "l": l, "bc_k": roller_support, "P": (P, l / 2), }

    s = [s0, s1, s2, s3, s4, s5, s6]

    # fig, ax = plt.subplots(figsize=(12, 5))
    # stp.plot_system(ax, s=22, *s)
    # stp.plot_load(ax, *s, P_scale=0.5, q_scale=0.5)
    # ax.set_ylim(-0.5, 1)
    # plt.show()

    x = np.sort(np.append(np.linspace(0,7*l,70),[l,2*l, 3*l, 4*l, 5*l, 6*l]))
    Zi, Zk = stp.tr_solver(*s)
    Fx = stp.tr(*s, x=x)
    Zx = Fx.dot(Zi)

    path = os.path.join(dir_path, "reduction_method_npz", "test_large_system.npz")
    # np.savez_compressed(path, Fx=Fx, Zx=Zx)

    npz = np.load(path)
    Zx_test = npz["Zx"]
    Fx_test = npz["Fx"]

    np.testing.assert_allclose(Fx, Fx_test,rtol=1e-5)
    np.testing.assert_allclose(Zx, Zx_test,rtol=1e-5)

    # scale = 0.5
    # fig, ax = plt.subplots()
    # stp.plot_system(ax, *s, watermark=False)
    # stp.plot_M(
    #     ax,
    #     x=x,
    #     Mx=Zx[:, 2],
    #     annotate_x=[l,2*l, 3*l, 4*l, 5*l, 6*l],
    #     fill_p="red",
    #     fill_n="blue",
    #     scale=scale,
    #     alpha=0.2,
    # )

    # ax.set_ylim(-1, 1)
    # ax.axis('off')
    # plt.show()

def test_large_system_II():
    import numpy as np
    import sympy as sym
    import stanpy as stp
    import matplotlib.pyplot as plt

    EI = 32000  # kN/m2
    P = 5  # kN
    q = 4  # kN/m
    l = 3  # m

    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}
    hinge = {"M": 0}

    s0 = {"EI": EI, "l": l, "bc_i": fixed_support, "bc_k": {"w": 0}, "N": -1000}
    s1 = {"EI": EI, "l": l, "bc_k": {"w": 0}, "q": q, "N": -1000}
    s2 = {"EI": EI, "l": l, "bc_k": {"w": 0}, "N": -1000}
    s3 = {"EI": EI, "l": l, "bc_k": hinge, "q": q, "P": (P, l), "N": -1000}
    s4 = {"EI": EI, "l": l, "bc_k": {"w": 0}, "N": -1000}
    s5 = {"EI": EI, "l": l, "bc_k": hinge, "N": -1000}
    s6 = {"EI": EI, "l": l, "bc_k": roller_support, "P": (P, l / 2), "N": -1000}

    s = [s0, s1, s2, s3, s4, s5, s6]

    # fig, ax = plt.subplots(figsize=(12, 5))
    # stp.plot_system(ax, s=22, *s)
    # stp.plot_load(ax, *s, P_scale=0.5, q_scale=0.5)
    # ax.set_ylim(-0.5, 1)
    # plt.show()

    x = np.sort(np.append(np.linspace(0,7*l,70),[l,2*l, 3*l, 4*l, 5*l, 6*l]))
    Zi, Zk = stp.tr_solver(*s)
    Fx = stp.tr(*s, x=x)
    Zx = Fx.dot(Zi)

    path = os.path.join(dir_path, "reduction_method_npz", "test_large_system_II.npz")
    # np.savez_compressed(path, Fx=Fx, Zx=Zx)

    npz = np.load(path)
    Zx_test = npz["Zx"]
    Fx_test = npz["Fx"]

    np.testing.assert_allclose(Fx, Fx_test,rtol=1e-5)
    np.testing.assert_allclose(Zx, Zx_test,rtol=1e-5)

    # scale = 0.5
    # fig, ax = plt.subplots()
    # stp.plot_system(ax, *s, watermark=False)
    # stp.plot_M(
    #     ax,
    #     x=x,
    #     Mx=Zx[:, 2],
    #     annotate_x=[l,2*l, 3*l, 4*l, 5*l, 6*l],
    #     fill_p="red",
    #     fill_n="blue",
    #     scale=scale,
    #     alpha=0.2,
    # )

    # ax.set_ylim(-1, 1)
    # ax.axis('off')
    # plt.show()

def empty():
    import matplotlib.pyplot as plt
    import numpy as np

    EI = 32000 # kNm²
    GA = 20000 # kN
    l = 6 # m
    q = 4 # kN/m
    P = 1500 # kN
    H = 10 # kN

    fixed = {"w":0, "phi":0}
    hinged = {"w":0, "M":0, "H":0}

    s = {"EI":EI, "GA":GA, "l":l, "q":q, "w_0":0.03,"N":(-P ),"P1":(H, l/2),"P2":(H, l/3),"P3":(H, 2*l/3), "bc_i":fixed, "bc_k":hinged}
    fig, ax = plt.subplots()
    stp.plot_system(ax, s)
    stp.plot_load(ax, s)
    stp.plot_w_0(ax, s, scale=0.4, dy=-0.2)
    ax.set_ylim(-1,1)
    plt.show()
    x = np

    Zi, Zk = stp.tr_solver(s)
    Fxx = stp.tr(s)
    Zx = Fxx.dot(Zi)

    print(Zx)

if __name__=="__main__":
    # test_large_system_II()
    empty()