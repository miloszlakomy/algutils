#!/usr/bin/env python3


from algutils.primes import factorisation

import unittest


class TestFactorise(unittest.TestCase):
  def test_corner_cases(self):
    with self.assertRaises(ValueError):
      factorisation.factorise(-1)

    with self.assertRaises(ValueError):
      factorisation.factorise(0)

    self.assertEqual(factorisation.factorise(1), {})
    self.assertEqual(factorisation.factorise(2), {2: 1})
    self.assertEqual(factorisation.factorise(3), {3: 1})
    self.assertEqual(factorisation.factorise(4), {2: 2})
    self.assertEqual(factorisation.factorise(5), {5: 1})
    self.assertEqual(factorisation.factorise(6), {2: 1, 3:1})

  def test_factorise(self):
    self.assertEqual(factorisation.factorise(782), {2: 1, 17: 1, 23: 1})
    self.assertEqual(factorisation.factorise(775), {5: 2, 31: 1})
    self.assertEqual(factorisation.factorise(244), {2: 2, 61: 1})


if __name__ == '__main__':
  unittest.main()

