from hashlib import sha384
import stanpy as stp
import numpy as np

from stanpy.transfer_relation import solve_tr

Xw = np.zeros((5,5))
Xw[0,0] = 1
Xphi = np.zeros((5,5))
Xphi[1,1] = 1
XM = np.zeros((5,5))
XM[2,2] = 1
XR = np.zeros((5,5))
XR[3,3] = 1

Pw = np.zeros((5,5))
Pw[3,:] = 1
PM = np.zeros((5,5))
PM[1,:] = 1

 
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

def tr_plus2(s, detach="V", inject="V"):
    eye = np.eye(5,5)
    if isinstance(s, list):
        Fji_i = stp.tr(*s)[-1]
    elif isinstance(s, dict):
        Fji_i = stp.tr(s)
    
    detach_dict = {"V":XR, "R":XR, "M":XM, "phi":Xphi, "w":Xw}
    X = detach_dict[detach]
    if inject == "V" or inject == "R":
        A = A_w(s)
        P = Pw.dot(X)
        A_j = X.dot(A)+eye
    elif inject == "phi":
        A = A_M(s)
        P = PM.dot(X)
        A_j = X.dot(A)+eye
    Fji_k = Fji_i.dot(A_j) + P
    return Fji_k, A_j

def detachable(bc):
    if all(k in bc for k in ("w","phi")):
        return ["R", "M"]
    elif all(k in bc for k in ("w")):
        return ["R"]
    elif all(k in bc for k in ("M")):
        return ["phi"]
    elif bc==None:
        return [None]

def injectable(bc):
    if {"w":0}==bc:
        return ["R"]
    elif {"M":0}==bc:
        return ["phi"]
    elif bc==None:
        return [None]
    else:
        return [None]

def tr_red(s_list:list, x:np.ndarray):
    if isinstance(s_list, dict):
        s_list = [s_list]

    if isinstance(x, (int, float, list)):
        x = np.array([x]).flatten()

    if x.size == 0:
        x = stp.calc_x_system(*s_list)

    bc_interface = np.empty(len(s_list)+1, dtype=object)
    bc_interface[1:-1] = stp.get_bc_interfaces(*s_list)
    # bc_interface = stp.get_bc_interfaces(*s_list)

    tr_R_ends = np.zeros((len(s_list) + 1, 5, 5))
    tr_R_ends[0, :, :] = np.eye(5, 5)

    tr_R_x = np.zeros((x.size, 5, 5))

    lengths, x_mask = stp.calc_x_mask(s_list, x)
    A = np.empty((len(s_list)+1, 5, 5))
    A[-1] = np.eye(5,5)
    F, A[:-1] = tr_red_ends(s_list)
    for i, s in enumerate(s_list):
        EI, GA = stp.load_material_parameters(**s)
        if isinstance(EI, (float, int)):
            tr_R_ends[i + 1, :, :] = A[i+1].dot(stp.tr_R(**s)).dot(tr_R_ends[i, :, :])
            tr_R_x[x_mask[i], :, :] = stp.tr_R(x=x[x_mask[i]] - lengths[i], **s).dot(tr_R_ends[i, :, :])
        elif isinstance(EI, np.poly1d):
            tr_R_ends[i + 1, :, :] = A[i+1].dot(stp.tr_R_poly(**s)).dot(tr_R_ends[i, :, :])
            tr_R_x[x_mask[i], :, :] = stp.tr_R_poly(x=x[x_mask[i]] - lengths[i], **s).dot(tr_R_ends[i, :, :])
    
    if x.size == 1:
        tr_R_x = tr_R_x.reshape((5, 5))

    return tr_R_x

def tr_red_ends(s_list:list):
    bc = fill_bc_dictionary_slab(*s_list)
    bc_interace = get_bc_interfaces(*s_list)

    number_slabs = len(s_list)
    l = np.array([s.get("l") for s in s_list])
    bc_i = [s.get("bc_i") for s in s_list]
    bc_k = [s.get("bc_k") for s in s_list]

    F = np.empty((number_slabs, 5, 5))
    A = np.empty((number_slabs, 5, 5))
    A[:] = np.eye(5,5)

    last_detachable = None
    s_poly = []
    for i, s in enumerate(s_list):
        bc_i = bc[i*2]
        bc_k = bc[i*2+1]

        if bc_i == None:
            bc_i = {}
        if bc_k == None:
            bc_k = {}
        
        if bc_i!={} and bc_k!={} and i!=number_slabs-1:
            detach = detachable(bc_i)[0]
            inject = injectable(bc_k)[0]
            F[i], A[i] = tr_plus2(s, detach=detach, inject=inject)
            last_detachable = detach
        elif bc_k == {}:
            # F[i] = stp.tr(s)
            F[i] = np.eye(5,5)
            A[i] = np.eye(5,5)
            s_poly.append(s)
        elif i==number_slabs-1:
            s_poly.append(s)
            F[i] = stp.tr(*s_poly)
            detach = detachable(bc_i)[0]
            inject = injectable(bc_k)[0]
            if inject==None:
                inject = "V"
            _, A[i-len(s_poly)+1] = tr_plus2(s_poly, detach=detach, inject=inject)
            s_poly=[] 
        elif bc_i == {} and bc_k != {}:
            s_poly.append(s)
            detach = last_detachable
            inject = injectable(bc_k)[0]
            F[i], A[i-len(s_poly)+1] = tr_plus2(s_poly, detach=detach, inject=inject)
            s_poly=[] 
    return F, A

def solve_tr_red(s_list:list):

    bc = fill_bc_dictionary_slab(*s_list)
    number_slabs = len(s_list)

    Fxx = np.empty((number_slabs+1, 5, 5))
    Fxx[0] = np.eye(5,5)

    F, A = tr_red_ends(s_list)

    for i, Fi in enumerate(F):
        Fxx[i+1] = Fi.dot(Fxx[i])

    Zi_star, Zk = solve_tr(Fxx[-1], bc_i=bc[0], bc_k=bc[-1])
    Zi = A[0].dot(Zi_star)

    return Zi, Zk
        
    

def A_w(s, detach=None):
    if isinstance(s, list):
        Fji = stp.tr(*s)
        if len(Fji.shape)>2:
            Fji=Fji[-1]
    elif isinstance(s, dict):
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
    if isinstance(s, list):
        Fji = stp.tr(*s)
    elif isinstance(s, dict):
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
    return bc

def get_bc_interfaces(*slabs):
    bc_i = [s.get("bc_i") for s in slabs]
    bc_k = [s.get("bc_k") for s in slabs]
    bc = np.array(list(zip(bc_i, bc_k))).flatten()

    return bc[1:-1:2]


def solve_system2(*s, x: np.ndarray = np.array([])):

    fill_bc_dictionary_slab(*s)
    bc_interface = get_bc_interfaces(*s)

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
    # s2 = {"EI": EI, "l": l, "bc_k": {"w": 0}, "q": 8}
    # s2 = {"EI": EI, "l": l, "q": 8}
    s3 = {"EI": EI, "l": l, "bc_k": {"w": 0}, "q": 6}
    s4 = {"EI": EI, "l": l, "bc_k": roller_support}

    s = [s1, s2, s3, s4]

    fig, ax = plt.subplots()
    stp.plot_system(ax, *s)
    plt.show()

    x = np.sort(np.append(np.linspace(0,4*l,4000), [l,2*l, 3*l, 4*l]))

    Zi, Zk = stp.tr_solver(*s)
    Fx = stp.tr(*s, x=x)
    Zx = Fx.dot(Zi).round(10)

    # Fba_plus, Ab = stp.tr_plus2(s1)
    # Fdb_plus, Ad = stp.tr_plus2([s2,s3])
    # Fed = stp.tr(s4)

    # Fea = Fed.dot(Fdb_plus).dot(Fba_plus)
    # Zi, Zk = stp.solve_tr(Fea, bc_i=s1["bc_i"], bc_k=s4["bc_k"])


  
    scale = 0.5
    fig, ax = plt.subplots()
    stp.plot_system(ax, *s, watermark=False)
    stp.plot_M(
        ax,
        x=x,
        Mx=Zx[:, 2],
        annotate_x=[0,l,2*l, 3*l, 4*l],
        fill_p="red",
        fill_n="blue",
        scale=scale,
        alpha=0.2,
    )

    ax.set_ylim(-1, 1)
    ax.axis('off')

    plt.show()
    quit()

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
