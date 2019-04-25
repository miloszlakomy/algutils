#!/usr/bin/env python3


from algutils.primes import primes


_PRIMES = [2, 3]
_SET_PRIMES = set(_PRIMES)


def _precompute_primes(min_lim):
  global _PRIMES, _SET_PRIMES

  if _PRIMES[-1] < min_lim - 1:
    _PRIMES = primes.sieve(min_lim)
    _SET_PRIMES = set(_PRIMES)

def is_prime(n):
  lim = int(n**.5) + 1
  _precompute_primes(min_lim=lim)

  if n <= _PRIMES[-1]:
    return n in _SET_PRIMES

  for p in _PRIMES:
    if p > lim:
      break

    if n % p == 0:
      return False

  return True

def get_primes_list(min_lim):
  _precompute_primes(min_lim)
  return _PRIMES

def get_primes_set(min_lim):
  _precompute_primes(min_lim)
  return _SET_PRIMES

