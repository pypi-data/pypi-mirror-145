#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sympy as sym
import matplotlib.pyplot as plt
import stanpy as stp

x = sym.Symbol("x")
l = 4  # m
b, ha, hb = 0.2, 0.3, 0.4  # m
hx = ha + (hb - ha) / l * x  # m

cs_props = stp.cs(b=b, h=hx)

print(cs_props)
print("I_y(0) = ", cs_props["I_y"](0))
print("I_y(l) = ", cs_props["I_y"](l))

offset = 0.2
fig, ax = plt.subplots()
stp.plot_cs(ax, b, hx.subs(x, 0))
stp.plot_cs(ax, b, hx.subs(x, l), dy=0.3)

ax.set_xlim(-offset, b + offset)
ax.set_ylim(-offset, float(hx.subs(x, l)) + offset)
ax.grid(linestyle=":")
ax.axis('equal')

plt.show()


# In[2]:


import numpy as np
import sympy as sym
import stanpy as stp

x = sym.Symbol("x")
l = 4  # m
s, t = 0.012, 0.02  # m
b, ha, hb = 0.2, 0.3, 0.4  # m
hx = ha + (hb - ha) / l * x  # m

b_v = np.array([b, s, b])
h_v = np.array([t, hx, t])
zsi_v = np.array([t / 2, t + hx/ 2, t + hx + t / 2])  # von OK
ysi_v = np.array([b / 2, b / 2, b / 2])  # von Links

cs_props = stp.cs(b=b_v, h=h_v, y_si=ysi_v, z_si=zsi_v)

print(cs_props)
print("I_y(0) = ", cs_props["I_y"](0))
print("I_y(l) = ", cs_props["I_y"](l))

h_v_fun = sym.lambdify(x, h_v, 'numpy')
zsi_v_fun = sym.lambdify(x, zsi_v, 'numpy')

offset = 0.2
fig, ax = plt.subplots()
stp.plot_cs(ax, b_v, h_v_fun(0), ysi_v, zsi_v_fun(0))
stp.plot_cs(ax, b_v, h_v_fun(l), ysi_v, zsi_v_fun(l), dy=0.3)

ax.set_xlim(-offset, b + offset)
ax.set_ylim(-offset, float(hx.subs(x, l)) + offset)
ax.grid(linestyle=":")
ax.axis('equal')

plt.show()


# In[3]:


import numpy as np
import sympy as sym
import stanpy as stp

x = sym.Symbol("x")
l = 4  # m
s, t = 0.012, 0.02  # m
b, ha, hb = 0.2, 0.3, 0.4  # m
hx = ha + (hb - ha) / l * x  # m

b_v = np.array([b, s, b])
h_v = np.array([t, hx - 2 * t, t])
zsi_v = stp.AI_z.dot(h_v) # von OK
ysi_v = stp.AI_y.dot(b_v)  # von Links

cs_props = stp.cs(b=b_v, h=h_v, y_si=ysi_v, z_si=zsi_v)

print(cs_props)
print("I_y(0) = ", cs_props["I_y"](0))
print("I_y(l) = ", cs_props["I_y"](l))

h_v_fun = sym.lambdify(x, h_v, 'numpy')
zsi_v_fun = sym.lambdify(x, zsi_v, 'numpy')

offset = 0.2
fig, ax = plt.subplots(1)
stp.plot_cs(ax, b_v, h_v_fun(0), ysi_v, zsi_v_fun(0))
stp.plot_cs(ax, b_v, h_v_fun(l), ysi_v, zsi_v_fun(l), dy=0.3)

ax.set_xlim(-offset, b + offset)
ax.set_ylim(-offset, float(hx.subs(x, l)) + offset)
ax.grid(linestyle=":")
ax.axis('equal')

plt.show()


# In[4]:


import numpy as np
import sympy as sym
import stanpy as stp

x = sym.Symbol("x")
l = 4  # m
s, t = 0.012, 0.02  # m
ba, bb, ha, hb = 0.3, 0.4, 0.3, 0.4  # m
hx = ha + (hb - ha) / l * x  # m
bx = ba + (bb - ba) / l * x  # m

b_v = np.array([t, hx - 2 * t, t])
h_v = np.array([bx, s, bx])
zsi_v = stp.AH_z.dot(h_v)  # von OK
ysi_v = stp.AH_y.dot(b_v)  # von Links

cs_props = stp.cs(b=b_v, h=h_v, y_si=ysi_v, z_si=zsi_v)

print(cs_props)
print("I_y(0) = ", cs_props["I_y"](0))
print("I_y(l) = ", cs_props["I_y"](l))

b_v_fun = sym.lambdify(x, b_v, 'numpy')
h_v_fun = sym.lambdify(x, h_v, 'numpy')
zsi_v_fun = sym.lambdify(x, zsi_v, 'numpy')
ysi_v_fun = sym.lambdify(x, ysi_v, 'numpy')

offset = 0.2
fig, ax = plt.subplots(1)
stp.plot_cs(ax, b_v_fun(0), h_v_fun(0), ysi_v_fun(0), zsi_v_fun(0))
stp.plot_cs(ax, b_v_fun(l), h_v_fun(l), ysi_v_fun(l), zsi_v_fun(l), dy=0.4)

ax.grid(linestyle=":")
ax.axis('equal')

plt.show()


# In[5]:


import numpy as np
import sympy as sym
import stanpy as stp

x = sym.Symbol("x")
l = 4  # m
s, t = 0.012, 0.02  # m
b, ha, hb = 0.3, 0.3, 0.4  # m
hx = ha + (hb - ha) / l * x  # m

b_v = np.array([b, s, s, b])
h_v = np.array([t, hx - 2 * t, hx - 2 * t, t])
zsi_v = stp.AK_z.dot(h_v)  # von OK
ysi_v = stp.AK_y.dot(b_v)  # von Links

cs_props = stp.cs(b=b_v, h=h_v, y_si=ysi_v, z_si=zsi_v)

h_v_fun = sym.lambdify(x, h_v, 'numpy')
zsi_v_fun = sym.lambdify(x, zsi_v, 'numpy')

offset = 0.2
fig, ax = plt.subplots()
stp.plot_cs(ax, b_v, h_v_fun(0), ysi_v, zsi_v_fun(0))
stp.plot_cs(ax, b_v, h_v_fun(l), ysi_v, zsi_v_fun(l), dy=0.4)

ax.set_xlim(-offset, b + offset)
ax.set_ylim(-offset, float(hx.subs(x, l)) + offset)
ax.grid(linestyle=":")
ax.axis('equal')

plt.show()


# In[6]:


import numpy as np
import sympy as sym
import stanpy as stp

x = sym.Symbol("x")
l = 4  # m
s, t = 0.012, 0.02  # m
b, ha, hb = 0.3, 0.3, 0.4  # m
hx = ha + (hb - ha) / l * x  # m

b_v = np.array([b, s, s, b])
h_v = np.array([t, hx - 2 * t, hx - 2 * t, t])
h_i = 0.05

b_v = np.array([b, s, b, s, s, s, s])
h_v = np.array([t, hx - 2 * t, t, h_i, h_i, h_i, h_i])
zsi_v = stp.AI_zp.dot(h_v)  # von OK
ysi_v = stp.AI_yp.dot(b_v)  # von Links

cs_props = stp.cs(b=b_v, h=h_v, y_si=ysi_v, z_si=zsi_v)

print(cs_props)

h_v_fun = sym.lambdify(x, h_v, 'numpy')
zsi_v_fun = sym.lambdify(x, zsi_v, 'numpy')

offset = 0.2
fig, ax = plt.subplots()
stp.plot_cs(ax, b_v, h_v_fun(0), ysi_v, zsi_v_fun(0))
stp.plot_cs(ax, b_v, h_v_fun(l), ysi_v, zsi_v_fun(l), dy=0.4)

ax.set_xlim(-offset, b + offset)
ax.set_ylim(-offset, float(hx.subs(x, l)) + offset)
ax.grid(linestyle=":")
ax.axis('equal')

plt.show()

