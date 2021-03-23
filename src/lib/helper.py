# python3
"""Helper functions."""

import itertools
import math
from typing import List, Sequence

import numpy as np


def bitprod(nbits):
  """Produce the iterable cartesian of nbits {0, 1}."""

  for bits in itertools.product([0, 1], repeat=nbits):
    yield bits


def bits2val(bits: Sequence[int]) -> int:
  """For given bits, compute the decimal integer."""

  # We assume bits are given in high to low order. For example,
  # the bits [1, 1, 0] will produce the value 6.
  return sum(v * (1 << (len(bits)-i-1)) for i, v in enumerate(bits))


def val2bits(val: int, nbits: int) -> List[int]:
  """Convert decimal integer to list of {0, 1}."""

  # We return the bits in order high to low. For example,
  # the value 6 is being returned as [1, 1, 0].
  return [int(c) for c in format(val, f'0{nbits}b')]


def bits2frac(bits, length):
  """For given bits, compute the binary fraction."""

  return sum(bits[i] * 2**(-i-1) for i in range(length))


def density_to_cartesian(rho):
  """Compute Bloch sphere coordinates from 2x2 density matrix."""

  a = rho[0, 0]
  b = rho[1, 0]
  x = 2.0 * b.real
  y = 2.0 * b.imag
  z = 2.0 * a - 1.0

  return np.real(x), np.real(y), np.real(z)


def qubit_to_bloch(psi):
  """Compute Bloch spere coordinates from 2x1 state vector/qubit."""

  return density_to_cartesian(psi.density())


def dump_bloch(x, y, z):
  """Textual output for Bloch sphere coordinates."""

  print(f'x: {x:.2f}, y: {y:.2f}, z: {z:.2f}')


def qubit_dump_bloch(psi):
  """Print Bloch coordinates for state psi."""

  x, y, z = helper.qubit_to_bloch(psi)
  helper.dump_bloch(x, y, z)


def pi_fractions(val, pi='pi') -> str:
  """Convert a value in fractions of pi."""

  if val is None:
    return ''
  if val == 0:
    return '0'
  for pi_multiplier in range(1, 4):
    for denom in range(-128, 128):
      if denom and math.isclose(val, pi_multiplier * math.pi / denom):
        pi_str = ''
        if pi_multiplier != 1:
          pi_str = f'{abs(pi_multiplier)}*'
        if denom == -1:
          return f'-{pi_str}{pi}'
        if denom < 0:
          return f'-{pi_str}{pi}/{-denom}'
        if denom == 1:
          return f'{pi_str}{pi}'
        return f'{pi_str}{pi}/{denom}'

  # couldn't find fractional, just return original value.
  return f'{val}'
