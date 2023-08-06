# -*- coding: utf-8 -*-


from pprint import pprint

import brainpy as bp


class GABAa_without_Variable(bp.dyn.TwoEndConn):
  def __init__(self, pre, post, conn, delay=0., g_max=0.1, E=-75.,
               alpha=12., beta=0.1, T=1.0, T_duration=1.0, **kwargs):
    super(GABAa_without_Variable, self).__init__(pre=pre, post=post, **kwargs)

    # parameters
    self.g_max = g_max
    self.E = E
    self.alpha = alpha
    self.beta = beta
    self.T = T
    self.T_duration = T_duration
    self.delay = delay

    # connections
    self.conn = conn(pre.size, post.size)
    self.conn_mat = self.conn.requires(bp.connect.CONN_MAT)
    self.size = bp.math.shape(self.conn_mat)

    # variables
    self.t_last_pre_spike = bp.math.ones(self.size) * -1e7
    self.s = bp.math.zeros(self.size)
    self.g = bp.dyn.ConstantDelay(size=self.size, delay=delay)

  @bp.odeint
  def int_s(self, s, t, TT):
    return self.alpha * TT * (1 - s) - self.beta * s

  def update(self, _t, _i):
    spike = bp.math.reshape(self.pre.spikes, (self.pre.num, 1)) * self.conn_mat
    self.t_last_pre_spike[:] = bp.math.where(spike, _t, self.t_last_pre_spike)
    TT = ((_t - self.t_last_pre_spike) < self.T_duration) * self.T
    self.s[:] = self.int_s(self.s, _t, TT)
    self.g.push(self.g_max * self.s)
    g = self.g.pull()
    self.post.inputs -= bp.math.sum(g, axis=0) * (self.post.V - self.E)


class HH_without_Variable(bp.dyn.NeuGroup):
  def __init__(self, size, ENa=55., EK=-90., EL=-65, C=1.0,
               gNa=35., gK=9., gL=0.1, V_th=20., phi=5.0, **kwargs):
    super(HH_without_Variable, self).__init__(size=size, **kwargs)

    # parameters
    self.ENa = ENa
    self.EK = EK
    self.EL = EL
    self.C = C
    self.gNa = gNa
    self.gK = gK
    self.gL = gL
    self.V_th = V_th
    self.phi = phi

    # variables
    self.V = bp.math.ones(self.num) * -65.
    self.h = bp.math.ones(self.num) * 0.6
    self.n = bp.math.ones(self.num) * 0.32
    self.inputs = bp.math.zeros(self.num)
    self.spikes = bp.math.zeros(self.num, dtype=bp.math.bool_)

  @bp.odeint
  def integral(self, V, h, n, t, Iext):
    alpha = 0.07 * bp.math.exp(-(V + 58) / 20)
    beta = 1 / (bp.math.exp(-0.1 * (V + 28)) + 1)
    dhdt = self.phi * (alpha * (1 - h) - beta * h)

    alpha = -0.01 * (V + 34) / (bp.math.exp(-0.1 * (V + 34)) - 1)
    beta = 0.125 * bp.math.exp(-(V + 44) / 80)
    dndt = self.phi * (alpha * (1 - n) - beta * n)

    m_alpha = -0.1 * (V + 35) / (bp.math.exp(-0.1 * (V + 35)) - 1)
    m_beta = 4 * bp.math.exp(-(V + 60) / 18)
    m = m_alpha / (m_alpha + m_beta)
    INa = self.gNa * m ** 3 * h * (V - self.ENa)
    IK = self.gK * n ** 4 * (V - self.EK)
    IL = self.gL * (V - self.EL)
    dVdt = (- INa - IK - IL + Iext) / self.C

    return dVdt, dhdt, dndt

  def update(self, _t, _i):
    V, h, n = self.integral(self.V, self.h, self.n, _t, self.inputs)
    self.spikes[:] = bp.math.logical_and(self.V < self.V_th, V >= self.V_th)
    self.V[:] = V
    self.h[:] = h
    self.n[:] = n
    self.inputs[:] = 0.


def test_subset_integrator():
  neu = HH_without_Variable(10)
  syn = GABAa_without_Variable(pre=neu, post=neu, conn=bp.connect.All2All(include_self=False))
  syn.g_max = 0.1 / neu.num
  net = bp.dyn.Network(neu, syn)

  ints = net.ints()
  print()
  print(ints)

  ode_ints = ints.subset(bp.integrators.ODEIntegrator)
  print(ode_ints)
  assert len(ode_ints) == 2


def test_neu_vars_1():
  neu = HH_without_Variable(10)
  vars = neu.vars()

  print()
  print(vars)
  assert len(vars) == 0


class HH_with_Variable(bp.dyn.NeuGroup):
  def __init__(self, size, ENa=55., EK=-90., EL=-65, C=1.0,
               gNa=35., gK=9., gL=0.1, V_th=20., phi=5.0, **kwargs):
    super(HH_with_Variable, self).__init__(size=size, **kwargs)

    # parameters
    self.ENa = ENa
    self.EK = EK
    self.EL = EL
    self.C = C
    self.gNa = gNa
    self.gK = gK
    self.gL = gL
    self.V_th = V_th
    self.phi = phi

    # variables
    self.V = bp.math.Variable(bp.math.ones(self.num) * -65.)
    self.h = bp.math.Variable(bp.math.ones(self.num) * 0.6)
    self.n = bp.math.Variable(bp.math.ones(self.num) * 0.32)
    self.inputs = bp.math.Variable(bp.math.zeros(self.num))
    self.spikes = bp.math.Variable(bp.math.zeros(self.num, dtype=bp.math.bool_))

  @bp.odeint
  def integral(self, V, h, n, t, Iext):
    alpha = 0.07 * bp.math.exp(-(V + 58) / 20)
    beta = 1 / (bp.math.exp(-0.1 * (V + 28)) + 1)
    dhdt = self.phi * (alpha * (1 - h) - beta * h)

    alpha = -0.01 * (V + 34) / (bp.math.exp(-0.1 * (V + 34)) - 1)
    beta = 0.125 * bp.math.exp(-(V + 44) / 80)
    dndt = self.phi * (alpha * (1 - n) - beta * n)

    m_alpha = -0.1 * (V + 35) / (bp.math.exp(-0.1 * (V + 35)) - 1)
    m_beta = 4 * bp.math.exp(-(V + 60) / 18)
    m = m_alpha / (m_alpha + m_beta)
    INa = self.gNa * m ** 3 * h * (V - self.ENa)
    IK = self.gK * n ** 4 * (V - self.EK)
    IL = self.gL * (V - self.EL)
    dVdt = (- INa - IK - IL + Iext) / self.C

    return dVdt, dhdt, dndt

  def update(self, _t, _i):
    V, h, n = self.integral(self.V, self.h, self.n, _t, self.inputs)
    self.spikes[:] = bp.math.logical_and(self.V < self.V_th, V >= self.V_th)
    self.V[:] = V
    self.h[:] = h
    self.n[:] = n
    self.inputs[:] = 0.


def test_neu_vars_2():
  neu = HH_with_Variable(10)
  vars = neu.vars()
  print()
  print(vars.keys())

  vars = neu.vars(method='relative')
  print()
  print(vars.keys())


def test_neu_nodes_1():
  neu = HH_with_Variable(10)
  print()
  print(neu.nodes().keys())
  assert len(neu.nodes()) == 1

  print()
  print(neu.nodes(method='relative').keys())
  assert len(neu.nodes(method='relative')) == 1


def test_neu_ints_1():
  neu = HH_with_Variable(10)
  print()
  print(neu.ints().keys())
  assert len(neu.ints()) == 1

  print()
  print(neu.ints(method='relative').keys())
  assert len(neu.ints(method='relative')) == 1


class GABAa_with_Variable(bp.dyn.TwoEndConn):
  def __init__(self, pre, post, conn, delay=0., g_max=0.1, E=-75.,
               alpha=12., beta=0.1, T=1.0, T_duration=1.0, **kwargs):
    super(GABAa_with_Variable, self).__init__(pre=pre, post=post, **kwargs)

    # parameters
    self.g_max = g_max
    self.E = E
    self.alpha = alpha
    self.beta = beta
    self.T = T
    self.T_duration = T_duration
    self.delay = delay

    # connections
    self.conn = conn(pre.size, post.size)
    self.conn_mat = self.conn.requires(bp.connect.CONN_MAT)
    self.size = bp.math.shape(self.conn_mat)

    # variables
    self.t_last_pre_spike = bp.math.Variable(bp.math.ones(self.size) * -1e7)
    self.s = bp.math.Variable(bp.math.zeros(self.size))
    self.g = bp.dyn.ConstantDelay(size=self.size, delay=delay)

  @bp.odeint
  def int_s(self, s, t, TT):
    return self.alpha * TT * (1 - s) - self.beta * s

  def update(self, _t, _i):
    spike = bp.math.reshape(self.pre.spikes, (self.pre.num, 1)) * self.conn_mat
    self.t_last_pre_spike[:] = bp.math.where(spike, _t, self.t_last_pre_spike)
    TT = ((_t - self.t_last_pre_spike) < self.T_duration) * self.T
    self.s[:] = self.int_s(self.s, _t, TT)
    self.g.push(self.g_max * self.s)
    g = self.g.pull()
    self.post.inputs -= bp.math.sum(g, axis=0) * (self.post.V - self.E)


def test_net_1():
  neu = HH_without_Variable(10)
  syn = GABAa_without_Variable(pre=neu, post=neu, conn=bp.connect.All2All(include_self=False))
  net = bp.dyn.Network(neu=neu, syn=syn)

  # variables
  print()
  pprint(list(net.vars().keys()))
  assert len(net.vars()) == 3

  print()
  pprint(list(net.vars(method='relative').keys()))
  assert len(net.vars(method='relative')) == 3

  # nodes
  print()
  pprint(list(net.nodes().keys()))
  assert len(net.nodes()) == 4

  print()
  pprint(list(net.nodes(method='relative').keys()))
  assert len(net.nodes(method='relative')) == 5

  # ints
  print()
  pprint(list(net.ints().keys()))
  assert len(net.ints()) == 2

  print()
  pprint(list(net.ints(method='relative').keys()))
  assert len(net.ints(method='relative')) == 3


def test_net_vars_2():
  neu = HH_with_Variable(10)
  syn = GABAa_with_Variable(pre=neu, post=neu, conn=bp.connect.All2All(include_self=False))
  net = bp.dyn.Network(neu=neu, syn=syn)

  # variables
  print()
  pprint(list(net.vars().keys()))
  # assert len(net.vars()) == 3

  print()
  pprint(list(net.vars(method='relative').keys()))
  # assert len(net.vars(method='relative')) == 3

  # nodes
  print()
  pprint(list(net.nodes().keys()))
  assert len(net.nodes()) == 4

  print()
  pprint(list(net.nodes(method='relative').keys()))
  assert len(net.nodes(method='relative')) == 5

  # ints
  print()
  pprint(list(net.ints().keys()))
  assert len(net.ints()) == 2

  print()
  pprint(list(net.ints(method='relative').keys()))
  assert len(net.ints(method='relative')) == 3
