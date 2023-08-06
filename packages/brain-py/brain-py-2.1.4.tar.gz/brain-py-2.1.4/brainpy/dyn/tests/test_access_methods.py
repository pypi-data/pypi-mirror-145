# -*- coding: utf-8 -*-


import brainpy as bp

bp.integrators.set_default_odeint('rk4')


class GABAa(bp.dyn.TwoEndConn):
  def __init__(self, pre, post, conn, delay=0., g_max=0.1, E=-75.,
               alpha=12., beta=0.1, T=1.0, T_duration=1.0, **kwargs):
    super(GABAa, self).__init__(pre=pre, post=post, conn=conn, **kwargs)

    # parameters
    self.g_max = g_max
    self.E = E
    self.alpha = alpha
    self.beta = beta
    self.T = T
    self.T_duration = T_duration
    self.delay = delay

    # connections
    self.conn_mat = self.conn.requires('conn_mat')
    self.size = bp.math.shape(self.conn_mat)

    # variables
    self.t_last_pre_spike = bp.math.ones(self.size) * -1e7
    self.s = bp.math.zeros(self.size)
    self.g = bp.dyn.ConstantDelay(size=self.size, delay=delay)

  @staticmethod
  @bp.odeint
  def int_s(s, t, TT, alpha, beta):
    return alpha * TT * (1 - s) - beta * s

  def update(self, _t, _i, **kwargs):
    spike = bp.math.reshape(self.pre.spikes, (self.pre.num, 1)) * self.conn_mat
    self.t_last_pre_spike = bp.math.where(spike, _t, self.t_last_pre_spike)
    TT = ((_t - self.t_last_pre_spike) < self.T_duration) * self.T
    self.s = self.int_s(self.s, _t, TT, self.alpha, self.beta)
    self.g.push(self.g_max * self.s)
    g = self.g.pull()
    self.post.inputs -= bp.math.sum(g, axis=0) * (self.post.V - self.E)


class HH(bp.dyn.NeuGroup):
  def __init__(self, size, ENa=55., EK=-90., EL=-65,
               C=1.0, gNa=35., gK=9., gL=0.1, V_th=20.,
               phi=5.0, **kwargs):
    super(HH, self).__init__(size=size, **kwargs)

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
    self.spikes = bp.math.zeros(self.num)
    self.inputs = bp.math.zeros(self.num)

  @bp.odeint
  def integral(self, V, h, n, t, Iext):
    alpha = 0.07 * bp.math.exp(-(V + 58) / 20)
    beta = 1 / (bp.math.exp(-0.1 * (V + 28)) + 1)
    dhdt = alpha * (1 - h) - beta * h

    alpha = -0.01 * (V + 34) / (bp.math.exp(-0.1 * (V + 34)) - 1)
    beta = 0.125 * bp.math.exp(-(V + 44) / 80)
    dndt = alpha * (1 - n) - beta * n

    m_alpha = -0.1 * (V + 35) / (bp.math.exp(-0.1 * (V + 35)) - 1)
    m_beta = 4 * bp.math.exp(-(V + 60) / 18)
    m = m_alpha / (m_alpha + m_beta)
    INa = self.gNa * m ** 3 * h * (V - self.ENa)
    IK = self.gK * n ** 4 * (V - self.EK)
    IL = self.gL * (V - self.EL)
    dVdt = (- INa - IK - IL + Iext) / self.C

    return dVdt, self.phi * dhdt, self.phi * dndt

  def update(self, _t, _i, **kwargs):
    V, h, n = self.integral(self.V, self.h, self.n, _t, self.inputs)
    self.spikes[:] = (self.V < self.V_th) * (V >= self.V_th)
    self.V[:] = V
    self.h[:] = h
    self.n[:] = n
    self.inputs[:] = 0


def test1():
    num = 10
    neu = HH(num)
    neu.V = -70. + bp.math.random.normal(size=num) * 20

    syn = GABAa(pre=neu, post=neu, conn=bp.connect.All2All(include_self=False))
    syn.g_max = 0.1 / num

    net = bp.dyn.Network(neu=neu, syn=syn)

    for method in ['relative', 'absolute']:
      print(f'Method: {method}\n')
      print('vars:')
      print('-----')
      print('neu.vars()', list(neu.vars(method).keys()))
      print('syn.vars()', list(syn.vars(method).keys()))
      print('net.vars()', list(net.vars(method).keys()))
      print()

      print('ints:')
      print('-----')
      print('neu.ints()', list(neu.ints(method).keys()))
      print('syn.ints()', list(syn.ints(method).keys()))
      print('net.ints()', list(net.ints(method).keys()))
      print()

      print('nodes:')
      print('------')
      print('neu.nodes()', list(neu.nodes(method).keys()))
      print('syn.nodes()', list(syn.nodes(method).keys()))
      print('net.nodes()', list(net.nodes(method).keys()))
      print()
