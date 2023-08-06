import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import stanpy as stp

E = 3e7 # kN/m2
l1 = 12 # m
P = 10 # kN/m

b = 0.2 # m
xs = sym.symbols("x")
hx1 = 13.6*(1+xs*0.2941-0.02451*xs**2)/100
hx2 = 25.6*(1-0.01302*xs**2)/100
cs1 = stp.cs(b=b, h=hx1, pow_series_trunc=10, l=l1)

fixed = {"w":0, "phi":0}
hinged = {"w":0, "M":0, "H":0}

s = {"E":E, "cs":cs1, "l":l1, "bc_i":hinged, "P1":(P, l1/3), "bc_k":fixed}

fig, ax = plt.subplots(figsize=(12,5))
stp.plot_system(ax, s, render=True, facecolor="gray", alpha=0.3, render_scale=1)
stp.plot_load(ax, s, offset=0.1)
ax.set_ylim(-1.5, 2)
ax.set_aspect("equal")
plt.show()

x = np.linspace(0, l1, 1000)
x_annoation = [0,l1, l1, (l1)/2]
x = np.sort(np.append(x, x_annoation))
Fxi = stp.tr(s, x=x)
Zi, Zk = stp.tr_solver(s)
Zx = Fxi.dot(Zi)

scale = 0.5

fig, ax = plt.subplots(figsize=(12, 5))
stp.plot_system(ax, s)
stp.plot_solution(
    ax,
    x=x,
    y=Zx[:,2],
    annotate_x=[],
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