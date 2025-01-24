#!/usr/bin/env python3


from algutils.primes import cached_primes

import unittest


class TestIsPrime(unittest.TestCase):
  def test_is_prime(self):
    sps = {2, 3, 5, 7, 11, 13, 17, 19}
    lim = 23

    for i in range(lim):
      self.assertEqual(cached_primes.is_prime(i), i in sps)


class TestGetPrimesList(unittest.TestCase):
  def test_get_primes_list(self):
    want = [2, 3, 5, 7, 11, 13, 17, 19]
    got = cached_primes.get_primes_list(min_lim=23)

    self.assertEqual(want, got[:len(want)])


class TestGetPrimesSet(unittest.TestCase):
  def test_get_primes_set(self):
    want = {2, 3, 5, 7, 11, 13, 17, 19}
    got = cached_primes.get_primes_set(min_lim=23)

    self.assertTrue(want <= got)


if __name__ == '__main__':
  unittest.main()

