
*************************************************
Übertragungsbeziehungen der Stabtheorie I Ordnung
*************************************************
.. Note:: 
    todo: Abbildungen

Grundlagen
==========
Ausgangspunkt der Herleitung der Übertragungsbeziehungen von Stäben mit linear veränderlicher Höhe sind die die Differentialgleichungen :eq:`differential_equations` des Biegeproblems 
der Stabtheorie I. Ordnung

.. math::
    :label: differential_equations

    \frac{dV(x)}{dx} &= -q(x) \\[1em] 
    \frac{dM(x)}{dx} &= V(x) + m(x)\\[1em]            
    \frac{d\varphi (x)}{dx} &= -\left[\frac{M(x)}{EI(x)}+\kappa (x)\right]\\[1em] 
    \frac{dw (x)}{dx} &= \varphi (x) 

.. Important:: 
    Die Differnetialgleichungen sind spezialisiert für den Fall der Schubstarrheit :math:`G\tilde{A}(x)=\infty`

Integrationsschritte
--------------------
Die gesuchten, von x abhängigen, Zustandsgrößen ergeben sich durch Schritt für Schritt aufintegrieren und einsetzen der Differnetialgleichungen :eq:`differential_equations`.
Nach jedem Integrationsschritt werden die Integrationskonstanten auf die andere Seite gebracht sowie die lastabhängigen Terme zu sogenannte 
Lastglieder zusammengefasst. (todo: ref Funktion load_integrals). Zusätzlich wird zur Vereinfachung der Integrale die dimensionslose Funktion :math:`f(x)` eingeführt.

.. math::
    :label: iteration_steps

    V(x) &= V_i - \underbrace{\int_0^x q(x)~dx}_{V^L(x)} = V_i + V^L(x)\\[1em]
    M(x) &= M_i + V_i~x + \underbrace{\int_0^x V^L(x) + m(x)~dx}_{M^L(x)} =  M_i + V_i~x + M^L(x)\\[1em]
    \varphi(x) &= \varphi_i - \frac{M_i}{EI_i}\underbrace{\int_0^x\frac{1}{f(x)}~dx}_{b'_2(x)} - \frac{V_i}{EI_i}\underbrace{\int_0^x\frac{x}{f(x)}~dx}_{b'_3(x)} - \underbrace{\int_0^x\left[\frac{M^L(x)}{EI_i~f(x)}~dx+\kappa(x)\right]}_{\varphi^L(x)}\\[1em]
    w(x) &= w_i + \varphi_i~x - \frac{M_i}{EI_i}\underbrace{\iint_0^x\frac{1}{f(x)}~dx~dx}_{b_2(x)}- \frac{V_i}{EI_i}\underbrace{\iint_0^x\frac{x}{f(x)}~dx~dx}_{b_3(x)} + \underbrace{\int_0^x\varphi^L(x)~dx}_{w^L(x)}


Zusammenfassen zu den Übertragungsbeziehungen
---------------------------------------------
Durch das Anschreiben der Gleichungen aus :eq:`iteration_steps` in Matrix Vektor Notation ergeben sich die Übertragungsbeziehungen für einen Stab mit linear veränderlicher Höhe
vom Stabanfang bis zu einem beliebigen Punkt x zu:

.. math::
    :label: transferrelations_height_eq

    \underbrace{\left[\begin{array}{c}
                        w(x)\\
                       \varphi(x) \\
                        M(x)\\
                        V(x)\\
                        1
                        \end{array}
                        \right]}_{\vec{Z_x}}
                        =
                        \underbrace{\left[\begin{array}{ccccc}
                        1&x&-b_2/EI_i&-b_3/EI_i&w^L(x)\\
                        0&1&-b'_2/EI_i&-b'_3/EI_i&\varphi^L(x)\\
                        0&0&1&x&M^L(x)\\
                        0&0&0&1&V^L(x)\\
                        0&0&0&0&1\\
                        \end{array}
                        \right]}_{\boldsymbol{F_{xi}}}\cdot\underbrace{\left[\begin{array}{c}
                        w_i\\
                       \varphi_i\\
                        M_i\\
                        V_i\\
                        1
                        \end{array}
                        \right]}_{\vec{Z_i} }


Zweigliedrige Stabkonstruktion
==============================

.. figure:: static/transfer_relation/system2.PNG
    :align: center
    :figwidth: 700px



Handstatik
----------
::

    import stanpy as stp 
    from sympy.abc import x

    E = 3*10**7 # kN/m²
    q = 10 # kN/m
    l = 2 # m

    b, ha, hb, hc = 0.2, 0.3, 0.3, 0.4 # m 
    hx = ha+(hb-ha)/l*x # m 

    cs1_props = stp.cs(b=b, h=ha)
    cs2_props = stp.cs(b=b, h=hx)

    s_1 = {"l":l, "q":q, "E":E, "I":cs1_props["I"]} 
    s_2 = {"l":l, "q":q, "E":E, "I":cs2_props["I"]} 

    f_ba = stp.tr(s1)
    f_cb = stp.tr(s2)  
    f_ca = f_cb * f_ba 

    z_a = {"w":0, "M":0}
    z_c = {"w":0, "phi":0}

    z_c, z_a = stp.solve_tr(z_c, f_ca, z_a)
    z_b = f_ba*z_a

    s_1 = stp.inject_bc(s_1, z_a, z_b)
    s_2 = stp.inject_bc(s_2, z_b, z_c)

Development-Box
---------------
.. Note:: 
    Definition der Variablen

    für jeden Stab:
        berechnen der Querschnittswerte
        berechnen der b Integrale
        berechnen der Lastintegrale
        einsetzen in Übertragungsbeziehung
    
    Definition der Randbedingunen
    zusammenführen der Übertragungsbeziehungen
    Solven der Übertragungsbeziehungen


::

    import stanpy as stp 
    from sympy.abc import x

    E = 3*10**7 # kN/m²
    q = 10 # kN/m
    l = 2 # m

    b, ha, hb, hc = 0.2, 0.3, 0.3, 0.4 # m 
    hx = ha+(hb-ha)/l*x # m 

    cs1_prop = stp.cs(b=b, h=ha)
    cs2_prop = stp.cs(b=b, h=hx)

    s_1 = {"l":l, "q":q, "E":E, "I":cs1_prop["I"]} 
    s_2 = {"l":l, "q":q, "E":E, "I":cs2_prop["I"]} 

    f_ba = stp.tr(s1)
    f_cb = stp.tr(s2)  
    f_ca = f_cb * f_ba 

    z_a = {"w":0, "M":0}
    z_c = {"w":0, "phi":0}

    z_c, z_a = stp.solve_tr(z_c, f_ca, z_a)
    z_b = f_ba*z_a

    s_1 = stp.inject_bc(s_1, z_a, z_b)
    s_2 = stp.inject_bc(s_2, z_b, z_c)

Black-Box
---------
::

    import stanpy as stp 
    from sympy.abc import x

    E = 3*10**7 # kN/m²
    q = 10 # kN/m
    l = 2 # m

    b, ha, hb, hc = 0.2, 0.3, 0.3, 0.4 # m 
    hx = ha+(hb-ha)/l*x # m 

    cs1_prop = stp.cs(b=b, h=ha)
    cs2_prop = stp.cs(b=b, h=hx)

    bc_a = {"w":0, "M":0} # Randbedingung in a
    bc_c = {"w":0, "phi":0} # Randbedingung in c

    s_1 = {"l":l, "q":q, "E":E, "I":cs1_prop["I"], "bci":bc_a} 
    s_2 = {"l":l, "q":q, "E":E, "I":cs2_prop["I"], "bck":bc_c}

    s_1, s_2 = stp.solve(s_1, s_2)


.. meta::
    :description lang=de:
        Examples of document structure features in pydata-sphinx-theme.
