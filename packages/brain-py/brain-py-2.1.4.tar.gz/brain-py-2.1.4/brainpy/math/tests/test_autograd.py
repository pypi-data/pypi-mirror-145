# -*- coding: utf-8 -*-


import unittest
from pprint import pprint

import jax
import jax.numpy as jnp
import pytest

import brainpy as bp
import brainpy.math as bm
from brainpy.math.autograd import _jacfwd


class TestPureFuncGrad(unittest.TestCase):
  def test_grad_pure_func_1(self):
    def call(a, b, c): return bm.sum(a + b + c)

    bm.random.seed(1)
    a = bm.ones(10)
    b = bm.random.randn(10)
    c = bm.random.uniform(size=10)
    f_grad = bm.grad(call, argnums=[0, 1, 2])
    grads = f_grad(a, b, c)

    for g in grads: assert (g == 1.).all()

  def test_grad_pure_func_2(self):
    def call(a, b, c): return bm.sum(a + b + c)

    bm.random.seed(1)
    a = bm.ones(10)
    b = bm.random.randn(10)
    c = bm.random.uniform(size=10)
    f_grad = bm.grad(call)
    assert (f_grad(a, b, c) == 1.).all()

  def test_grad_pure_func_aux1(self):
    def call(a, b, c):
      return bm.sum(a + b + c), (bm.sin(100), bm.exp(0.1))

    bm.random.seed(1)
    f_grad = bm.grad(call, argnums=[0, 1, 2])
    with pytest.raises(TypeError):
      f_grad(bm.ones(10), bm.random.randn(10), bm.random.uniform(size=10))

  def test_grad_pure_func_aux2(self):
    def call(a, b, c):
      return bm.sum(a + b + c), (bm.sin(100), bm.exp(0.1))

    bm.random.seed(1)
    f_grad = bm.grad(call, argnums=[0, 1, 2], has_aux=True)
    grads, aux = f_grad(bm.ones(10), bm.random.randn(10), bm.random.uniform(size=10))
    for g in grads: assert (g == 1.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)

  def test_grad_pure_func_return1(self):
    def call(a, b, c): return bm.sum(a + b + c)

    bm.random.seed(1)
    a = bm.ones(10)
    b = bm.random.randn(10)
    c = bm.random.uniform(size=10)
    f_grad = bm.grad(call, return_value=True)
    grads, returns = f_grad(a, b, c)
    assert (grads == 1.).all()
    assert returns == bm.sum(a + b + c)

  def test_grad_func_return_aux1(self):
    def call(a, b, c):
      return bm.sum(a + b + c), (bm.sin(100), bm.exp(0.1))

    bm.random.seed(1)
    a = bm.ones(10)
    b = bm.random.randn(10)
    c = bm.random.uniform(size=10)
    f_grad = bm.grad(call, return_value=True, has_aux=True)
    grads, returns, aux = f_grad(a, b, c)
    assert (grads == 1.).all()
    assert returns == bm.sum(a + b + c)
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)


class TestObjectFuncGrad(unittest.TestCase):
  def test_grad_ob1(self):
    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()

        self.a = bm.TrainVar(bm.ones(10))
        self.b = bm.TrainVar(bm.random.randn(10))
        self.c = bm.TrainVar(bm.random.uniform(size=10))

      def __call__(self):
        return bm.sum(self.a + self.b + self.c)

    bm.random.seed(0)

    t = Test()
    f_grad = bm.grad(t, grad_vars=t.vars())
    grads = f_grad()
    for g in grads.values(): assert (g == 1.).all()

    t = Test()
    f_grad = bm.grad(t, grad_vars=[t.a, t.b], dyn_vars=t.vars())
    grads = f_grad()
    for g in grads: assert (g == 1.).all()

    t = Test()
    f_grad = bm.grad(t, grad_vars=t.a, dyn_vars=t.vars())
    grads = f_grad()
    assert (grads == 1.).all()

  def test_grad_ob_aux(self):
    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.a = bm.TrainVar(bm.ones(10))
        self.b = bm.TrainVar(bm.random.randn(10))
        self.c = bm.TrainVar(bm.random.uniform(size=10))

      def __call__(self):
        return bm.sum(self.a + self.b + self.c), (bm.sin(100), bm.exp(0.1))

    bm.random.seed(0)
    t = Test()
    f_grad = bm.grad(t, grad_vars=[t.a, t.b], dyn_vars=t.vars(), has_aux=True)
    grads, aux = f_grad()
    for g in grads: assert (g == 1.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)

    t = Test()
    f_grad = bm.grad(t, grad_vars=t.a, dyn_vars=t.vars(), has_aux=True)
    grads, aux = f_grad()
    assert (grads == 1.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)

  def test_grad_ob_return(self):
    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.a = bm.TrainVar(bm.ones(10))
        self.b = bm.TrainVar(bm.random.randn(10))
        self.c = bm.TrainVar(bm.random.uniform(size=10))

      def __call__(self):
        return bm.sum(self.a + self.b + self.c)

    bm.random.seed(0)
    t = Test()
    f_grad = bm.grad(t, grad_vars=[t.a, t.b], dyn_vars=t.vars(), return_value=True)
    grads, returns = f_grad()
    for g in grads: assert (g == 1.).all()
    assert returns == t()

    t = Test()
    f_grad = bm.grad(t, grad_vars=t.a, dyn_vars=t.vars(), return_value=True)
    grads, returns = f_grad()
    assert (grads == 1.).all()
    assert returns == t()

  def test_grad_ob_aux_return(self):
    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.a = bm.TrainVar(bm.ones(10))
        self.b = bm.TrainVar(bm.random.randn(10))
        self.c = bm.TrainVar(bm.random.uniform(size=10))

      def __call__(self):
        return bm.sum(self.a + self.b + self.c), (bm.sin(100), bm.exp(0.1))

    bm.random.seed(0)
    t = Test()
    f_grad = bm.grad(t, grad_vars=[t.a, t.b], dyn_vars=t.vars(),
                     has_aux=True, return_value=True)
    grads, returns, aux = f_grad()
    for g in grads: assert (g == 1.).all()
    assert returns == bm.sum(t.a + t.b + t.c)
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)

    t = Test()
    f_grad = bm.grad(t, grad_vars=t.a, dyn_vars=t.vars(),
                     has_aux=True, return_value=True)
    grads, returns, aux = f_grad()
    assert (grads == 1.).all()
    assert returns == bm.sum(t.a + t.b + t.c)
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)

  def test_grad_ob_argnums(self):
    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()

        self.a = bm.TrainVar(bm.ones(10))
        self.b = bm.TrainVar(bm.random.randn(10))
        self.c = bm.TrainVar(bm.random.uniform(size=10))

      def __call__(self, d):
        return bm.sum(self.a + self.b + self.c + 2 * d)

    bm.random.seed(0)

    t = Test()
    f_grad = bm.grad(t, t.vars(), argnums=0)
    var_grads, arg_grads = f_grad(bm.random.random(10))
    for g in var_grads.values(): assert (g == 1.).all()
    assert (arg_grads == 2.).all()

    t = Test()
    f_grad = bm.grad(t, t.vars(), argnums=[0])
    var_grads, arg_grads = f_grad(bm.random.random(10))
    for g in var_grads.values(): assert (g == 1.).all()
    assert (arg_grads[0] == 2.).all()

    t = Test()
    f_grad = bm.grad(t, dyn_vars=t.vars(), argnums=0)
    arg_grads = f_grad(bm.random.random(10))
    assert (arg_grads == 2.).all()

    t = Test()
    f_grad = bm.grad(t, dyn_vars=t.vars(), argnums=[0])
    arg_grads = f_grad(bm.random.random(10))
    assert (arg_grads[0] == 2.).all()

  def test_grad_ob_argnums_aux(self):
    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.a = bm.TrainVar(bm.ones(10))
        self.b = bm.TrainVar(bm.random.randn(10))
        self.c = bm.TrainVar(bm.random.uniform(size=10))

      def __call__(self, d):
        return bm.sum(self.a + self.b + self.c + 2 * d), (bm.sin(100), bm.exp(0.1))

    bm.random.seed(0)

    t = Test()
    f_grad = bm.grad(t, grad_vars=t.vars(), argnums=0, has_aux=True)
    (var_grads, arg_grads), aux = f_grad(bm.random.random(10))
    for g in var_grads.values(): assert (g == 1.).all()
    assert (arg_grads == 2.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)

    t = Test()
    f_grad = bm.grad(t, grad_vars=t.vars(), argnums=[0], has_aux=True)
    (var_grads, arg_grads), aux = f_grad(bm.random.random(10))
    for g in var_grads.values(): assert (g == 1.).all()
    assert (arg_grads[0] == 2.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)

    t = Test()
    f_grad = bm.grad(t, dyn_vars=t.vars(), argnums=0, has_aux=True)
    arg_grads, aux = f_grad(bm.random.random(10))
    assert (arg_grads == 2.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)

    t = Test()
    f_grad = bm.grad(t, dyn_vars=t.vars(), argnums=[0], has_aux=True)
    arg_grads, aux = f_grad(bm.random.random(10))
    assert (arg_grads[0] == 2.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)

  def test_grad_ob_argnums_return(self):
    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()

        self.a = bm.TrainVar(bm.ones(10))
        self.b = bm.TrainVar(bm.random.randn(10))
        self.c = bm.TrainVar(bm.random.uniform(size=10))

      def __call__(self, d):
        return bm.sum(self.a + self.b + self.c + 2 * d)

    bm.random.seed(0)

    t = Test()
    f_grad = bm.grad(t, t.vars(), argnums=0, return_value=True)
    d = bm.random.random(10)
    (var_grads, arg_grads), loss = f_grad(d)
    for g in var_grads.values(): assert (g == 1.).all()
    assert (arg_grads == 2.).all()
    assert loss == t(d)

    t = Test()
    f_grad = bm.grad(t, t.vars(), argnums=[0], return_value=True)
    d = bm.random.random(10)
    (var_grads, arg_grads), loss = f_grad(d)
    for g in var_grads.values(): assert (g == 1.).all()
    assert (arg_grads[0] == 2.).all()
    assert loss == t(d)

    t = Test()
    f_grad = bm.grad(t, dyn_vars=t.vars(), argnums=0, return_value=True)
    d = bm.random.random(10)
    arg_grads, loss = f_grad(d)
    assert (arg_grads == 2.).all()
    assert loss == t(d)

    t = Test()
    f_grad = bm.grad(t, dyn_vars=t.vars(), argnums=[0], return_value=True)
    d = bm.random.random(10)
    arg_grads, loss = f_grad(d)
    assert (arg_grads[0] == 2.).all()
    assert loss == t(d)

  def test_grad_ob_argnums_aux_return(self):
    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.a = bm.TrainVar(bm.ones(10))
        self.b = bm.TrainVar(bm.random.randn(10))
        self.c = bm.TrainVar(bm.random.uniform(size=10))

      def __call__(self, d):
        return bm.sum(self.a + self.b + self.c + 2 * d), (bm.sin(100), bm.exp(0.1))

    bm.random.seed(0)

    t = Test()
    f_grad = bm.grad(t, grad_vars=t.vars(), argnums=0, has_aux=True, return_value=True)
    d = bm.random.random(10)
    (var_grads, arg_grads), loss, aux = f_grad(d)
    for g in var_grads.values(): assert (g == 1.).all()
    assert (arg_grads == 2.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)
    assert loss == t(d)[0]

    t = Test()
    f_grad = bm.grad(t, grad_vars=t.vars(), argnums=[0], has_aux=True, return_value=True)
    d = bm.random.random(10)
    (var_grads, arg_grads), loss, aux = f_grad(d)
    for g in var_grads.values(): assert (g == 1.).all()
    assert (arg_grads[0] == 2.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)
    assert loss == t(d)[0]

    t = Test()
    f_grad = bm.grad(t, dyn_vars=t.vars(), argnums=0, has_aux=True, return_value=True)
    d = bm.random.random(10)
    arg_grads, loss, aux = f_grad(d)
    assert (arg_grads == 2.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)
    assert loss == t(d)[0]

    t = Test()
    f_grad = bm.grad(t, dyn_vars=t.vars(), argnums=[0], has_aux=True, return_value=True)
    d = bm.random.random(10)
    arg_grads, loss, aux = f_grad(d)
    assert (arg_grads[0] == 2.).all()
    assert aux[0] == bm.sin(100)
    assert aux[1] == bm.exp(0.1)
    assert loss == t(d)[0]


class TestPureFuncJacobian(unittest.TestCase):
  def test1(self):
    jac, aux = _jacfwd(lambda x: (x ** 3, [x ** 2]), has_aux=True)(3.)
    self.assertTrue(jax.numpy.allclose(jac, jax.jacfwd(lambda x: x ** 3)(3.)))
    self.assertTrue(aux[0] == 9.)

  def test_jacfwd_and_aux_nested(self):
    def f(x):
      jac, aux = _jacfwd(lambda x: (x ** 3, [x ** 3]), has_aux=True)(x)
      return aux[0]

    f2 = lambda x: x ** 3

    self.assertEqual(_jacfwd(f)(4.), _jacfwd(f2)(4.))
    self.assertEqual(bm.jit(_jacfwd(f))(4.), _jacfwd(f2)(4.))
    self.assertEqual(bm.jit(_jacfwd(bm.jit(f)))(4.), _jacfwd(f2)(4.))

    self.assertEqual(_jacfwd(f)(bm.asarray(4.)), _jacfwd(f2)(bm.asarray(4.)))
    self.assertEqual(bm.jit(_jacfwd(f))(bm.asarray(4.)), _jacfwd(f2)(bm.asarray(4.)))
    self.assertEqual(bm.jit(_jacfwd(bm.jit(f)))(bm.asarray(4.)), _jacfwd(f2)(bm.asarray(4.)))

    def f(x):
      jac, aux = _jacfwd(lambda x: (x ** 3, [x ** 3]), has_aux=True)(x)
      return aux[0] * bm.sin(x)

    f2 = lambda x: x ** 3 * bm.sin(x)

    self.assertEqual(_jacfwd(f)(4.), _jacfwd(f2)(4.))
    self.assertEqual(bm.jit(_jacfwd(f))(4.), _jacfwd(f2)(4.))
    self.assertEqual(bm.jit(_jacfwd(bm.jit(f)))(4.), _jacfwd(f2)(4.))

    self.assertEqual(_jacfwd(f)(bm.asarray(4.)), _jacfwd(f2)(bm.asarray(4.)))
    self.assertEqual(bm.jit(_jacfwd(f))(bm.asarray(4.)), _jacfwd(f2)(bm.asarray(4.)))
    self.assertEqual(bm.jit(_jacfwd(bm.jit(f)))(bm.asarray(4.)), _jacfwd(f2)(bm.asarray(4.)))

  def test_jacrev1(self):
    def f1(x, y):
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], 4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r

    br = bm.jacrev(f1)(bm.array([1., 2., 3.]), bm.array([10., 5.]))
    jr = jax.jacrev(f1)(bm.array([1., 2., 3.]), bm.array([10., 5.]))
    assert (br == jr).all()

    br = bm.jacrev(f1, argnums=(0, 1))(bm.array([1., 2., 3.]), bm.array([10., 5.]))
    jr = jax.jacrev(f1, argnums=(0, 1))(bm.array([1., 2., 3.]), bm.array([10., 5.]))
    assert (br[0] == jr[0]).all()
    assert (br[1] == jr[1]).all()

  def test_jacrev2(self):
    print()

    def f2(x, y):
      r1 = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1]])
      r2 = jnp.asarray([4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r1, r2

    jr = jax.jacrev(f2)(jnp.array([1., 2., 3.]), jnp.array([10., 5.]))
    pprint(jr)

    br = bm.jacrev(f2)(bm.array([1., 2., 3.]).value, bm.array([10., 5.]).value)
    pprint(br)
    assert bm.array_equal(br[0], jr[0])
    assert bm.array_equal(br[1], jr[1])

    br = bm.jacrev(f2)(bm.array([1., 2., 3.]), bm.array([10., 5.]))
    pprint(br)
    assert bm.array_equal(br[0], jr[0])
    assert bm.array_equal(br[1], jr[1])

    def f2(x, y):
      r1 = bm.asarray([x[0] * y[0], 5 * x[2] * y[1]])
      r2 = bm.asarray([4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r1, r2

    br = bm.jacrev(f2)(bm.array([1., 2., 3.]).value, bm.array([10., 5.]).value)
    pprint(br)
    assert bm.array_equal(br[0], jr[0])
    assert bm.array_equal(br[1], jr[1])

    br = bm.jacrev(f2)(bm.array([1., 2., 3.]), bm.array([10., 5.]))
    pprint(br)
    assert bm.array_equal(br[0], jr[0])
    assert bm.array_equal(br[1], jr[1])

  def test_jacrev3(self):
    print()

    def f3(x, y):
      r1 = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1]])
      r2 = jnp.asarray([4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r1, r2

    jr = jax.jacrev(f3, argnums=(0, 1))(jnp.array([1., 2., 3.]), jnp.array([10., 5.]))
    pprint(jr)

    br = bm.jacrev(f3, argnums=(0, 1))(bm.array([1., 2., 3.]).value, bm.array([10., 5.]).value)
    pprint(br)
    assert bm.array_equal(br[0][0], jr[0][0])
    assert bm.array_equal(br[0][1], jr[0][1])
    assert bm.array_equal(br[1][0], jr[1][0])
    assert bm.array_equal(br[1][1], jr[1][1])

    br = bm.jacrev(f3, argnums=(0, 1))(bm.array([1., 2., 3.]), bm.array([10., 5.]))
    pprint(br)
    assert bm.array_equal(br[0][0], jr[0][0])
    assert bm.array_equal(br[0][1], jr[0][1])
    assert bm.array_equal(br[1][0], jr[1][0])
    assert bm.array_equal(br[1][1], jr[1][1])

    def f3(x, y):
      r1 = bm.asarray([x[0] * y[0], 5 * x[2] * y[1]])
      r2 = bm.asarray([4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r1, r2

    br = bm.jacrev(f3, argnums=(0, 1))(bm.array([1., 2., 3.]).value, bm.array([10., 5.]).value)
    pprint(br)
    assert bm.array_equal(br[0][0], jr[0][0])
    assert bm.array_equal(br[0][1], jr[0][1])
    assert bm.array_equal(br[1][0], jr[1][0])
    assert bm.array_equal(br[1][1], jr[1][1])

    br = bm.jacrev(f3, argnums=(0, 1))(bm.array([1., 2., 3.]), bm.array([10., 5.]))
    pprint(br)
    assert bm.array_equal(br[0][0], jr[0][0])
    assert bm.array_equal(br[0][1], jr[0][1])
    assert bm.array_equal(br[1][0], jr[1][0])
    assert bm.array_equal(br[1][1], jr[1][1])

  def test_jacrev_aux1(self):
    x = bm.array([1., 2., 3.])
    y = bm.array([10., 5.])

    def f1(x, y):
      a = 4 * x[1] ** 2 - 2 * x[2]
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], a, x[2] * jnp.sin(x[0])])
      return r, a

    f2 = lambda *args: f1(*args)[0]
    jr = jax.jacrev(f2)(x, y)  # jax jacobian
    pprint(jr)
    grads, aux = bm.jacrev(f1, has_aux=True)(x, y)
    assert (grads == jr).all()
    assert aux == (4 * x[1] ** 2 - 2 * x[2])

    jr = jax.jacrev(f2, argnums=(0, 1))(x, y)  # jax jacobian
    pprint(jr)
    grads, aux = bm.jacrev(f1, argnums=(0, 1), has_aux=True)(x, y)
    assert (grads[0] == jr[0]).all()
    assert (grads[1] == jr[1]).all()
    assert aux == (4 * x[1] ** 2 - 2 * x[2])

  def test_jacrev_return_aux1(self):
    def f1(x, y):
      a = 4 * x[1] ** 2 - 2 * x[2]
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], a, x[2] * jnp.sin(x[0])])
      return r, a

    _x = bm.array([1., 2., 3.])
    _y = bm.array([10., 5.])
    _r, _a = f1(_x, _y)
    f2 = lambda *args: f1(*args)[0]
    _g1 = jax.jacrev(f2)(_x, _y)  # jax jacobian
    pprint(_g1)
    _g2 = jax.jacrev(f2, argnums=(0, 1))(_x, _y)  # jax jacobian
    pprint(_g2)

    grads, vec, aux = bm.jacrev(f1, return_value=True, has_aux=True)(_x, _y)
    assert (grads == _g1).all()
    assert aux == _a
    assert (vec == _r).all()

    grads, vec, aux = bm.jacrev(f1, return_value=True, argnums=(0, 1), has_aux=True)(_x, _y)
    assert (grads[0] == _g2[0]).all()
    assert (grads[1] == _g2[1]).all()
    assert aux == _a
    assert (vec == _r).all()


class TestClassFuncJacobian(unittest.TestCase):
  def test_jacrev1(self):
    def f1(x, y):
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], 4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r

    _x = bm.array([1., 2., 3.])
    _y = bm.array([10., 5.])

    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.x = bm.array([1., 2., 3.])
        self.y = bm.array([10., 5.])

      def __call__(self, ):
        a = self.x[0] * self.y[0]
        b = 5 * self.x[2] * self.y[1]
        c = 4 * self.x[1] ** 2 - 2 * self.x[2]
        d = self.x[2] * jnp.sin(self.x[0])
        r = jnp.asarray([a, b, c, d])
        return r

    _jr = jax.jacrev(f1)(_x, _y)
    t = Test()
    br = bm.jacrev(t, grad_vars=t.x)()
    self.assertTrue((br == _jr).all())

    _jr = jax.jacrev(f1, argnums=(0, 1))(_x, _y)
    t = Test()
    br = bm.jacrev(t, grad_vars=[t.x, t.y])()
    self.assertTrue((br[0] == _jr[0]).all())
    self.assertTrue((br[1] == _jr[1]).all())

  def test_jacfwd1(self):
    def f1(x, y):
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], 4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r

    _x = bm.array([1., 2., 3.])
    _y = bm.array([10., 5.])

    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.x = bm.array([1., 2., 3.])
        self.y = bm.array([10., 5.])

      def __call__(self, ):
        a = self.x[0] * self.y[0]
        b = 5 * self.x[2] * self.y[1]
        c = 4 * self.x[1] ** 2 - 2 * self.x[2]
        d = self.x[2] * jnp.sin(self.x[0])
        r = jnp.asarray([a, b, c, d])
        return r

    _jr = jax.jacfwd(f1)(_x, _y)
    t = Test()
    br = bm.jacfwd(t, grad_vars=t.x)()
    self.assertTrue((br == _jr).all())

    _jr = jax.jacfwd(f1, argnums=(0, 1))(_x, _y)
    t = Test()
    br = bm.jacfwd(t, grad_vars=[t.x, t.y])()
    self.assertTrue((br[0] == _jr[0]).all())
    self.assertTrue((br[1] == _jr[1]).all())

  def test_jacrev2(self):
    def f1(x, y):
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], 4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r

    _x = bm.array([1., 2., 3.])
    _y = bm.array([10., 5.])

    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.x = bm.array([1., 2., 3.])

      def __call__(self, y):
        a = self.x[0] * y[0]
        b = 5 * self.x[2] * y[1]
        c = 4 * self.x[1] ** 2 - 2 * self.x[2]
        d = self.x[2] * jnp.sin(self.x[0])
        r = jnp.asarray([a, b, c, d])
        return r

    _jr = jax.jacrev(f1)(_x, _y)
    t = Test()
    br = bm.jacrev(t, grad_vars=t.x)(_y)
    self.assertTrue((br == _jr).all())

    _jr = jax.jacrev(f1, argnums=(0, 1))(_x, _y)
    t = Test()
    var_grads, arg_grads = bm.jacrev(t, grad_vars=t.x, argnums=0)(_y)
    print(var_grads, )
    print(arg_grads, )
    self.assertTrue((var_grads == _jr[0]).all())
    self.assertTrue((arg_grads == _jr[1]).all())

  def test_jacfwd2(self):
    def f1(x, y):
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], 4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r

    _x = bm.array([1., 2., 3.])
    _y = bm.array([10., 5.])

    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.x = bm.array([1., 2., 3.])

      def __call__(self, y):
        a = self.x[0] * y[0]
        b = 5 * self.x[2] * y[1]
        c = 4 * self.x[1] ** 2 - 2 * self.x[2]
        d = self.x[2] * jnp.sin(self.x[0])
        r = jnp.asarray([a, b, c, d])
        return r

    _jr = jax.jacfwd(f1)(_x, _y)
    t = Test()
    br = bm.jacfwd(t, grad_vars=t.x)(_y)
    self.assertTrue((br == _jr).all())

    _jr = jax.jacfwd(f1, argnums=(0, 1))(_x, _y)
    t = Test()
    var_grads, arg_grads = bm.jacfwd(t, grad_vars=t.x, argnums=0)(_y)
    print(var_grads, )
    print(arg_grads, )
    self.assertTrue((var_grads == _jr[0]).all())
    self.assertTrue((arg_grads == _jr[1]).all())

  def test_jacrev_aux1(self):
    def f1(x, y):
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], 4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r

    _x = bm.array([1., 2., 3.])
    _y = bm.array([10., 5.])

    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.x = bm.array([1., 2., 3.])

      def __call__(self, y):
        a = self.x[0] * y[0]
        b = 5 * self.x[2] * y[1]
        c = 4 * self.x[1] ** 2 - 2 * self.x[2]
        d = self.x[2] * jnp.sin(self.x[0])
        r = jnp.asarray([a, b, c, d])
        return r, (c, d)

    _jr = jax.jacrev(f1)(_x, _y)
    t = Test()
    br, _ = bm.jacrev(t, grad_vars=t.x, has_aux=True)(_y)
    self.assertTrue((br == _jr).all())

    t = Test()
    _jr = jax.jacrev(f1, argnums=(0, 1))(_x, _y)
    _aux = t(_y)[1]
    (var_grads, arg_grads), aux = bm.jacrev(t, grad_vars=t.x, argnums=0, has_aux=True)(_y)
    print(var_grads, )
    print(arg_grads, )
    self.assertTrue((var_grads == _jr[0]).all())
    self.assertTrue((arg_grads == _jr[1]).all())
    self.assertTrue(bm.array_equal(aux, _aux))

  def test_jacfwd_aux1(self):
    def f1(x, y):
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], 4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r

    _x = bm.array([1., 2., 3.])
    _y = bm.array([10., 5.])

    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.x = bm.array([1., 2., 3.])

      def __call__(self, y):
        a = self.x[0] * y[0]
        b = 5 * self.x[2] * y[1]
        c = 4 * self.x[1] ** 2 - 2 * self.x[2]
        d = self.x[2] * jnp.sin(self.x[0])
        r = jnp.asarray([a, b, c, d])
        return r, (c, d)

    _jr = jax.jacfwd(f1)(_x, _y)
    t = Test()
    br, (c, d) = bm.jacfwd(t, grad_vars=t.x, has_aux=True)(_y)
    # print(_jr)
    # print(br)
    a = (br == _jr)
    self.assertTrue(a.all())

    t = Test()
    _jr = jax.jacfwd(f1, argnums=(0, 1))(_x, _y)
    _aux = t(_y)[1]
    (var_grads, arg_grads), aux = bm.jacfwd(t, grad_vars=t.x, argnums=0, has_aux=True)(_y)
    print(var_grads, )
    print(arg_grads, )
    self.assertTrue((var_grads == _jr[0]).all())
    self.assertTrue((arg_grads == _jr[1]).all())
    self.assertTrue(bm.array_equal(aux, _aux))

  def test_jacrev_return_aux1(self):
    def f1(x, y):
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], 4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r

    _x = bm.array([1., 2., 3.])
    _y = bm.array([10., 5.])

    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.x = bm.array([1., 2., 3.])

      def __call__(self, y):
        a = self.x[0] * y[0]
        b = 5 * self.x[2] * y[1]
        c = 4 * self.x[1] ** 2 - 2 * self.x[2]
        d = self.x[2] * jnp.sin(self.x[0])
        r = jnp.asarray([a, b, c, d])
        return r, (c, d)

    _jr = jax.jacrev(f1)(_x, _y)
    t = Test()
    br, _ = bm.jacrev(t, grad_vars=t.x, has_aux=True)(_y)
    self.assertTrue((br == _jr).all())

    t = Test()
    _jr = jax.jacrev(f1, argnums=(0, 1))(_x, _y)
    _val, _aux = t(_y)
    (var_grads, arg_grads), value, aux = bm.jacrev(t, grad_vars=t.x, argnums=0, has_aux=True, return_value=True)(_y)
    print(var_grads, )
    print(arg_grads, )
    self.assertTrue((var_grads == _jr[0]).all())
    self.assertTrue((arg_grads == _jr[1]).all())
    self.assertTrue(bm.array_equal(aux, _aux))
    self.assertTrue(bm.array_equal(value, _val))

  def test_jacfwd_return_aux1(self):
    def f1(x, y):
      r = jnp.asarray([x[0] * y[0], 5 * x[2] * y[1], 4 * x[1] ** 2 - 2 * x[2], x[2] * jnp.sin(x[0])])
      return r

    _x = bm.array([1., 2., 3.])
    _y = bm.array([10., 5.])

    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.x = bm.array([1., 2., 3.])

      def __call__(self, y):
        a = self.x[0] * y[0]
        b = 5 * self.x[2] * y[1]
        c = 4 * self.x[1] ** 2 - 2 * self.x[2]
        d = self.x[2] * jnp.sin(self.x[0])
        r = jnp.asarray([a, b, c, d])
        return r, (c, d)

    _jr = jax.jacfwd(f1)(_x, _y)
    t = Test()
    br, _ = bm.jacfwd(t, grad_vars=t.x, has_aux=True)(_y)
    self.assertTrue((br == _jr).all())

    t = Test()
    _jr = jax.jacfwd(f1, argnums=(0, 1))(_x, _y)
    _val, _aux = t(_y)
    (var_grads, arg_grads), value, aux = bm.jacfwd(t, grad_vars=t.x, argnums=0, has_aux=True, return_value=True)(_y)
    print(_val, )
    print(_aux, )
    print(var_grads, )
    print(arg_grads, )
    self.assertTrue((var_grads == _jr[0]).all())
    self.assertTrue((arg_grads == _jr[1]).all())
    self.assertTrue(bm.array_equal(aux, _aux))
    self.assertTrue(bm.array_equal(value, _val))


class TestPureFuncVectorGrad(unittest.TestCase):
  def test1(self):
    f = lambda x: 3 * x ** 2
    _x = bm.ones(10)
    pprint(bm.vector_grad(f, argnums=0)(_x))

  def test2(self):
    def f(x, y):
      dx = x ** 2 + y ** 2 + 10
      return dx

    _x = bm.ones(5)
    _y = bm.ones(5)

    g = bm.vector_grad(f, argnums=0)(_x, _y)
    pprint(g)
    self.assertTrue(bm.array_equal(g, 2 * _x))

    g = bm.vector_grad(f, argnums=(0,))(_x, _y)
    self.assertTrue(bm.array_equal(g[0], 2 * _x))

    g = bm.vector_grad(f, argnums=(0, 1))(_x, _y)
    pprint(g)
    self.assertTrue(bm.array_equal(g[0], 2 * _x))
    self.assertTrue(bm.array_equal(g[1], 2 * _y))

  def test3(self):
    def f(x, y):
      dx = x ** 2 + y ** 2 + 10
      dy = x ** 3 + y ** 3 - 10
      return dx, dy

    _x = bm.ones(5)
    _y = bm.ones(5)

    g = bm.vector_grad(f, argnums=0)(_x, _y)
    # pprint(g)
    self.assertTrue(bm.array_equal(g, 2 * _x + 3 * _x ** 2))

    g = bm.vector_grad(f, argnums=(0,))(_x, _y)
    self.assertTrue(bm.array_equal(g[0], 2 * _x + 3 * _x ** 2))

    g = bm.vector_grad(f, argnums=(0, 1))(_x, _y)
    # pprint(g)
    self.assertTrue(bm.array_equal(g[0], 2 * _x + 3 * _x ** 2))
    self.assertTrue(bm.array_equal(g[1], 2 * _y + 3 * _y ** 2))

  def test_aux1(self):
    def f(x, y):
      dx = x ** 2 + y ** 2 + 10
      dy = x ** 3 + y ** 3 - 10
      return dx, dy

    _x = bm.ones(5)
    _y = bm.ones(5)

    g, aux = bm.vector_grad(f, has_aux=True)(_x, _y)
    pprint(g, )
    pprint(aux)
    self.assertTrue(bm.array_equal(g, 2 * _x))
    self.assertTrue(bm.array_equal(aux, _x ** 3 + _y ** 3 - 10))

  def test_return1(self):
    def f(x, y):
      dx = x ** 2 + y ** 2 + 10
      return dx

    _x = bm.ones(5)
    _y = bm.ones(5)

    g, value = bm.vector_grad(f, return_value=True)(_x, _y)
    pprint(g, )
    pprint(value)
    self.assertTrue(bm.array_equal(g, 2 * _x))
    self.assertTrue(bm.array_equal(value, _x ** 2 + _y ** 2 + 10))

  def test_return_aux1(self):
    def f(x, y):
      dx = x ** 2 + y ** 2 + 10
      dy = x ** 3 + y ** 3 - 10
      return dx, dy

    _x = bm.ones(5)
    _y = bm.ones(5)

    g, value, aux = bm.vector_grad(f, has_aux=True, return_value=True)(_x, _y)
    print('grad', g)
    print('value', value)
    print('aux', aux)
    self.assertTrue(bm.array_equal(g, 2 * _x))
    self.assertTrue(bm.array_equal(value, _x ** 2 + _y ** 2 + 10))
    self.assertTrue(bm.array_equal(aux, _x ** 3 + _y ** 3 - 10))


class TestClassFuncVectorGrad(unittest.TestCase):
  def test1(self):
    class Test(bp.Base):
      def __init__(self):
        super(Test, self).__init__()
        self.x = bm.ones(5)
        self.y = bm.ones(5)

      def __call__(self, *args, **kwargs):
        return self.x ** 2 + self.y ** 2 + 10

    t = Test()

    g = bm.vector_grad(t, grad_vars=t.x)()
    self.assertTrue(bm.array_equal(g, 2 * t.x))

    g = bm.vector_grad(t, grad_vars=(t.x,))()
    self.assertTrue(bm.array_equal(g[0], 2 * t.x))

    g = bm.vector_grad(t, grad_vars=(t.x, t.y))()
    self.assertTrue(bm.array_equal(g[0], 2 * t.x))
    self.assertTrue(bm.array_equal(g[1], 2 * t.y))
