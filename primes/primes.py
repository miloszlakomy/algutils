#!/usr/bin/env python3


def sieve(lim):
  if lim <= 2:
    return []

  ret = [2]
  si = list(range(3, lim, 2))

  for i in range(len(si)):
    p = si[i]
    if p is None:
      continue

    ret.append(p)

    for j in range(i+p, len(si), p):
      si[j] = None

  return ret

