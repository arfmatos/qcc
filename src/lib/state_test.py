# python3

import random

from absl.testing import absltest
import numpy as np

from src.lib import state


class StateTest(absltest.TestCase):

  def test_simple_state(self):
    psi = state.zero
    self.assertEqual(psi[0], 1)
    self.assertEqual(psi[1], 0)

    psi = state.one
    self.assertEqual(psi[0], 0)
    self.assertEqual(psi[1], 1)

    psi = state.zeros(8)
    self.assertEqual(psi[0], 1)
    for i in range(1, 2**8 - 1):
      self.assertEqual(psi[i], 0)

    psi = state.ones(8)
    for i in range(0, 2**8 - 2):
      self.assertEqual(psi[i], 0)
    self.assertEqual(psi[2**8 - 1], 1)

    psi = state.rand(8)
    self.assertEqual(psi.nbits, 8)

  def test_probabilities(self):
    psi = state.bitstring(0, 1, 1)
    self.assertEqual(psi.prob(0, 0, 0), 0.0)
    self.assertEqual(psi.prob(0, 0, 1), 0.0)
    self.assertEqual(psi.prob(0, 1, 0), 0.0)
    self.assertEqual(psi.prob(0, 1, 1), 1.0)
    self.assertEqual(psi.prob(1, 0, 0), 0.0)
    self.assertEqual(psi.prob(1, 0, 1), 0.0)
    self.assertEqual(psi.prob(1, 1, 0), 0.0)
    self.assertEqual(psi.prob(1, 1, 1), 0.0)

  def test_schmidt(self):
    psi = state.zeros(2)
    self.assertEqual(psi.schmidt_number([1]), 1.0)

    psi = state.bitstring(0, 1, 1, 0, 1, 0, 1, 1)
    self.assertEqual(psi.schmidt_number([1]), 1.0)

    psi = state.State(np.array([1.0, 1.0, 0.0, 1.0]))
    self.assertNotEqual(psi.schmidt_number([1]), 1.0)

  def test_density(self):
    psi = state.bitstring(1, 0)
    rho = psi.density()
    self.assertTrue(rho.is_density())
    self.assertTrue(rho.is_hermitian())
    self.assertTrue(rho.is_pure())
    self.assertFalse(rho.is_unitary())

  def test_regs(self):
    a = state.Reg(3, [0, 1, 1], 0)
    b = state.Reg(3, [0, 0, 1], 3)
    psi = state.fromregs(a, b)
    psi_manual = state.bitstring(0, 1, 1, 0, 0, 1)
    self.assertEqual(a[0], 0)
    self.assertEqual(b[0], 3)
    self.assertTrue(psi.is_close(psi_manual))

    a = state.Reg(3, 1, 0)
    self.assertEqual('|001>', str(a))
    a = state.Reg(3, 6, 3)
    self.assertEqual('|110>', str(a))
    a = state.Reg(3, 7, 6)
    self.assertEqual('|111>', str(a))

    a = state.Reg(3, [1, 0, 0], 3)
    self.assertEqual('|100>', str(a))
    a = state.Reg(3, [0, 1, 1], 6)
    self.assertEqual('|011>', str(a))
    a = state.Reg(3, [1, 1, 1], 9)
    self.assertEqual('|111>', str(a))

  def test_ordering(self):
    a = state.Reg(3, [0, 0, 0], 0)
    self.assertGreater(a.psi()[0], 0.99)
    a = state.Reg(3, [0, 0, 1], 3)
    self.assertGreater(a.psi()[1], 0.99)
    a = state.Reg(3, [1, 1, 0], 6)
    self.assertGreater(a.psi()[6], 0.99)
    a = state.Reg(3, [1, 1, 1], 9)
    self.assertGreater(a.psi()[7], 0.99)

    psi = state.bitstring(0, 0, 0)
    self.assertGreater(psi[0], 0.99)
    psi = state.bitstring(0, 0, 1)
    self.assertGreater(psi[1], 0.99)
    psi = state.bitstring(1, 1, 0)
    self.assertGreater(psi[6], 0.99)
    psi = state.bitstring(1, 1, 1)
    self.assertGreater(psi[7], 0.99)

  def test_mult_conjugates(self):
    a = state.qubit(0.6)
    b = state.qubit(0.8)
    psi = a * b
    psi_adj = np.conj(a) * np.conj(b)
    self.assertTrue(np.allclose(psi_adj, np.conj(psi)))

    i1 = np.conj(np.inner(a, b))
    i2 = np.inner(b, a)
    self.assertTrue(np.allclose(i1, i2))

  def test_inner_tensor_product(self):
    p1 = state.qubit(random.random())
    p2 = state.qubit(random.random())
    x1 = state.qubit(random.random())
    x2 = state.qubit(random.random())

    psi1 = p1 * x1
    psi2 = p2 * x2
    inner1 = np.inner(psi1.conj(), psi2)
    inner2 = np.inner(p1.conj(), p2) * np.inner(x1.conj(), x2)
    self.assertTrue(np.allclose(inner1, inner2))

    self.assertTrue(np.allclose(np.inner(psi1.conj(), psi1), 1.0))
    self.assertTrue(np.allclose(np.inner(p1.conj(), p1) *
                                np.inner(x1.conj(), x1), 1.0))

  def test_normalize(self) -> None:
    denormalized = state.State([1.0, 1.0])
    denormalized.normalize()
    assert np.allclose(denormalized, state.State([0.5 ** 0.5, 0.5 ** 0.5]))


if __name__ == '__main__':
  absltest.main()
