#!/usr/bin/env python3


from algutils.primes import primes

import unittest


class TestSieve(unittest.TestCase):
  def test_cornercases(self):
    self.assertEqual(primes.sieve(0), [])
    self.assertEqual(primes.sieve(1), [])
    self.assertEqual(primes.sieve(2), [])
    self.assertEqual(primes.sieve(3), [2])
    self.assertEqual(primes.sieve(4), [2, 3])

  def test_sieve(self):
    lim = 100
    pi_lim = 25  # π(lim), number of primes below lim.

    ps = primes.sieve(lim)

    self.assertEqual(len(ps), pi_lim)

    for p in ps:
      self.assertLess(p, lim)

      for i in range(2, p):
        self.assertNotEqual(p % i, 0)


if __name__ == '__main__':
  unittest.main()

