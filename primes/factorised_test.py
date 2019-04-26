#!/usr/bin/env python3


from algutils.primes import factorised

import unittest


class TestFactorised(unittest.TestCase):
  def test_corner_cases(self):
    with self.assertRaises(ValueError):
      _ = factorised.Factorised(-1)

    with self.assertRaises(ValueError):
      _ = factorised.Factorised(0)

    f = factorised.Factorised()  # Defaults to 1.
    self.assertEqual(f.factors, {})
    self.assertEqual(int(f), 1)

    f = factorised.Factorised(1)
    self.assertEqual(f.factors, {})
    self.assertEqual(int(f), 1)

    f = factorised.Factorised(2)
    self.assertEqual(f.factors, {2: 1})
    self.assertEqual(int(f), 2)

    f = factorised.Factorised(3)
    self.assertEqual(f.factors, {3: 1})
    self.assertEqual(int(f), 3)

    f = factorised.Factorised(4)
    self.assertEqual(f.factors, {2: 2})
    self.assertEqual(int(f), 4)

    f = factorised.Factorised(5)
    self.assertEqual(f.factors, {5: 1})
    self.assertEqual(int(f), 5)

    f = factorised.Factorised(6)
    self.assertEqual(f.factors, {2:1, 3: 1})
    self.assertEqual(int(f), 6)

  def test_multiplication(self):
    a = factorised.Factorised(764)
    b = factorised.Factorised(992)

    self.assertEqual((a * b).factors, {2: 7, 31: 1, 191: 1})
    self.assertEqual(int(a), 764)
    self.assertEqual(int(b), 992)

    a *= b
    self.assertEqual(a.factors, {2: 7, 31: 1, 191: 1})
    self.assertEqual(int(a), 764 * 992)

  def test_division(self):
    a = factorised.Factorised(151)
    b = factorised.Factorised(242)

    self.assertEqual((a / b).factors, {2: -1, 11: -2, 151:1})
    self.assertEqual(int(a), 151)
    self.assertEqual(int(b), 242)

    a /= b
    self.assertEqual(a.factors, {2: -1, 11: -2, 151:1})
    self.assertEqual(int(a), 0)  # 0 < 151 / 242 < 1

  def test_exponentiation(self):
    f = factorised.Factorised(165)
    e = 96

    self.assertEqual((f**e).factors, {3: e, 5: e, 11: e})
    self.assertEqual(int(f), 165)

    f **= e
    self.assertEqual(f.factors, {3: e, 5: e, 11: e})
    self.assertEqual(int(f), 165**e)


if __name__ == '__main__':
  unittest.main()

