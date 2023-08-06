# -*- coding: utf-8 -*-


import numpy as np

import brainpy.math as bm
from brainpy.dyn.base import ConstantDelay


def test_constant_delay_uniform_no_batch1():
  print()

  cd = ConstantDelay(size=10, delay=2, dt=0.1)
  for i in range(cd.num_step):
    cd.push(bm.ones(cd.size) * i)
    cd.update(0, 0)
  print(cd.pull())
  cd.update(0, 0)
  print(cd.pull())
  cd.update(0, 0)
  a = cd.pull()
  print(a)
  print(type(a))


def test_constant_delay_nonuniform_no_batch1():
  print()

  rng = np.random.RandomState(1234)
  delays = rng.random(10) * 3 + 0.2

  cd = ConstantDelay(size=10, delay=delays, dt=0.1)
  for i in range(cd.num_step.max()):
    cd.push(bm.ones(cd.size) * i)
    cd.update(0, 0)
  print(cd.pull())
  cd.update(0, 0)
  print(cd.pull())
  cd.update(0, 0)
  a = cd.pull()
  print(a)
  print(type(a))
