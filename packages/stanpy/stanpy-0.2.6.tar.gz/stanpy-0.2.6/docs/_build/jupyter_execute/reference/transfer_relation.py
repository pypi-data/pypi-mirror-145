#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
np.set_printoptions(precision=5)


# In[2]:


import stanpy as stp

s = {"EI":32000, "GA":20000, "N":-1000}
gamma, K = stp.gamma_K(**s)
print(gamma, K)


# In[3]:


import stanpy as stp

aj = stp.aj(x=[-1,0,2,3],n=5)
print(aj)


# In[4]:


import stanpy as stp

s = {"EI":32000, "GA":20000, "N":-1000}
bj = stp.bj(x=[-1,0,2,3],**s)
print(bj)


# In[5]:


import sympy as sym
import stanpy as stp

x = sym.Symbol("x")
E = 32000  # kN/m2
b = 0.2  # m
ha = hb = 0.3  # m
hc = 0.4  # m
l = 4  # m
hx = ha + (hc - hb) / l * x

cs_props = stp.cs(b=b, h=hx)
s = {"E": E, "cs": cs_props, "l": l}
bj = stp.bj(x=[-1,0,2,3,4],**s)
print(bj)


# In[6]:


import sympy as sym
import stanpy as stp

x = sym.Symbol("x")
E = 32000  # kN/m2
b = 0.2  # m
ha = hb = 0.3  # m
hc = 0.4  # m
l = 4  # m
q = 5 # kN/m
hx = ha + (hc - hb) / l * x

cs_props = stp.cs(b=b, h=hx)
s = {"E": E, "cs": cs_props, "l": l, "q":q}
li = stp.load_integral(x=[-1,0,2,3,4],**s)
print(li)


# In[7]:


import stanpy as stp

l = 5 #m
s = {"EI":32000, "GA":20000, "l":l, "q":2}
Fik = stp.tr(s, x=[0,l/2,l])
print(Fik)


# In[8]:


import stanpy as stp

l = 5 #m
s1 = {"EI":32000, "GA":20000, "l":l, "q":2}
s2 = {"EI":32000, "GA":20000, "l":l, "q":2}
s = [s1,s2]

Fik = stp.tr(*s, x=np.linspace(0, 2*l, 3))
print(Fik)


# In[9]:


import stanpy as stp

l = 5 #m
s = {"EI":32000, "GA":20000, "l":l, "q":2}
load_integral_Q = stp.calc_load_integral_Q(x=[0,l/2,l],**s)
print(load_integral_Q)


# In[10]:


import stanpy as stp

l = 5 #m
s = {"EI":32000, "GA":20000, "l":l, "q":2}
Fik = stp.tr_Q(**s)
print(Fik)


# In[11]:


import stanpy as stp

l = 5 #m
s = {"EI":32000, "GA":20000, "l":l, "q":2, "N":-1000}
load_integral_R = stp.calc_load_integral_R(x=[0,l/2,l],**s)
print(load_integral_R)


# In[12]:


import stanpy as stp

l = 5 #m
s = {"EI":32000, "GA":20000, "l":l, "q":2, "N":-1000}
Fik = stp.tr_R(**s)
print(Fik)


# In[13]:


import stanpy as stp

x = sym.Symbol("x")
E = 3*10**7  # kN/m2
b = 0.2  # m
hi = 0.3  # m
hk = 0.4  # m
l = 3  # m
hx = hi + (hk - hi) / l * x

cs_props = stp.cs(b=b, h=hx)
s = {"E": E, "cs": cs_props, "l": l, "q":10}
load_integral_Q = stp.calc_load_integral_Q_poly(x=[0,l/2,l],**s)

print(load_integral_Q)


# In[14]:


import stanpy as stp

x = sym.Symbol("x")
E = 3*10**7  # kN/m2
b = 0.2  # m
hi = 0.3  # m
hk = 0.4  # m
l = 3  # m
hx = hi + (hk - hi) / l * x

cs_props = stp.cs(b=b, h=hx)
s = {"E": E, "cs": cs_props, "l": l, "q":10}

Fik = stp.tr_Q_poly(**s)
print(Fik)


# In[15]:


import stanpy as stp

x = sym.Symbol("x")
E = 3*10**7  # kN/m2
b = 0.2  # m
hi = 0.3  # m
hk = 0.4  # m
l = 3  # m
hx = hi + (hk - hi) / l * x

cs_props = stp.cs(b=b, h=hx)
s = {"E": E, "cs": cs_props, "l": l, "q":10, "N":-1000}
load_integral_R = stp.calc_load_integral_R_poly(x=[0,l/2,l],**s)

print(load_integral_R)


# In[16]:


import stanpy as stp

x = sym.Symbol("x")
E = 3*10**7  # kN/m2
b = 0.2  # m
hi = 0.3  # m
hk = 0.4  # m
l = 3  # m
hx = hi + (hk - hi) / l * x

cs_props = stp.cs(b=b, h=hx)
s = {"E": E, "cs": cs_props, "l": l, "q":10, "N":-1000}

Fik = stp.tr_R_poly(**s)
print(Fik)

