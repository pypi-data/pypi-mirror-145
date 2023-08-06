========================
stanpy.transfer_relation
========================
utils
=====
gamma_K
-------

.. jupyter-execute::
    :hide-code:

    import numpy as np
    np.set_printoptions(precision=5)

.. automodule:: stanpy
    :members: gamma_K

.. math::
    :label: gamma_and_K

    \gamma = \dfrac{1}{1 - N / G\tilde{A}}\qquad
    K = -\gamma\dfrac{N}{EI}

.. jupyter-execute::

    import stanpy as stp

    s = {"EI":32000, "GA":20000, "N":-1000}
    gamma, K = stp.gamma_K(**s)
    print(gamma, K)

aj(x)
-----
.. automodule:: stanpy
    :members: aj

.. math::
    :label: aj_coeffs

    x \geq 0&:\quad a_0 = 1,\quad a_j = \dfrac{x^j}{j!} \qquad\text{for}\qquad j=1,~2,~3,~...\\
    x < 0&:\quad \text{all}\quad a_j=0

.. jupyter-execute::

    import stanpy as stp

    aj = stp.aj(x=[-1,0,2,3],n=5)
    print(aj)

bj(x)
-----
.. automodule:: stanpy
    :members: bj

for beams with constant crossections :cite:p:`1993:rubin`:

.. math::
    :label: bj_recursion_constant

    b_j = \sum_{i=0}^{\infty}\beta_i \qquad \beta_i = \dfrac{K x^2}{(j+2i)(j+2i-1)}\beta_{i-1} \qquad \text{with}\qquad i=1,~2,~3,~...,~t

.. jupyter-execute::

    import stanpy as stp

    s = {"EI":32000, "GA":20000, "N":-1000}
    bj = stp.bj(x=[-1,0,2,3],**s)
    print(bj)

for beams with non-constant crossections :cite:p:`1993:rubin`:

.. math::
    :label: bj_recursion_non_constant

    \beta_{0,0} &= 1,~\beta_{0,1}~\text{to}~\beta_{0,p-1}=0\\[1em]
    t &= 1,2,3...:~s=j+t,~e=\dfrac{x}{s-n}\\[1em]
    r &= 1~\text{to}~ p:\beta_{t,r}=e~\beta_{t-1, r-1}\\[1em]
    \beta_{t,0} &= K_i\beta_{t,2}-\sum_{r=1}^{p}\dfrac{(s-2)!}{(s-2-r)!}\beta_{t,r}\eta_r  \qquad\text{with}\qquad \dfrac{EI}{EI_i}=\eta=1+\sum_{r=1}^{p}x^r\eta_r\\[1em]
    b_j^{(n)} &= a_{j-n} \sum_{i=0}^{\infty}\beta_{t,0}

.. Note:: 
    for the :math:`\eta_r` coefficients in :eq:`bj_recursion_non_constant` see :meth:`stanpy.cross_section.cs`

.. jupyter-execute::

    import sympy as sym
    import stanpy as stp

    x = sym.Symbol("x")
    E = 32000  # kN/m2
    b = 0.2  # m
    ha = hb = 0.3  # m
    hc = 0.4  # m
    l = 4  # m
    hx = ha + (hc - hb) / l * x

    cs_props = stp.cs(b=b, h=ha)
    s = {"E": E, "cs": cs_props, "l": l}
    bj = stp.bj(x=[-1,0,2,3,4],**s)
    print(bj)

tr(x)
-----
.. automodule:: stanpy
    :members: tr

.. jupyter-execute::

    import stanpy as stp

    l = 5 #m
    s = {"EI":32000, "GA":20000, "l":l, "q":2}
    Fik = stp.tr(s, x=[0,l/2,l])
    print(Fik)

.. jupyter-execute::

    import stanpy as stp

    l = 5 #m
    s1 = {"EI":32000, "GA":20000, "l":l, "q":2}
    s2 = {"EI":32000, "GA":20000, "l":l, "q":2}
    s = [s1,s2]
    
    Fik = stp.tr(*s, x=np.linspace(0, 2*l, 3))
    print(Fik)

transfer relations constant cross-section
=========================================
load integrals Q (shear-force-representation)
---------------------------------------------
.. automodule:: stanpy
    :members: calc_load_integral_Q

.. jupyter-execute::

    import stanpy as stp

    l = 5 #m
    s = {"EI":32000, "GA":20000, "l":l, "q":2}
    load_integral_Q = stp.calc_load_integral_Q(x=[0,l/2,l],**s)
    print(load_integral_Q)

.. math::
    :label: load_Q_constant_wQ

    w^Q &= \gamma\sum_0\left(\dfrac{b_{j+4}}{EI}-\dfrac{b_{j+2}}{G\tilde{A}}\right)~\overline{q_j}-\dfrac{\gamma}{EI}\sum_{0}b_{j+3}m_j-\gamma\sum_{0}b_{j+2}\kappa_j^e\\[1em]
        &+ \gamma\left(\dfrac{b_4^*-b_4^{**}}{EI}-\dfrac{b_2^*-b_2^{**}}{G\tilde{A}}\right)q_{\Delta}+\gamma\left(\dfrac{b_3^*}{EI}-\dfrac{b_1^*}{G\tilde{A}}\right)P-\gamma\dfrac{b_2^*}{EI}-\gamma b_1^*\phi^e+b_0^*W^e

.. math::
    :label: load_Q_constant_phiQ

    \varphi^Q &=  \dfrac{\gamma}{EI}\sum_0b_{j+3}~\overline{q_j}-\dfrac{1}{EI}\sum b_{j+2}m_j-\sum_0 b_{j+1}\kappa_j^e\\[1em]
    &+\gamma\dfrac{b_3^*-b_3^{**}}{EI}q_{\Delta}+\gamma\dfrac{b_2^*}{EI}P-\dfrac{b_1^*}{EI}M^e-b_0^*\phi^e+\dfrac{K}{\gamma}b_1^*W^e

.. math::
    :label: load_Q_constant_MQ

    M^Q &= -\gamma\sum_0 b_{j+2}~\overline{q_j}+\sum_0 b_{j+1} m_j - \gamma N \sum_0 b_{j+2} \kappa_j^e\\[1em]
        &-\gamma\left(b_2^*-b_2^{**}\right)q_{\Delta}-\gamma b_1^*P+b_0^*M^e-\gamma N b_1^*\phi^e + Nb_0^*W^e

.. math::
    :label: load_Q_constant_QQ

    Q^Q &= -\gamma\sum_0 b_{j+1}~\overline{q_j}+K\sum_0 b_{j+2}m_j+\gamma N \sum_0 b_{j+1}\kappa_j^e\\[1em]
        &-\gamma\left(b_1^*-b_1^{**}\right)q_{\Delta}-\gamma b_0^*P+K b_1^*M^e-\gamma N b_0^*\phi^e+N K b_1^* W^e

.. math::
    :label: q_j_hat

    \overline{q_j} = q_j-N w_{j+2}^v

.. math::
    :label: w_V

    w_1^V = \psi^0+4\dfrac{w^0}{l} \qquad w_2^V = -8\dfrac{w^0}{l^2}


field matrix Q (shear-force-representation)
-------------------------------------------
.. automodule:: stanpy
    :members: tr_Q

.. jupyter-execute::

    import stanpy as stp

    l = 5 #m
    s = {"EI":32000, "GA":20000, "l":l, "q":2}
    Fik = stp.tr_Q(**s)
    print(Fik)

.. math::
    :label: field_Q_constant

    F_{ik}^Q = 
    \begin{bmatrix}
			1& x & -\gamma\dfrac{b_2}{EI}&-\gamma\left(\dfrac{b_3}{EI}-\dfrac{b_1}{G\tilde{A}}\right)&w^Q\\
			0& 1 & -\dfrac{b_1}{EI}&-\dfrac{b_2}{EI}&\varphi^Q\\
			0& 0 & b_0& b_1&M^Q\\
			0& 0 & K b_1& b_0&Q^Q\\
			0& 0 & 0& 0&1
	\end{bmatrix}


load integrals R (transverse-force-representation)
--------------------------------------------------
.. automodule:: stanpy
    :members: calc_load_integral_R

.. jupyter-execute::

    import stanpy as stp

    l = 5 #m
    s = {"EI":32000, "GA":20000, "l":l, "q":2, "N":-1000}
    load_integral_R = stp.calc_load_integral_R(x=[0,l/2,l],**s)
    print(load_integral_R)

.. math::
    :label: load_Q_constant_wR

    w^R = w^Q-\gamma\left(\dfrac{b_3}{EI}-\dfrac{b_1}{G\tilde{A}}\right)N w_1^V

.. math::
    :label: load_Q_constant_phiR

    \varphi^R = \varphi^Q-\gamma\dfrac{b_2}{EI} N w_1^V

.. math::
    :label: load_Q_constant_MR

    M^R = M^Q+\gamma b_1 N w_1^V

.. math::
    :label: load_Q_constant_RR

    R^R = -\sum_0 a_{j+1}q_j-(a_1^*-a_1^{**})q_{\Delta}-a_0^*P


field matrix R (transverse-force-representation)
------------------------------------------------
.. automodule:: stanpy
    :members: tr_R

.. jupyter-execute::

    import stanpy as stp

    l = 5 #m
    s = {"EI":32000, "GA":20000, "l":l, "q":2, "N":-1000}
    Fik = stp.tr_R(**s)
    print(Fik)

.. math::
    :label: field_R_constant

    F_{ik}^R = 
    \begin{bmatrix}
			1&\gamma b_1 & -\gamma\dfrac{b_2}{EI}&-\gamma\left(\dfrac{b_3}{EI}-\dfrac{b_1}{G\tilde{A}}\right)&w^R\\
			0& b_0 & -\dfrac{b_1}{EI}&-\gamma\dfrac{b_2}{EI}&\varphi^R\\
			0& \gamma N b_1 & b_0& \gamma b_1&M^R\\
			0& 0 & 0& 1&R^R\\
			0& 0 & 0& 0&1
	\end{bmatrix}

transfer relations non constant cross-section
=============================================
load integrals Q (shear-force-representation)
---------------------------------------------
.. automodule:: stanpy
    :members: calc_load_integral_Q_poly

.. jupyter-execute::

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

.. math::
    :label: load_Q_non_constant_wQ

    w^Q &= \dfrac{1}{EI_i}\sum_0 b_{j+4}~\overline{q}_j-\dfrac{1}{EI_i}\sum_0 b_{j+3}~m_j-\kappa_i^e\sum_{r=0}^{p_\gamma}b_{r+2}~\gamma_r\\
    &+\left(\dfrac{b_4^*}{EI^*}-\dfrac{b_4^{**}}{EI^{**}}\right)q_\Delta+\dfrac{b_3^*}{EI^*}P-\dfrac{b_2^*}{EI^*}M^e-b_1^*\phi^e+b_0^*W^e

.. math::
    :label: load_Q_non_constant_phiQ

    \varphi^Q &= \dfrac{1}{EI_i}\sum_0 b'_{j+4}~\overline{q}_j-\dfrac{1}{EI_i}\sum_0 b'_{j+3}~m_j-\kappa_i^e\sum_{r=0}^{p_\gamma}b'_{r+2}~\gamma_r\\
    &+\left(\dfrac{b_4^{'*}}{EI^*} -\dfrac{b_4^{'**}}{EI^{**}}\right)q_\Delta+\dfrac{b_3^{'*}}{EI^*}P-\dfrac{b_2^{'*}}{EI^*}M^e-b_1^{'*}\phi^e+b_0^{'*}W^e

.. math::
    :label: load_Q_non_constant_MQ

    M^Q = -\sum_0 a_{j+2}\overline{q}_j+\sum_0 a_{j+1}m_j-\left(a_2^*-a_2^{**}\right)q_\Delta-a_1^*P+a_0^*M^e-N w^Q

.. math::
    :label: load_Q_non_constant_QQ

    Q^Q = -\sum_0 a_{j+1}\overline{q}_j-\left(a_1^*-a_1^{**}\right)q_\Delta-a_0^*P-N \varphi^Q

field matrix Q (shear-force-representation)
-------------------------------------------
.. automodule:: stanpy
    :members: tr_Q_poly

.. jupyter-execute::

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

.. math::
    :label: field_Q_constant

    F_{ik}^Q = 
    \begin{bmatrix}
			1& x & -\dfrac{b_2}{EI_i}&-\dfrac{b_3}{EI_i} & w^Q\\
			0& 1 & -\dfrac{b'_2}{EI_i}&-\dfrac{b'_3}{EI_i}& \varphi^Q\\
			0& 0 & b_0& b_1&M^Q\\
			0& 0 & K b'_0& b'_1&Q^Q\\
			0& 0 & 0& 0&1
	\end{bmatrix}

load integrals R (transverse-force-representation)
--------------------------------------------------
.. automodule:: stanpy
    :members: calc_load_integral_R_poly

.. jupyter-execute::

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

.. math::
    :label: load_R_non_constant_wR

    w^R = w^Q + \dfrac{b_3}{EI_i}N w_1^V

.. math::
    :label: load_R_non_constant_phiR

    \varphi^R = \varphi^Q + \dfrac{b'_3}{EI_i} N w_1^V

.. math::
    :label: load_R_non_constant_MR

    M^R = M^Q - b_1 N w_1^V

.. math::
    :label: load_R_non_constant_QR

    R^R = -\sum_0 a_{j+1}q_j-\left(a_1^*-a_1^{**}\right)q_\Delta-a_0^* P

field matrix R (transverse-force-representation)
------------------------------------------------
.. automodule:: stanpy
    :members: tr_R_poly

.. jupyter-execute::

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

.. math::
    :label: field_R_constant

    F_{ik}^R = 
    \begin{bmatrix}
			1 & b_1 & -\dfrac{b_2}{EI_i} &-\dfrac{b_3}{EI_i} &w^Q\\
			0 & b'_1 & -\dfrac{b'_2}{EI_i} &-\dfrac{b'_3}{EI_i}&\varphi^Q\\
			0 & - N b_1 & b_0 & b_1 & M^Q\\
			0 & 0 & 0 & 1 & R^Q\\
			0 & 0 & 0 & 0 & 1
	\end{bmatrix}


Citations
=========
.. bibliography::