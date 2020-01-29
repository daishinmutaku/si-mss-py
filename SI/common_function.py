# coding: utf-8
"""
Commonly used functions and classes
"""

import numpy as np
import copy
from mpmath import mp
mp.dps = 3000

#----------------------------------------------------------------------
#切断正規分布の累積分布を計算する関数
def tn_cdf(x, intervals, mean=0, var=1):
  """
  CDF of a truncated normal distribution

  [Parameters]
    x <float> : Return the value at x
    intervals <list np.ndarray> : [L, U] or [[L1, U1], [L2, U2],...]
    mean <float>
    var <float>

  [Returns]
    float : CDF of TN
  """
  x = mp.mpf(x)
  intervals = np.array(intervals)

  if len(intervals.shape) == 1:
    intervals = np.array([intervals])

  n_intervals = len(intervals)  # number of intervals
  sd = mp.sqrt(var)  # standard deviation


  # locate the interval that contains x
  threshold = 1e-15
  for i in range(n_intervals):
    # if abs(intervals[i][0] - x) < threshold or abs(intervals[i][1] - x) < threshold:
    #     return float(0)
    if intervals[i][0] <= x <= intervals[i][1]:
      x_index = i
      break
  else:
    # raise ValueError(f'tn_cdf at x={x} is undefined.\nintervals={intervals}')
    raise ValueError("error! x:", x, ", intervals:", intervals)

  norm_intervals = (intervals - mean) / sd  # normalized intervals

  # calculate the sum(delta) in order
  delta = [0,]
  for i in range(n_intervals):
    diff = mp.ncdf(norm_intervals[i][1]) - mp.ncdf(norm_intervals[i][0])
    delta.append(delta[-1] + diff)

  numerator = mp.ncdf((x-mean)/sd) - mp.ncdf(norm_intervals[x_index][0]) + delta[x_index]
  denominator = delta[-1]

  return mp.mpf(numerator / denominator)


#----------------------------------------------------------------------

class QuadraticInterval():
  """
  Calculate the truncation intervals E(z)=∩{ατ^2+βτ+γ≦0} for quadratic
  selection events. τ is test statistic, and β,γ are function of c,z.

  [Constructor]
    tau <float> : Set tau=0 unless we consider E(z)=∩{ατ^2+κτ+λ≦0}.      κ,λ are function of c,x.
  """
  def __init__(self, tau=0, init_lower=-mp.mpf('inf'), init_upper=mp.mpf('inf')):
    self.tau = tau
    self.lower = init_lower
    self.upper = init_upper
    self.concave_intervals = []

  def cut(self, a, b, c):
    """
    Truncate the interval with a quadratic inequality ατ^2+βτ+γ≦0

    [Parameters]
      a <float> : α
      b <float> : β or κ
      c <float> : γ or λ
    """
    threshold = 1e-10
    if -threshold < a < threshold:
      a = 0
    if -threshold < b < threshold:
      b = 0
    if -threshold < c < threshold:
      c = 0

    a = mp.mpf(a)
    b = mp.mpf(b)
    c = mp.mpf(c)

    if a == 0:
      if b == 0:
        return
      elif b < 0:
        self.lower = self.mp_max(self.lower, -c/b + self.tau)
      elif b > 0:
        self.upper = self.mp_min(self.upper, -c/b + self.tau)
      # print("\t", self.lower, self.upper)
    elif a > 0:
      disc = b**2 - 4*a*c  # discriminant
      disc_sqrt = mp.sqrt(disc)
      self.lower = self.mp_max(self.lower, (-b-disc_sqrt) / (2*a) + self.tau)
      self.upper = self.mp_min(self.upper, (-b+disc_sqrt) / (2*a) + self.tau)
      # print("\t", self.lower, self.upper)
    else:
      disc = b**2 - 4*a*c  # discriminant
      if disc <= 0:  # no solution
        return
      disc_sqrt = mp.sqrt(disc)
      lower = (-b+disc_sqrt) / (2*a) + self.tau
      upper = (-b-disc_sqrt) / (2*a) + self.tau

      # To reduce the calculation cost in _concave_cut,
      # truncate the interval if it's possible at this moment
      if lower <= self.lower < upper < self.upper:
        self.lower = upper
      elif self.lower < lower < self.upper <= upper:
        self.upper = lower
      elif self.lower < lower and upper < self.upper:
        # The interval is splitted into 2 parts at this moment
        self.concave_intervals.append((lower, upper))
      if  self.lower > self.upper:
        print(self.upper - self.lower)
        exit()


  def _concave_cut(self):
    intervals = [[self.lower, self.upper],]

    for lower, upper in self.concave_intervals:
      if lower < intervals[0][0] < upper < intervals[-1][1]:
        # truncate the left side of the intervals
        for i in range(len(intervals)):
          if upper <= intervals[i][0]:
            intervals = intervals[i:]
            break
          elif intervals[i][0] < upper < intervals[i][1]:
            intervals = intervals[i:]
            intervals[0][0] = upper
            break
      elif intervals[0][0] < lower < intervals[-1][1] <= upper:
        # truncate the right side of the intervals
        for i in range(len(intervals)-1, -1, -1):
          if intervals[i][1] <= lower:
            intervals = intervals[:i+1]
            break
          elif intervals[i][0] < lower < intervals[i][1]:
            intervals = intervals[:i+1]
            intervals[-1][1] = lower
            break
      elif intervals[0][0] < lower < upper < intervals[-1][1]:
        # truncate the middle part of the intervals
        for i in range(len(intervals)):
          if upper <= intervals[i][0]:
            right_intervals = intervals[i:]
            break
          elif intervals[i][0] < upper < intervals[i][1]:
            right_intervals = copy.deepcopy(intervals[i:])
            right_intervals[0][0] = upper
            break

        for i in range(len(intervals)-1, -1, -1):
          if intervals[i][1] <= lower:
            left_intervals = intervals[:i+1]
            break
          elif intervals[i][0] < lower < intervals[i][1]:
            left_intervals = copy.deepcopy(intervals[:i+1])
            left_intervals[-1][1] = lower
            break

        intervals = left_intervals + right_intervals

    return np.array(intervals)

  def get(self):
    """
    Get the intervals

    [Returns]
      numpy.ndarray
    """
    return self._concave_cut()

  def mp_max(self, a, b):
    if a < b:
      return b
    else:
      return a

  def mp_min(self, a, b):
    if a > b:
      return b
    else:
      return a