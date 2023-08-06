# -*- coding: utf-8 -*-

import unittest

import numpy as np
import pytest

from brainpy import errors
from brainpy.integrators.ode import odeint


class TestExponentialEuler(unittest.TestCase):
  def test1(self):
    def func(m, t, V):
      alpha = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
      beta = 4.0 * np.exp(-(V + 65) / 18)
      dmdt = alpha * (1 - m) - beta * m
      return dmdt

    odeint(method='exponential_euler', show_code=True, f=func)

  def test2(self):
    with pytest.raises(errors.CodeError):
      def func(f, t, V):
        alpha = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
        beta = 4.0 * np.exp(-(V + 65) / 18)
        dmdt = alpha * (1 - f) - beta * f
        return dmdt

      odeint(method='exponential_euler', show_code=True, f=func)

  def test3(self):
    with pytest.raises(errors.CodeError):
      def func(m, t, dt):
        alpha = 0.1 * (dt + 40) / (1 - np.exp(-(dt + 40) / 10))
        beta = 4.0 * np.exp(-(dt + 65) / 18)
        dmdt = alpha * (1 - m) - beta * m
        return dmdt

      odeint(method='exponential_euler', show_code=True, f=func)

  def test4(self):
    with pytest.raises(errors.CodeError):
      def func(m, t, m_new):
        alpha = 0.1 * (m_new + 40) / (1 - np.exp(-(m_new + 40) / 10))
        beta = 4.0 * np.exp(-(m_new + 65) / 18)
        dmdt = alpha * (1 - m) - beta * m
        return dmdt

      odeint(method='exponential_euler', show_code=True, f=func)

  def test5(self):
    with pytest.raises(errors.CodeError):
      def func(m, t, exp):
        alpha = 0.1 * (exp + 40) / (1 - np.exp(-(exp + 40) / 10))
        beta = 4.0 * np.exp(-(exp + 65) / 18)
        dmdt = alpha * (1 - m) - beta * m
        return dmdt

      odeint(method='exponential_euler', show_code=True, f=func)

  def test6(self):
    with pytest.raises(errors.CodeError):
      def func(math, t, exp):
        alpha = 0.1 * (exp + 40) / (1 - np.exp(-(exp + 40) / 10))
        beta = 4.0 * np.exp(-(exp + 65) / 18)
        dmdt = alpha * (1 - math) - beta * math
        return dmdt

      odeint(method='exponential_euler', show_code=True, f=func)
