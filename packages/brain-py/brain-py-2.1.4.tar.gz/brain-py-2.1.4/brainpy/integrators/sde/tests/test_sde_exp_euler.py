# -*- coding: utf-8 -*-

import brainpy as bp
from brainpy.integrators.sde.normal import ExponentialEuler


def test1():
  p = 0.1

  def lorenz_g(x, y, z, t, sigma=10, beta=8 / 3, rho=28):
    return p * x, p * y, p * z

  def lorenz_f(x, y, z, t, sigma=10, beta=8 / 3, rho=28):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

  ExponentialEuler(f=lorenz_f, g=lorenz_g, dt=0.01,
                   intg_type=bp.integrators.ITO_SDE,
                   wiener_type=bp.integrators.SCALAR_WIENER,
                   var_type=bp.integrators.POP_VAR,
                   show_code=True)
