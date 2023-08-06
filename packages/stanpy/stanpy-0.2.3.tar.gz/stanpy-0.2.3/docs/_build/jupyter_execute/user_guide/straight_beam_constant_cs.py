#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
np.set_printoptions(precision=5)


# In[2]:


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


# In[3]:


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


# In[4]:


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


# In[5]:


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


# In[6]:


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


# In[7]:


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


# In[8]:


dx = 1e-9
x = np.linspace(0, l, 500)
annotation = np.array([2-dx, 2, 3-dx, 3, 4-dx, 4, 6-dx])
x = np.sort(np.append(x, annotation))

Fxa = stp.tr(s, x=x)
Z_a, Z_b = stp.tr_solver(s)
Z_x = Fxa.dot(Z_a)

print("Z_a =", Z_a)
print("Z_b =", Z_b)


# In[9]:


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


# In[10]:


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


# In[11]:


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


# In[12]:


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


# In[13]:


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


# In[14]:


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


# In[15]:


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


# In[16]:


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


# In[17]:


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


# In[18]:


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


# In[19]:


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


# In[20]:


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


# In[21]:


dx = 1e-9
x = np.linspace(0, l, 500)
annotation = np.array([l / 2 - dx, l / 2, l-dx])
x = np.sort(np.append(x, annotation))

Fxa = stp.tr(s, x=x)
Z_a, Z_b = stp.solve_tr(Fxa[-1], **s)
Z_x = Fxa.dot(Z_a)

print("Z_a =", Z_a)
print("Z_b =", Z_b)

w_x = Z_x[:, 0]
phi_x = Z_x[:, 1]
M_x = Z_x[:, 2]
R_x = Z_x[:, 3]

V_x = stp.R_to_Q(x, Z_x, s)


# In[22]:


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


# In[23]:


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


# In[24]:


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


# In[25]:


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


# In[26]:


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

