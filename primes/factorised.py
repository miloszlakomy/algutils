#!/usr/bin/env python3


from algutils.primes import factorisation

import copy
import functools

class Factorised(object):
  def __init__(self, number=1):
    if number < 1:
      raise ValueError("Factorised number must be at least 1")

    self.factors = factorisation.factorise(number)

  def __int__(self):
    product = lambda a, b: a * b
    return int(functools.reduce(
        product, (k**v for k, v in self.factors.items()), 1))

  def _normalise(self):
    zeroes = [k for k, v in self.factors.items() if v == 0]

    for k in zeroes:
      del self.factors[k]

    return self

  def __imul__(self, other):
    for k, v in other.factors.items():
      self.factors.setdefault(k, 0)
      self.factors[k] += v

    return self._normalise()

  def __mul__(self, other):
    ret = copy.deepcopy(self)
    ret *= other

    return ret

  def __itruediv__(self, other):
    for k, v in other.factors.items():
      self.factors.setdefault(k, 0)
      self.factors[k] -= v

    return self._normalise()

  def __truediv__(self, other):
    ret = copy.deepcopy(self)
    ret /= other

    return ret

  def __ipow__(self, exponent):
    for k in self.factors.keys():
      self.factors[k] *= exponent

    return self._normalise()

  def __pow__(self, exponent):
    ret = copy.deepcopy(self)
    ret **= exponent

    return ret

