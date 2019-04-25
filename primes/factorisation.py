#!/usr/bin/env python3


from algutils.primes import cached_primes


def factorise(n):
  if n <= 0:
    raise ValueError("n must be a positive integer")

  ps = cached_primes.get_primes_list(min_lim=int(n**.5) + 1)

  ret = {}

  for p in ps:
    if n == 1:
      break

    if p**2 > n:  # n is prime
      break

    if n % p == 0:
      n //= p
      v = 1
      while n % p == 0:
        n //= p
        v += 1
      ret[p] = v

  if n > 1:  # n is prime
    ret[n] = 1

  return ret

