# -*- coding: utf-8 -*-

from typing import Union, Dict

import brainpy.math as bm
from brainpy.connect import TwoEndConnector, All2All, One2One
from brainpy.dyn.base import NeuGroup, TwoEndConn
from brainpy.dyn.utils import init_delay
from brainpy.integrators import odeint
from brainpy.types import Tensor, Parameter

__all__ = [
  'DeltaSynapse',
  'ExpCUBA',
  'ExpCOBA',
  'DualExpCUBA',
  'DualExpCOBA',
  'AlphaCUBA',
  'AlphaCOBA',
]


class DeltaSynapse(TwoEndConn):
  """Voltage Jump Synapse Model, or alias of Delta Synapse Model.

  **Model Descriptions**

  .. math::

      I_{syn} (t) = \sum_{j\in C} w \delta(t-t_j-D)

  where :math:`w` denotes the chemical synaptic strength, :math:`t_j` the spiking
  moment of the presynaptic neuron :math:`j`, :math:`C` the set of neurons connected
  to the post-synaptic neuron, and :math:`D` the transmission delay of chemical
  synapses. For simplicity, the rise and decay phases of post-synaptic currents are
  omitted in this model.

  **Model Examples**

  .. plot::
    :include-source: True

    >>> import brainpy as bp
    >>> import matplotlib.pyplot as plt
    >>>
    >>> neu1 = bp.dyn.LIF(1)
    >>> neu2 = bp.dyn.LIF(1)
    >>> syn1 = bp.dyn.DeltaSynapse(neu1, neu2, bp.connect.All2All(), w=5.)
    >>> net = bp.dyn.Network(pre=neu1, syn=syn1, post=neu2)
    >>>
    >>> runner = bp.dyn.DSRunner(net, inputs=[('pre.input', 25.), ('post.input', 10.)], monitors=['pre.V', 'post.V', 'pre.spike'])
    >>> runner.run(150.)
    >>>
    >>> fig, gs = bp.visualize.get_figure(1, 1, 3, 8)
    >>> plt.plot(runner.mon.ts, runner.mon['pre.V'], label='pre-V')
    >>> plt.plot(runner.mon.ts, runner.mon['post.V'], label='post-V')
    >>> plt.xlim(40, 150)
    >>> plt.legend()
    >>> plt.show()

  **Model Parameters**

  ============= ============== ======== ===========================================
  **Parameter** **Init Value** **Unit** **Explanation**
  ------------- -------------- -------- -------------------------------------------
  w             1              mV       The synaptic strength.
  ============= ============== ======== ===========================================

  Parameters
  ----------
  pre: NeuGroup
    The pre-synaptic neuron group.
  post: NeuGroup
    The post-synaptic neuron group.
  conn: optional, ndarray, JaxArray, dict of (str, ndarray), TwoEndConnector
    The synaptic connections.
  delay_step: int, ndarray, JaxArray
    The delay length. It should be the value of :math:`\mathrm{delay\_time / dt}`.
  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, Tensor, Dict[str, Tensor]],
      w: Parameter = 1.,
      delay_step: Parameter = None,
      post_key='V',
      post_has_ref=False,
      name: str = None,
  ):
    super(DeltaSynapse, self).__init__(pre=pre, post=post, conn=conn, name=name)
    self.check_pre_attrs('spike')
    self.check_post_attrs(post_key)

    # parameters
    self.post_key = post_key
    self.post_has_ref = post_has_ref
    if post_has_ref:  # checking
      self.check_post_attrs('refractory')
    self.w = w

    # connections
    assert self.conn is not None
    if not isinstance(self.conn, (All2All, One2One)):
      self.pre2post = self.conn.require('pre2post')

    # variables
    delay_type, delay_step, delay_value = init_delay(delay_step, self.pre.spike)
    self.delay_type = delay_type
    self.delay_step = delay_step
    self.pre_spike = delay_value

  def update(self, _t, _dt):
    # delays
    if self.delay_type == 'homo':
      pre_spike = self.pre_spike(self.delay_step)
      self.pre_spike.update(self.pre.spike)
    elif self.delay_type == 'heter':
      pre_spike = self.pre_spike(self.delay_step, bm.arange(self.pre.num))
      self.pre_spike.update(self.pre.spike)
    else:
      pre_spike = self.pre.spike

    # post values
    if isinstance(self.conn, All2All):
      post_vs = bm.sum(pre_spike)
      if not self.conn.include_self:
        post_vs = post_vs - pre_spike
      post_vs *= self.w
    elif isinstance(self.conn, One2One):
      post_vs = pre_spike * self.w
    else:
      post_vs = bm.pre2post_event_sum(pre_spike, self.pre2post, self.post.num, self.w)

    # updates
    target = getattr(self.post, self.post_key)
    if self.post_has_ref:
      target += post_vs * (1. - self.post.refractory)
    else:
      target += post_vs


class ExpCUBA(TwoEndConn):
  r"""Current-based exponential decay synapse model.

  **Model Descriptions**

  The single exponential decay synapse model assumes the release of neurotransmitter,
  its diffusion across the cleft, the receptor binding, and channel opening all happen
  very quickly, so that the channels instantaneously jump from the closed to the open state.
  Therefore, its expression is given by

  .. math::

      g_{\mathrm{syn}}(t)=g_{\mathrm{max}} e^{-\left(t-t_{0}\right) / \tau}

  where :math:`\tau_{delay}` is the time constant of the synaptic state decay,
  :math:`t_0` is the time of the pre-synaptic spike,
  :math:`g_{\mathrm{max}}` is the maximal conductance.

  Accordingly, the differential form of the exponential synapse is given by

  .. math::

      \begin{aligned}
       & g_{\mathrm{syn}}(t) = g_{max} g \\
       & \frac{d g}{d t} = -\frac{g}{\tau_{decay}}+\sum_{k} \delta(t-t_{j}^{k}).
       \end{aligned}

  For the current output onto the post-synaptic neuron, its expression is given by

  .. math::

      I_{\mathrm{syn}}(t) = g_{\mathrm{syn}}(t)


  **Model Examples**

  - `(Brunel & Hakim, 1999) Fast Global Oscillation <https://brainpy-examples.readthedocs.io/en/latest/oscillation_synchronization/Brunel_Hakim_1999_fast_oscillation.html>`_
  - `(Vreeswijk & Sompolinsky, 1996) E/I balanced network <https://brainpy-examples.readthedocs.io/en/latest/ei_nets/Vreeswijk_1996_EI_net.html>`_
  - `(Brette, et, al., 2007) CUBA <https://brainpy-examples.readthedocs.io/en/latest/ei_nets/Brette_2007_CUBA.html>`_
  - `(Tian, et al., 2020) E/I Net for fast response <https://brainpy-examples.readthedocs.io/en/latest/ei_nets/Tian_2020_EI_net_for_fast_response.html>`_

  .. plot::
    :include-source: True

    >>> import brainpy as bp
    >>> import matplotlib.pyplot as plt
    >>>
    >>> neu1 = bp.dyn.LIF(1)
    >>> neu2 = bp.dyn.LIF(1)
    >>> syn1 = bp.dyn.ExpCUBA(neu1, neu2, bp.conn.All2All(), g_max=5.)
    >>> net = bp.dyn.Network(pre=neu1, syn=syn1, post=neu2)
    >>>
    >>> runner = bp.dyn.DSRunner(net, inputs=[('pre.input', 25.)], monitors=['pre.V', 'post.V', 'syn.g'])
    >>> runner.run(150.)
    >>>
    >>> fig, gs = bp.visualize.get_figure(2, 1, 3, 8)
    >>> fig.add_subplot(gs[0, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['pre.V'], label='pre-V')
    >>> plt.plot(runner.mon.ts, runner.mon['post.V'], label='post-V')
    >>> plt.legend()
    >>>
    >>> fig.add_subplot(gs[1, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['syn.g'], label='g')
    >>> plt.legend()
    >>> plt.show()


  **Model Parameters**

  ============= ============== ======== ===================================================================================
  **Parameter** **Init Value** **Unit** **Explanation**
  ------------- -------------- -------- -----------------------------------------------------------------------------------
  delay         0              ms       The decay length of the pre-synaptic spikes.
  tau_decay     8              ms       The time constant of decay.
  g_max         1              µmho(µS) The maximum conductance.
  ============= ============== ======== ===================================================================================

  **Model Variables**

  ================ ================== =========================================================
  **Member name**  **Initial values** **Explanation**
  ---------------- ------------------ ---------------------------------------------------------
  g                 0                 Gating variable.
  pre_spike         False             The history spiking states of the pre-synaptic neurons.
  ================ ================== =========================================================

  **References**

  .. [1] Sterratt, David, Bruce Graham, Andrew Gillies, and David Willshaw.
          "The Synapse." Principles of Computational Modelling in Neuroscience.
          Cambridge: Cambridge UP, 2011. 172-95. Print.
  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, Tensor, Dict[str, Tensor]],
      g_max: Parameter = 1.,
      tau: Parameter = 8.0,
      method: str = 'exp_auto',
      delay_step=None,
      name: str = None
  ):
    super(ExpCUBA, self).__init__(pre=pre, post=post, conn=conn, name=name)
    self.check_pre_attrs('spike')
    self.check_post_attrs('input', 'V')

    # parameters
    self.tau = tau
    self.g_max = g_max

    # connection
    assert self.conn is not None
    if not isinstance(self.conn, (All2All, One2One)):
      self.pre2post = self.conn.require('pre2post')

    # variables
    self.g = bm.Variable(bm.zeros(self.post.num))
    delay_type, delay_step, delay_value = init_delay(delay_step, self.pre.spike)
    self.delay_type = delay_type
    self.delay_step = delay_step
    self.pre_spike = delay_value

    # function
    self.integral = odeint(lambda g, t: -g / self.tau, method=method)

  def update(self, _t, _dt):
    if self.delay_type == 'homo':
      delayed_pre_spike = self.pre_spike(self.delay_step)
      self.pre_spike.update(self.pre.spike)
    elif self.delay_type == 'heter':
      delayed_pre_spike = self.pre_spike(self.delay_step, bm.arange(self.pre.num))
      self.pre_spike.update(self.pre.spike)
    else:
      delayed_pre_spike = self.pre.spike

    # post values
    if isinstance(self.conn, All2All):
      post_vs = bm.sum(delayed_pre_spike)
      if not self.conn.include_self:
        post_vs = post_vs - delayed_pre_spike
      post_vs *= self.g_max
    elif isinstance(self.conn, One2One):
      post_vs = delayed_pre_spike * self.g_max
    else:
      post_vs = bm.pre2post_event_sum(delayed_pre_spike, self.pre2post, self.post.num, self.g_max)

    # updates
    self.g.value = self.integral(self.g.value, _t, dt=_dt) + post_vs
    self.post.input += self.g


class ExpCOBA(ExpCUBA):
  """Conductance-based exponential decay synapse model.

  **Model Descriptions**

  The conductance-based exponential decay synapse model is similar with the
  `current-based exponential decay synapse model <./brainmodels.synapses.ExpCUBA.rst>`_,
  except the expression which output onto the post-synaptic neurons:

  .. math::

      I_{syn}(t) = g_{\mathrm{syn}}(t) (V(t)-E)

  where :math:`V(t)` is the membrane potential of the post-synaptic neuron,
  :math:`E` is the reversal potential.

  **Model Examples**

  - `(Brette, et, al., 2007) COBA <https://brainpy-examples.readthedocs.io/en/latest/ei_nets/Brette_2007_COBA.html>`_
  - `(Brette, et, al., 2007) COBAHH <https://brainpy-examples.readthedocs.io/en/latest/ei_nets/Brette_2007_COBAHH.html>`_


  .. plot::
    :include-source: True

    >>> import brainpy as bp
    >>> import matplotlib.pyplot as plt
    >>>
    >>> neu1 = bp.dyn.HH(1)
    >>> neu2 = bp.dyn.HH(1)
    >>> syn1 = bp.dyn.ExpCOBA(neu1, neu2, bp.connect.All2All(), E=0.)
    >>> net = bp.dyn.Network(pre=neu1, syn=syn1, post=neu2)
    >>>
    >>> runner = bp.dyn.DSRunner(net, inputs=[('pre.input', 5.)], monitors=['pre.V', 'post.V', 'syn.g'])
    >>> runner.run(150.)
    >>>
    >>> fig, gs = bp.visualize.get_figure(2, 1, 3, 8)
    >>> fig.add_subplot(gs[0, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['pre.V'], label='pre-V')
    >>> plt.plot(runner.mon.ts, runner.mon['post.V'], label='post-V')
    >>> plt.legend()
    >>>
    >>> fig.add_subplot(gs[1, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['syn.g'], label='g')
    >>> plt.legend()
    >>> plt.show()

  **Model Parameters**

  ============= ============== ======== ===================================================================================
  **Parameter** **Init Value** **Unit** **Explanation**
  ------------- -------------- -------- -----------------------------------------------------------------------------------
  delay         0              ms       The decay length of the pre-synaptic spikes.
  tau_decay     8              ms       The time constant of decay.
  g_max         1              µmho(µS) The maximum conductance.
  E             0              mV       The reversal potential for the synaptic current.
  ============= ============== ======== ===================================================================================

  **Model Variables**

  ================ ================== =========================================================
  **Member name**  **Initial values** **Explanation**
  ---------------- ------------------ ---------------------------------------------------------
  g                 0                 Gating variable.
  pre_spike         False             The history spiking states of the pre-synaptic neurons.
  ================ ================== =========================================================

  **References**

  .. [1] Sterratt, David, Bruce Graham, Andrew Gillies, and David Willshaw.
          "The Synapse." Principles of Computational Modelling in Neuroscience.
          Cambridge: Cambridge UP, 2011. 172-95. Print.
  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, Tensor, Dict[str, Tensor]],
      g_max: Parameter = 1.,
      tau: Parameter = 8.0,
      E: Parameter = 0.,
      delay_step: Parameter = None,
      method: str = 'exp_auto',
      name: str = None
  ):
    super(ExpCOBA, self).__init__(pre=pre, post=post, conn=conn,
                                  g_max=g_max, delay_step=delay_step,
                                  tau=tau, method=method, name=name)

    # parameter
    self.E = E

  def update(self, _t, _dt):
    if self.delay_type == 'homo':
      delayed_spike = self.pre_spike(self.delay_step)
      self.pre_spike.update(self.pre.spike)
    elif self.delay_type == 'heter':
      delayed_spike = self.pre_spike(self.delay_step, bm.arange(self.pre.num))
      self.pre_spike.update(self.pre.spike)
    else:
      delayed_spike = self.pre.spike

    # post values
    if isinstance(self.conn, All2All):
      post_vs = bm.sum(delayed_spike)
      if not self.conn.include_self:
        post_vs = post_vs - delayed_spike
      post_vs *= self.g_max
    elif isinstance(self.conn, One2One):
      post_vs = delayed_spike * self.g_max
    else:
      post_vs = bm.pre2post_event_sum(delayed_spike, self.pre2post, self.post.num, self.g_max)

    # updates
    self.g.value = self.integral(self.g.value, _t, dt=_dt) + post_vs
    self.post.input += self.g * (self.E - self.post.V)


class DualExpCUBA(TwoEndConn):
  r"""Current-based dual exponential synapse model.

  **Model Descriptions**

  The dual exponential synapse model [1]_, also named as *difference of two exponentials* model,
  is given by:

  .. math::

    g_{\mathrm{syn}}(t)=g_{\mathrm{max}} \frac{\tau_{1} \tau_{2}}{
        \tau_{1}-\tau_{2}}\left(\exp \left(-\frac{t-t_{0}}{\tau_{1}}\right)
        -\exp \left(-\frac{t-t_{0}}{\tau_{2}}\right)\right)

  where :math:`\tau_1` is the time constant of the decay phase, :math:`\tau_2`
  is the time constant of the rise phase, :math:`t_0` is the time of the pre-synaptic
  spike, :math:`g_{\mathrm{max}}` is the maximal conductance.

  However, in practice, this formula is hard to implement. The equivalent solution is
  two coupled linear differential equations [2]_:

  .. math::

      \begin{aligned}
      &g_{\mathrm{syn}}(t)=g_{\mathrm{max}} g \\
      &\frac{d g}{d t}=-\frac{g}{\tau_{\mathrm{decay}}}+h \\
      &\frac{d h}{d t}=-\frac{h}{\tau_{\text {rise }}}+ \delta\left(t_{0}-t\right),
      \end{aligned}

  The current onto the post-synaptic neuron is given by

  .. math::

      I_{syn}(t) = g_{\mathrm{syn}}(t).


  **Model Examples**


  .. plot::
    :include-source: True

    >>> import brainpy as bp
    >>> import matplotlib.pyplot as plt
    >>>
    >>> neu1 = bp.dyn.LIF(1)
    >>> neu2 = bp.dyn.LIF(1)
    >>> syn1 = bp.dyn.DualExpCUBA(neu1, neu2, bp.connect.All2All())
    >>> net = bp.dyn.Network(pre=neu1, syn=syn1, post=neu2)
    >>>
    >>> runner = bp.dyn.DSRunner(net, inputs=[('pre.input', 25.)], monitors=['pre.V', 'post.V', 'syn.g', 'syn.h'])
    >>> runner.run(150.)
    >>>
    >>> fig, gs = bp.visualize.get_figure(2, 1, 3, 8)
    >>> fig.add_subplot(gs[0, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['pre.V'], label='pre-V')
    >>> plt.plot(runner.mon.ts, runner.mon['post.V'], label='post-V')
    >>> plt.legend()
    >>>
    >>> fig.add_subplot(gs[1, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['syn.g'], label='g')
    >>> plt.plot(runner.mon.ts, runner.mon['syn.h'], label='h')
    >>> plt.legend()
    >>> plt.show()


  **Model Parameters**

  ============= ============== ======== ===================================================================================
  **Parameter** **Init Value** **Unit** **Explanation**
  ------------- -------------- -------- -----------------------------------------------------------------------------------
  delay         0              ms       The decay length of the pre-synaptic spikes.
  tau_decay     10             ms       The time constant of the synaptic decay phase.
  tau_rise      1              ms       The time constant of the synaptic rise phase.
  g_max         1              µmho(µS) The maximum conductance.
  ============= ============== ======== ===================================================================================


  **Model Variables**

  ================ ================== =========================================================
  **Member name**  **Initial values** **Explanation**
  ---------------- ------------------ ---------------------------------------------------------
  g                  0                 Synapse conductance on the post-synaptic neuron.
  s                  0                 Gating variable.
  pre_spike          False             The history spiking states of the pre-synaptic neurons.
  ================ ================== =========================================================

  **References**

  .. [1] Sterratt, David, Bruce Graham, Andrew Gillies, and David Willshaw.
         "The Synapse." Principles of Computational Modelling in Neuroscience.
         Cambridge: Cambridge UP, 2011. 172-95. Print.
  .. [2] Roth, A., & Van Rossum, M. C. W. (2009). Modeling Synapses. Computational
         Modeling Methods for Neuroscientists.

  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, Tensor, Dict[str, Tensor]],
      g_max: Parameter = 1.,
      tau_decay: Parameter = 10.0,
      tau_rise: Parameter = 1.,
      delay_step: Parameter = None,
      method: str = 'exp_auto',
      name: str = None
  ):
    super(DualExpCUBA, self).__init__(pre=pre, post=post, conn=conn, name=name)
    self.check_pre_attrs('spike')
    self.check_post_attrs('input')

    # parameters
    self.tau_rise = tau_rise
    self.tau_decay = tau_decay
    self.g_max = g_max

    # connections
    if not isinstance(self.conn, One2One):
      self.pre_ids, self.post_ids = self.conn.require('pre_ids', 'post_ids')

    # variables
    if isinstance(self.conn, One2One):
      self.h = bm.Variable(bm.zeros(self.post.num))
      self.g = bm.Variable(bm.zeros(self.post.num))
    elif isinstance(self.conn, All2All):
      self.h = bm.Variable(bm.zeros(self.pre.num))
      self.g = bm.Variable(bm.zeros(self.pre.num))
    else:
      self.h = bm.Variable(bm.zeros(self.pre.num))
      self.g = bm.Variable(bm.zeros(self.pre_ids.size))
    delay_type, delay_step, delay_value = init_delay(delay_step, self.pre.spike)
    self.delay_type = delay_type
    self.delay_step = delay_step
    self.pre_spike = delay_value

    # integral
    self.int_h = odeint(method=method, f=lambda h, t: -h / self.tau_rise)
    self.int_g = odeint(method=method, f=lambda g, t, h: -g / self.tau_decay + h)

  def update(self, _t, _dt):
    # delays
    if self.delay_type == 'homo':
      delayed_pre_spike = self.pre_spike(self.delay_step)
      self.pre_spike.update(self.pre.spike)
    elif self.delay_type == 'heter':
      delayed_pre_spike = self.pre_spike(self.delay_step, bm.arange(self.pre.num))
      self.pre_spike.update(self.pre.spike)
    else:
      delayed_pre_spike = self.pre.spike

    # post-synaptic values
    if isinstance(self.conn, All2All):
      self.g.value = self.int_g(self.g, _t, self.h, _dt)
      self.h.value = self.int_h(self.h, _t, _dt) + delayed_pre_spike
      post_vs = self.g.sum()
      if not self.conn.include_self:
        post_vs = post_vs - self.g
      post_vs = self.g_max * post_vs
    elif isinstance(self.conn, One2One):
      self.g.value = self.int_g(self.g, _t, self.h, _dt)
      self.h.value = self.int_h(self.h, _t, _dt) + delayed_pre_spike
      post_vs = self.g_max * self.g
    else:
      self.g.value = self.int_g(self.g, _t, bm.pre2syn(self.h, self.pre_ids), _dt)
      self.h.value = self.int_h(self.h, _t, _dt) + delayed_pre_spike
      post_vs = self.g_max * bm.syn2post(self.g, self.post_ids, self.post.num)

    # output
    self.post.input += self.output(post_vs)

  def output(self, g_post):
    return g_post


class DualExpCOBA(DualExpCUBA):
  """Conductance-based dual exponential synapse model.

  **Model Descriptions**

  The conductance-based dual exponential synapse model is similar with the
  `current-based dual exponential synapse model <./brainmodels.synapses.DualExpCUBA.rst>`_,
  except the expression which output onto the post-synaptic neurons:

  .. math::

      I_{syn}(t) = g_{\mathrm{syn}}(t) (V(t)-E)

  where :math:`V(t)` is the membrane potential of the post-synaptic neuron,
  :math:`E` is the reversal potential.

  **Model Examples**

  .. plot::
    :include-source: True

    >>> import brainpy as bp
    >>> import matplotlib.pyplot as plt
    >>>
    >>> neu1 = bp.dyn.HH(1)
    >>> neu2 = bp.dyn.HH(1)
    >>> syn1 = bp.dyn.DualExpCOBA(neu1, neu2, bp.connect.All2All(), E=0.)
    >>> net = bp.dyn.Network(pre=neu1, syn=syn1, post=neu2)
    >>>
    >>> runner = bp.dyn.DSRunner(net, inputs=[('pre.input', 5.)], monitors=['pre.V', 'post.V', 'syn.g', 'syn.h'])
    >>> runner.run(150.)
    >>>
    >>> fig, gs = bp.visualize.get_figure(2, 1, 3, 8)
    >>> fig.add_subplot(gs[0, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['pre.V'], label='pre-V')
    >>> plt.plot(runner.mon.ts, runner.mon['post.V'], label='post-V')
    >>> plt.legend()
    >>>
    >>> fig.add_subplot(gs[1, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['syn.g'], label='g')
    >>> plt.plot(runner.mon.ts, runner.mon['syn.h'], label='h')
    >>> plt.legend()
    >>> plt.show()


  **Model Parameters**

  ============= ============== ======== ===================================================================================
  **Parameter** **Init Value** **Unit** **Explanation**
  ------------- -------------- -------- -----------------------------------------------------------------------------------
  delay         0              ms       The decay length of the pre-synaptic spikes.
  tau_decay     10             ms       The time constant of the synaptic decay phase.
  tau_rise      1              ms       The time constant of the synaptic rise phase.
  g_max         1              µmho(µS) The maximum conductance.
  E             0              mV       The reversal potential for the synaptic current.
  ============= ============== ======== ===================================================================================


  **Model Variables**

  ================ ================== =========================================================
  **Member name**  **Initial values** **Explanation**
  ---------------- ------------------ ---------------------------------------------------------
  g                  0                 Synapse conductance on the post-synaptic neuron.
  s                  0                 Gating variable.
  pre_spike          False             The history spiking states of the pre-synaptic neurons.
  ================ ================== =========================================================

  **References**

  .. [1] Sterratt, David, Bruce Graham, Andrew Gillies, and David Willshaw.
         "The Synapse." Principles of Computational Modelling in Neuroscience.
         Cambridge: Cambridge UP, 2011. 172-95. Print.

  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, Tensor, Dict[str, Tensor]],
      g_max: Parameter = 1.,
      tau_decay: Parameter = 10.0,
      tau_rise: Parameter = 1.,
      E: Parameter = 0.,
      delay_step: Parameter = None,
      method: str = 'exp_auto',
      name: str = None
  ):
    super(DualExpCOBA, self).__init__(pre, post, conn,
                                      delay_step=delay_step, g_max=g_max,
                                      tau_decay=tau_decay, tau_rise=tau_rise,
                                      method=method, name=name)
    self.check_post_attrs('V')

    # parameters
    self.E = E

  def output(self, g_post):
    return g_post * (self.E - self.post.V)


class AlphaCUBA(DualExpCUBA):
  r"""Current-based alpha synapse model.

  **Model Descriptions**

  The analytical expression of alpha synapse is given by:

  .. math::

      g_{syn}(t)= g_{max} \frac{t-t_{s}}{\tau} \exp \left(-\frac{t-t_{s}}{\tau}\right).

  While, this equation is hard to implement. So, let's try to convert it into the
  differential forms:

  .. math::

      \begin{aligned}
      &g_{\mathrm{syn}}(t)= g_{\mathrm{max}} g \\
      &\frac{d g}{d t}=-\frac{g}{\tau}+h \\
      &\frac{d h}{d t}=-\frac{h}{\tau}+\delta\left(t_{0}-t\right)
      \end{aligned}

  The current onto the post-synaptic neuron is given by

  .. math::

      I_{syn}(t) = g_{\mathrm{syn}}(t).


  **Model Examples**

  .. plot::
    :include-source: True

    >>> import brainpy as bp
    >>> import matplotlib.pyplot as plt
    >>>
    >>> neu1 = bp.dyn.LIF(1)
    >>> neu2 = bp.dyn.LIF(1)
    >>> syn1 = bp.dyn.AlphaCUBA(neu1, neu2, bp.connect.All2All())
    >>> net = bp.dyn.Network(pre=neu1, syn=syn1, post=neu2)
    >>>
    >>> runner = bp.dyn.DSRunner(net, inputs=[('pre.input', 25.)], monitors=['pre.V', 'post.V', 'syn.g', 'syn.h'])
    >>> runner.run(150.)
    >>>
    >>> fig, gs = bp.visualize.get_figure(2, 1, 3, 8)
    >>> fig.add_subplot(gs[0, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['pre.V'], label='pre-V')
    >>> plt.plot(runner.mon.ts, runner.mon['post.V'], label='post-V')
    >>> plt.legend()
    >>> fig.add_subplot(gs[1, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['syn.g'], label='g')
    >>> plt.plot(runner.mon.ts, runner.mon['syn.h'], label='h')
    >>> plt.legend()
    >>> plt.show()

  **Model Parameters**

  ============= ============== ======== ===================================================================================
  **Parameter** **Init Value** **Unit** **Explanation**
  ------------- -------------- -------- -----------------------------------------------------------------------------------
  delay         0              ms       The decay length of the pre-synaptic spikes.
  tau_decay     2              ms       The decay time constant of the synaptic state.
  g_max         .2             µmho(µS) The maximum conductance.
  ============= ============== ======== ===================================================================================

  **Model Variables**

  ================== ================= =========================================================
  **Variables name** **Initial Value** **Explanation**
  ------------------ ----------------- ---------------------------------------------------------
  g                   0                Synapse conductance on the post-synaptic neuron.
  h                   0                Gating variable.
  pre_spike           False            The history spiking states of the pre-synaptic neurons.
  ================== ================= =========================================================

  **References**

  .. [1] Sterratt, David, Bruce Graham, Andrew Gillies, and David Willshaw.
          "The Synapse." Principles of Computational Modelling in Neuroscience.
          Cambridge: Cambridge UP, 2011. 172-95. Print.
  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, Tensor, Dict[str, Tensor]],
      g_max: Parameter = 1.,
      tau_decay: Parameter = 10.0,
      delay_step: Parameter = None,
      method: str = 'exp_auto',
      name: str = None
  ):
    super(AlphaCUBA, self).__init__(pre=pre, post=post, conn=conn,
                                    delay_step=delay_step,
                                    g_max=g_max,
                                    tau_decay=tau_decay,
                                    tau_rise=tau_decay,
                                    method=method,
                                    name=name)


class AlphaCOBA(DualExpCOBA):
  """Conductance-based alpha synapse model.

  **Model Descriptions**

  The conductance-based alpha synapse model is similar with the
  `current-based alpha synapse model <./brainmodels.synapses.AlphaCUBA.rst>`_,
  except the expression which output onto the post-synaptic neurons:

  .. math::

      I_{syn}(t) = g_{\mathrm{syn}}(t) (V(t)-E)

  where :math:`V(t)` is the membrane potential of the post-synaptic neuron,
  :math:`E` is the reversal potential.


  **Model Examples**

  .. plot::
    :include-source: True

    >>> import brainpy as bp
    >>> import matplotlib.pyplot as plt
    >>>
    >>> neu1 = bp.dyn.HH(1)
    >>> neu2 = bp.dyn.HH(1)
    >>> syn1 = bp.dyn.AlphaCOBA(neu1, neu2, bp.connect.All2All(), E=0.)
    >>> net = bp.dyn.Network(pre=neu1, syn=syn1, post=neu2)
    >>>
    >>> runner = bp.dyn.DSRunner(net, inputs=[('pre.input', 5.)], monitors=['pre.V', 'post.V', 'syn.g', 'syn.h'])
    >>> runner.run(150.)
    >>>
    >>> fig, gs = bp.visualize.get_figure(2, 1, 3, 8)
    >>> fig.add_subplot(gs[0, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['pre.V'], label='pre-V')
    >>> plt.plot(runner.mon.ts, runner.mon['post.V'], label='post-V')
    >>> plt.legend()
    >>> fig.add_subplot(gs[1, 0])
    >>> plt.plot(runner.mon.ts, runner.mon['syn.g'], label='g')
    >>> plt.plot(runner.mon.ts, runner.mon['syn.h'], label='h')
    >>> plt.legend()
    >>> plt.show()


  **Model Parameters**

  ============= ============== ======== ===================================================================================
  **Parameter** **Init Value** **Unit** **Explanation**
  ------------- -------------- -------- -----------------------------------------------------------------------------------
  delay         0              ms       The decay length of the pre-synaptic spikes.
  tau_decay     2              ms       The decay time constant of the synaptic state.
  g_max         .2             µmho(µS) The maximum conductance.
  E             0              mV       The reversal potential for the synaptic current.
  ============= ============== ======== ===================================================================================


  **Model Variables**

  ================== ================= =========================================================
  **Variables name** **Initial Value** **Explanation**
  ------------------ ----------------- ---------------------------------------------------------
  g                   0                Synapse conductance on the post-synaptic neuron.
  h                   0                Gating variable.
  pre_spike           False            The history spiking states of the pre-synaptic neurons.
  ================== ================= =========================================================

  **References**

  .. [1] Sterratt, David, Bruce Graham, Andrew Gillies, and David Willshaw.
          "The Synapse." Principles of Computational Modelling in Neuroscience.
          Cambridge: Cambridge UP, 2011. 172-95. Print.

  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, Tensor, Dict[str, Tensor]],
      g_max: Parameter = 1.,
      tau_decay: Parameter = 10.0,
      E: Parameter = 0.,
      delay_step: Parameter = None,
      method: str = 'exp_auto',
      name: str = None
  ):
    super(AlphaCOBA, self).__init__(pre=pre, post=post, conn=conn,
                                    delay_step=delay_step,
                                    g_max=g_max, E=E,
                                    tau_decay=tau_decay,
                                    tau_rise=tau_decay,
                                    method=method,
                                    name=name)
