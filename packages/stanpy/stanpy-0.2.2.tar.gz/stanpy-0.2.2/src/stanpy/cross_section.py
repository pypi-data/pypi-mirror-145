__all__ = ['cs', 'I_fun_taylor', 'cs_dict']

import numpy as np
import sympy as sp
from scipy.interpolate import approximate_taylor_polynomial
import pprint


class cs_dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def __str__(self):
        return pprint.pformat(self)


def I_fun_taylor(Ix, deg):
    Ix_fun = sp.lambdify(sp.Symbol("x"), Ix)
    Ix_fun_taylor = approximate_taylor_polynomial(Ix_fun, 0, deg, 1)
    return Ix_fun_taylor


def _is_instance_sympy(param):
    return isinstance(param, (sp.core.mul.Mul, sp.core.add.Add))


def cs_old(**kwargs):

    b = kwargs.get("b", None)
    h = kwargs.get("h", None)
    zsi = kwargs.get("zsi", None)

    cs_dict = {}
    if isinstance(b, np.ndarray) and isinstance(h, np.ndarray) and isinstance(zsi, np.ndarray):
        cs_dict["Iy"], cs_dict["zs"], cs_dict["A"] = cs_params_vec(b, h, zsi)

    elif b != None and h != None:
        cs_dict["Iy"] = b * h**3 / 12
        cs_dict["Iz"] = b**3 * h / 12
        cs_dict["A"] = b * h
        cs_dict["zs"] = h / 2
        cs_dict["ys"] = b / 2
        if _is_instance_sympy(cs_dict["Iy"]):
            cs_dict["Iy"] = cs_dict["Iy"].as_poly()
            cs_dict["eta_y"] = np.flip(
                (cs_dict["Iy"] / cs_dict["Iy"](0)).as_poly().coeffs()
            )  # (todo) Ref - Stahlbauhandbuch P117 - Rubin
            cs_dict["gamma_y"] = (cs_dict["Iy"] / cs_dict["Iy"](0) * h.as_poly()(0) / h).as_poly().coeffs()

        if _is_instance_sympy(cs_dict["Iz"]):
            cs_dict["Iz"] = cs_dict["Iz"].as_poly()
            cs_dict["eta_z"] = np.flip((cs_dict["Iz"] / cs_dict["Iz"](0)).as_poly().coeffs())
            cs_dict["gamma_z"] = (cs_dict["Iz"] / cs_dict["Iz"](0) * h.as_poly()(0) / h).as_poly().coeffs()

    return cs_dict


def cs_params_vec(vb, vh, vzsi, vysi):

    if np.array([vi.shape != vb.shape for vi in [vb, vh, vzsi, vysi]]).any():
        raise Exception(
            "shape of input vectors b.shape = {}, h.shape = {}, vzsi.shape = {}, vysi.shape = {}  are not identical".format(
                vb.shape, vh.shape, vzsi.shape, vysi.shape
            )
        )

    A = np.dot(vb, vh)
    zs = np.matmul(vb * vh, vzsi) / np.matmul(vb, vh)
    ys = np.matmul(vb * vh, vysi) / np.matmul(vb, vh)
    Iy = np.matmul(vb, vh**3) / 12 + np.matmul(vb * vh, vzsi**2) - zs * np.matmul(vb * vh, vzsi)
    Iz = np.matmul(vb**3, vh) / 12 + np.matmul(vb * vh, vysi**2) - ys * np.matmul(vb * vh, vysi)

    cs_params = {}
    cs_params["A"] = A
    cs_params["z_s"] = zs
    cs_params["y_s"] = ys
    cs_params["I_y"] = Iy
    cs_params["I_z"] = Iz
    return cs_params


def cs(**kwargs):
    NoneType = type(None)

    b = kwargs.get("b")
    h = kwargs.get("h")
    zsi = kwargs.get("z_si", None)
    ysi = kwargs.get("y_si", None)
    poly_deg = kwargs.get("poly_deg", 3)
    poly_range = kwargs.get("poly_range", 12)
    validate = kwargs.get("validate", True)
    development_mode = kwargs.get("development_mode", False)

    cs_params = {}

    if (
        isinstance(b, (int, float, sp.core.mul.Mul, sp.core.mul.Add, sp.core.symbol.Symbol, sp.core.numbers.Float))
        and isinstance(h, (int, float, sp.core.mul.Mul, sp.core.mul.Add, sp.core.symbol.Symbol, sp.core.numbers.Float))
        and isinstance(zsi, NoneType)
    ):
        cs_params["A"] = b * h
        cs_params["z_s"] = h / 2
        cs_params["y_s"] = b / 2
        cs_params["I_y"] = b * h**3 / 12
        cs_params["I_z"] = b**3 * h / 12

    elif (
        isinstance(b, np.ndarray)
        and isinstance(h, np.ndarray)
        and isinstance(zsi, NoneType)
        and isinstance(ysi, NoneType)
    ):
        lower_triangle = np.tril(np.ones((b.size, b.size)))
        np.fill_diagonal(lower_triangle, 1 / 2)

        zsi = lower_triangle.dot(h)
        ysi = np.zeros(lower_triangle.shape).dot(b)
        cs_params = cs_params_vec(b, h, zsi, ysi)

    elif (
        isinstance(b, np.ndarray)
        and isinstance(h, np.ndarray)
        and isinstance(zsi, np.ndarray)
        and isinstance(ysi, NoneType)
    ):
        cs_params = cs_params_vec(b, h, zsi, np.zeros(zsi.shape))

    elif (
        isinstance(b, np.ndarray)
        and isinstance(h, np.ndarray)
        and isinstance(ysi, np.ndarray)
        and isinstance(zsi, NoneType)
    ):
        cs_params = cs_params_vec(b, h, np.zeros(ysi.shape), ysi)

    elif (
        isinstance(b, np.ndarray)
        and isinstance(h, np.ndarray)
        and isinstance(ysi, np.ndarray)
        and isinstance(zsi, np.ndarray)
    ):
        cs_params = cs_params_vec(b, h, zsi, ysi)

    # convert symbolic expressions to poly
    if isinstance(cs_params["I_y"], (sp.core.mul.Mul, sp.core.add.Add)):
        poly = I_fun_taylor(cs_params["I_y"], poly_deg)
        if validate:
            lam = sp.lambdify(sp.Symbol("x"), cs_params["I_y"])
            xvals = np.linspace(0, poly_range, 100)
            if np.max(np.abs(lam(xvals) - poly(xvals))) > 1e-9:
                raise Exception(
                    "deviation of taylor polynomial to large - increase poly_deg (default:3) and set a proper poly_range"
                )
        cs_params["I_y"] = poly
        cs_params["eta_y"] = np.flip(poly.c / poly(0))  # (todo) Ref - Stahlbauhandbuch P117 - Rubin

    if isinstance(cs_params["I_z"], (sp.core.mul.Mul, sp.core.add.Add)):
        poly = I_fun_taylor(cs_params["I_z"], poly_deg)
        if validate:
            lam = sp.lambdify(sp.Symbol("x"), cs_params["I_z"])
            xvals = np.linspace(0, poly_range, 100)
            if np.max(np.abs(lam(xvals) - poly(xvals))) > 1e-9:
                raise Exception(
                    "deviation of taylor polynomial to large - increase poly_deg (default:3) and set a proper poly_range"
                )
        cs_params["I_z"] = poly
        cs_params["eta_z"] = np.flip(poly.c / poly(0))  # (todo) Ref - Stahlbauhandbuch P117 - Rubin
        # cs_params["gamma_y"]  = np.flip((cs_params["Iy"]/cs_params["Iy"](0)*h.as_poly()(0)/h).as_poly().coeffs())

    return cs_dict(cs_params)
