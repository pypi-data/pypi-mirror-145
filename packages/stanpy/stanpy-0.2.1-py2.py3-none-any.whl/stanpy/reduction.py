import stanpy as stp
import numpy as np


def P_detach_mat(detach):
    P = np.zeros((5, 5))
    if detach == "w":
        P[0, 0] = 1
    elif detach == "phi":
        P[1, 1] = 1
    elif detach == "M":
        P[2, 2] = 1
    elif detach == "V":
        P[3, 3] = 1
    return P


def P_inject_mat(detach, row):
    P = np.zeros((5, 5))
    if detach == "w":
        P[row, 0] = 1
    elif detach == "phi":
        P[row, 1] = 1
    elif detach == "M":
        P[row, 2] = 1
    elif detach == "V":
        P[row, 3] = 1
    return P


def tr_plus(s, detach="V", inject="V"):
    Fji_i = stp.tr(s)
    if inject == "V":
        A, P_minus, P_plus = A_w(s, detach=detach)
    elif inject == "phi":
        A, P_minus, P_plus = A_M(s, detach=detach)

    A_j = P_minus.dot(A) + np.eye(5, 5)
    Fji_k = Fji_i.dot(A_j) + P_plus
    return Fji_k, A_j


def A_w(s, detach=None):
    Fji = stp.tr(s)
    A = np.array(
        [
            [-1.0, -Fji[0, 1], -Fji[0, 2], -Fji[0, 3], -Fji[0, 4]],
            [-1 / Fji[0, 1], -1.0, -Fji[0, 2] / Fji[0, 1], -Fji[0, 3] / Fji[0, 1], -Fji[0, 4] / Fji[0, 1]],
            [-1 / Fji[0, 2], -Fji[0, 1] / Fji[0, 2], -1.0, -Fji[0, 3] / Fji[0, 2], -Fji[0, 4] / Fji[0, 2]],
            [-1 / Fji[0, 3], -Fji[0, 1] / Fji[0, 3], -Fji[0, 2] / Fji[0, 3], -1.0, -Fji[0, 4] / Fji[0, 3]],
            [0, 0, 0, 0, -1.0],
        ]
    )
    if detach == None:
        return A
    else:
        return A, P_detach_mat(detach), P_inject_mat(detach, row=3)


def A_M(s, detach=None):
    Fji = stp.tr(s)
    if Fji[2, 1] == 0:
        A = np.array(
            [
                [-1.0, 0, 0, 0, 0],
                [0, -1.0, 0, 0, 0],
                [0, -Fji[2, 1] / Fji[2, 2], -1.0, -Fji[2, 3] / Fji[2, 2], -Fji[2, 4] / Fji[2, 2]],
                [0, -Fji[2, 1] / Fji[2, 3], -Fji[2, 2] / Fji[2, 3], -1.0, -Fji[2, 4] / Fji[2, 3]],
                [0, 0, 0, 0, -1.0],
            ]
        )
    else:
        A = np.array(
            [
                [-1.0, 0, 0, 0, 0],
                [0, -1.0, -Fji[2, 2] / Fji[2, 1], -Fji[2, 3] / Fji[2, 1], -Fji[2, 4] / Fji[2, 1]],
                [0, -Fji[2, 1] / Fji[2, 2], -1.0, -Fji[2, 3] / Fji[2, 2], -Fji[2, 4] / Fji[2, 2]],
                [0, -Fji[2, 1] / Fji[2, 3], -Fji[2, 2] / Fji[2, 3], -1.0, -Fji[2, 4] / Fji[2, 3]],
                [0, 0, 0, 0, -1.0],
            ]
        )
    if detach == None:
        return A
    else:
        return A, P_detach_mat(detach), P_inject_mat(detach, row=1)


def F_roller_support_reduced(Fxi_minus, bc_i, w_e=0, theta=0):
    """ """
    if bc_i == {"w": 0, "M": 0}:
        alpha_index = 1
        beta_index = 3
        delta_index = -1

    alpha = Fxi_minus[:, alpha_index]
    beta = Fxi_minus[:, beta_index]
    delta = Fxi_minus[:, -1]

    Fxi_plus = np.zeros((5, 3))
    # Fxi_plus[:,0] = alpha-alpha_hat/gamma_hat*gamma
    Fxi_plus[:, 0] = alpha - alpha[0] * beta / beta[0]
    Fxi_plus[:, -1] = delta - delta[0] * beta / beta[0]
    Fxi_plus[-2, -2] = 1
    Fxi_plus[-1, -1] = 1
    return Fxi_plus


def F_roller_support(Fxi_minus, bc_i):
    delta_index = -1

    if bc_i == {"w": 0, "M": 0}:
        alpha_index = 1
        beta_index = 3
    elif bc_i == {"w": 0, "phi": 0}:
        alpha_index = 2
        beta_index = 3

    alpha = Fxi_minus[:, alpha_index]
    beta = Fxi_minus[:, beta_index]
    delta = Fxi_minus[:, -1]

    Fxi_delta = np.zeros((5, 5))
    Fxi_delta[:, alpha_index] = -alpha[0] * beta / beta[0]
    Fxi_delta[:, delta_index] = -delta[0] * beta / beta[0]

    Fxi_plus = np.zeros((5, 5))
    Fxi_plus[:, [alpha_index, delta_index]] = (
        Fxi_minus[:, [alpha_index, delta_index]] + Fxi_delta[:, [alpha_index, delta_index]]
    )

    Ax = np.array([0, 0, 0, 1, 0])
    Fxi_plus[:, beta_index] = Ax
    # np.set_printoptions(precision=5)
    return Ax, Fxi_plus


def F_hinge(Fxi_minus, bc_i):
    delta_index = -1

    if bc_i == {"w": 0, "M": 0}:
        alpha_index = 1
        beta_index = 3
    elif bc_i == {"w": 0, "phi": 0}:
        alpha_index = 2
        beta_index = 3

    alpha = Fxi_minus[:, alpha_index]
    beta = Fxi_minus[:, beta_index]
    delta = Fxi_minus[:, -1]

    Fxi_delta = np.zeros((5, 5))
    Fxi_delta[:, alpha_index] = -alpha[2] * beta / beta[2]
    Fxi_delta[:, delta_index] = -delta[2] * beta / beta[2]

    Fxi_plus = np.zeros((5, 5))
    Fxi_plus[:, [alpha_index, delta_index]] = (
        Fxi_minus[:, [alpha_index, delta_index]] + Fxi_delta[:, [alpha_index, delta_index]]
    )

    Ax = np.array([0, 1, 0, 0, 0])
    Fxi_plus[:, 3] = Ax

    return Ax, Fxi_plus


def get_local_coordinates(*slabs, x: np.ndarray):
    l = np.array([s.get("l") for s in slabs])
    l_global = np.cumsum(l) - l
    x_local = np.zeros(x.shape)
    mask_list = []
    for lengths in zip(l_global[:-1], l_global[1:]):
        mask = (x > lengths[0]) & (x <= lengths[1])
        mask_list.append(mask)
        x_local[mask] = x[mask] - lengths[0]
    mask = x > lengths[1]
    x_local[mask] = x[mask] - lengths[1]
    mask_list.append(mask)
    return x_local, mask_list, l_global


def fill_bc_dictionary_slab(*slabs):
    bc_i = [s.get("bc_i") for s in slabs]
    bc_k = [s.get("bc_k") for s in slabs]
    bc = np.array(list(zip(bc_i, bc_k))).flatten()

    if (bc[1:-1:2] != None).any():
        bc[2:-1:2] = bc[1:-1:2]
    elif (bc[2:-1:2] != None).any():
        bc[1:-1:2] = bc[2:-1:2]


def get_bc_interfaces(*slabs):
    bc_i = [s.get("bc_i") for s in slabs]
    bc_k = [s.get("bc_k") for s in slabs]
    bc = np.array(list(zip(bc_i, bc_k))).flatten()

    return bc[1:-1:2]


def solve_system2(*s, x: np.ndarray = np.array([])):

    fill_bc_dictionary_slab(*s)
    bc_interface = get_bc_interfaces(*s)

    print(bc_interface)

    return 0, 0


def solve_system(*slabs, x: np.ndarray = np.array([])):

    fill_bc_dictionary_slab(*slabs)

    bc_interace = get_bc_interfaces(*slabs)

    number_slabs = len(slabs)
    l = np.array([s.get("l") for s in slabs])
    bc_i = [s.get("bc_i") for s in slabs]
    bc_k = [s.get("bc_k") for s in slabs]

    x_local, mask, l_global = get_local_coordinates(*slabs, x=x)

    Fxa_plus = np.zeros((number_slabs + 1, 5, 5))
    Fxa_plus[0] = np.eye(5, 5)
    Fxx = np.zeros((x.size, 5, 5))
    for i, slab in enumerate(slabs):
        Fxx[mask[i]] = stp.tr(slab, x=x_local[mask[i]])

    Axk = np.zeros((len(bc_interace), 5))

    for i, bci_interface in enumerate(bc_interace):
        if bci_interface == {"w": 0}:
            Axk[i], Fxa_plus[i + 1] = F_roller_support(Fxx[mask[i]][-1].dot(Fxa_plus[i]), bc_i=bc_i[0])
        elif bci_interface == {"M": 0}:
            Axk[i], Fxa_plus[i + 1] = F_hinge(Fxx[mask[i]][-1].dot(Fxa_plus[i]), bc_i=bc_i[0])

    Fxx[0] = np.eye(5, 5)

    Fxa_plus[0] = np.zeros((5, 5))

    if ~mask[-1].any():
        raise IndexError("length of system = {} < sum beam list {}".format(l_global[-1], l))

    Fxa_plus[-1] = Fxx[mask[-1]][-1].dot(Fxa_plus[-2])

    za_fiktiv, z_end = stp.solve_tr(Fxa_plus[-1], bc_i=bc_i[0], bc_k=bc_k[-1])

    dza_fiktiv = np.zeros((Fxa_plus.shape[0], 5))
    dza_fiktiv[1:-1, :] = -Axk * za_fiktiv
    zx_minus = Fxa_plus.dot(za_fiktiv) + dza_fiktiv

    zx_minus[-1, :] = z_end

    zx_plus = np.zeros(zx_minus.shape)
    zx_plus[0, :] = za_fiktiv - Axk[0] * (Fxx[mask[0]][-1].dot(za_fiktiv) - zx_minus[1])
    for i in range(1, zx_minus.shape[0] - 1):
        zx_plus[i, :] = zx_minus[i] - Axk[i - 1] * (np.dot(Fxx[mask[i]][-1], zx_minus[i]) - zx_minus[i + 1])

    zx = np.zeros((x.size, 5))
    for i in range(number_slabs):
        zx[mask[i], :] = Fxx[mask[i]].dot(zx_plus[i, :])

    zx[x == 0] = zx_plus[0, :]
    x = np.append(x, l_global[1:])
    zx = np.append(zx, zx_plus[1:-1, :], axis=0)

    arr1inds = x.argsort()
    x = x[arr1inds]
    zx = zx[arr1inds]

    return x, zx.round(9)


if __name__ == "__main__":

    import numpy as np
    import sympy as sym
    import stanpy as stp
    from scipy.signal import argrelextrema
    import matplotlib.pyplot as plt

    EI = 32000  # kN/m2
    l = 6  # m
    q = 5  # kN/m

    hinged_support = {"w": 0, "M": 0}
    roller_support = {"w": 0, "M": 0, "H": 0}
    fixed_support = {"w": 0, "phi": 0}

    s1 = {"EI": EI, "l": l, "bc_i": {"w": 0, "phi": 0}, "bc_k": {"M": 0}, "q": q}
    s2 = {"EI": EI, "l": l, "bc_k": {"w": 0, "phi": 0}, "q": q}

    s = [s1, s2]

    dx = 1e-10
    x = np.sort(np.append(np.linspace(0, 12, 1000), [0 + dx, l, l - dx]))
    # x, Zx = stp.solve_system(*s, x=x)
    x, Zx = stp.solve_system2(*s, x=x)

    quit()

    print(Zx[0])
    print(Zx[x == l])
    print(Zx[-1])
    local_mins_idx = argrelextrema(Zx[:, 2], np.greater)

    x_annotate = np.append([0, l, 2 * l], x[local_mins_idx])
    scale = 0.5
    fig, (ax, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 15))
    stp.plot_system(ax, *s, watermark_pos=2)
    stp.plot_M(
        ax,
        x=x,
        Mx=Zx[:, 2],
        annotate_x=x_annotate,
        fill_p="red",
        fill_n="blue",
        scale=scale,
        alpha=0.2,
    )

    ax.set_ylim(-1, 1)
    ax.set_title("\mathbf{[ M ]~=~kNm}")
    ax.axis('off')

    stp.plot_system(ax2, *s, watermark=False)
    stp.plot_R(
        ax2,
        x=x,
        Rx=Zx[:, 3],
        annotate_x=[0, l - dx, l, 2 * l],
        fill_p="red",
        fill_n="blue",
        scale=scale,
        alpha=0.2,
    )

    ax2.set_ylim(-1, 1)
    ax2.set_title("\mathbf{[ V ]~=~kN}")
    ax2.axis('off')

    local_mins_idx = argrelextrema(Zx[:, 0], np.greater)
    x_annotate = np.append([0, l, 2 * l], x[local_mins_idx])
    scale = 0.1
    stp.plot_system(ax3, *s, lw=2, c="gray", linestyle="--", watermark=False)
    stp.plot_solution(
        ax3,
        x=x,
        y=Zx[:, 0] * 1e2,
        annotate_x=x_annotate,
        round=6,
        lw=3,
        scale=scale,
        alpha=0.2,
        flip_y=True,
    )

    ax3.set_ylim(-1, 1)
    ax3.set_title("\mathbf{[ w ]~=~cm}")
    ax3.axis('off')

    local_mins_idx = argrelextrema(Zx[:, 1], np.greater)
    local_max_idx = argrelextrema(Zx[:, 1], np.less)
    x_annotate = np.append(np.append([0 + dx, 0, l, 2 * l], x[local_mins_idx]), x[local_max_idx]).flatten()
    scale = 0.3
    stp.plot_system(ax4, *s, watermark=False)
    stp.plot_solution(
        ax4,
        x=x,
        y=Zx[:, 1],
        annotate_x=x_annotate,
        round=6,
        fill_p="red",
        fill_n="blue",
        scale=scale,
        alpha=0.2,
    )

    ax4.set_ylim(-1, 1)
    # ax4.set_title("[ $\mathbf{\\varphi}$ ]")
    ax4.axis('off')

    plt.tight_layout()
    plt.show()
