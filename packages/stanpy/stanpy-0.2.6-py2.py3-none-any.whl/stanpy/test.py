import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import stanpy as stp

x_sym = sym.Symbol("x")
E = 3e7  # kN/m2
b = 0.2  # m
ha = hb = 0.3  # m
hc = 0.4  # m
l1 = 4  # m
l2 = 3  # m
hx = ha + (hc - hb) / l2 * x_sym

cs_props1 = stp.cs(b=b, h=ha)
s1 = {"E": E, "cs": cs_props1, "l": l1, "bc_i": {"w": 0, "M": 0, "H": 0}, "P1": (10,l2/3), "P2": (10,2*l2/3)}

cs_props2 = stp.cs(b=b, h=hx)
s2 = {"E": E, "cs": cs_props2, "l": l2, "bc_k": {"w": 0, "phi": 0}, "P1": (10,l2/3), "P2": (10,2.5), "P3": (10,l2/2)}

s = [s1,s2]

fig, ax = plt.subplots(figsize=(12, 5))
stp.plot_system(ax, *s, render=True, facecolor="gray", alpha=0.5, render_scale=0.3)
stp.plot_load(ax, *s)
ax.grid(linestyle=":")
ax.set_axisbelow(True)
ax.set_ylim(-0.75, 1.0)
plt.show()

x = np.linspace(0, l1+l2, 1000)
x_annoation = [0,l1, l1+l2, (l1+l2)/2]
x = np.sort(np.append(x, x_annoation))
F_xa = stp.tr(*s, x=x)
Z_a, Z_c = stp.tr_solver(*s)

Zx = F_xa.dot(Z_a)

# Moment
fig, ax = plt.subplots(figsize=(12,5))
stp.plot_system(ax, *s)
stp.plot_solution(ax, x=x, y=Zx[:,2], annotate_x = [0,x[Zx[:,2]==np.max(Zx[:,2])], l1+l2],flip_y=True, fill_p="red", fill_n="blue", alpha=0.2)
ax.set_ylim(-1.5, 2)
plt.show()