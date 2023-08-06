"""Time series data.

Rewrite of old timedtuple.py.

"""
import logging as log
from amphetype import timer
import re

def median(lst):
  lst, n = sorted(lst), len(lst)
  if not n:
    return None
  res = lst[n//2]
  if n % 2 == 0:
    res += lst[n//2+1]
    res /= 2.0
  return res


class table(tuple):
  """Poor man's NumPy.

  A table is here defined as a static tuple of columns (lists).
  """
  def __getattr__(self, key):
    return type(self)(getattr(x, key) for x in self)

  def __getitem__(self, idx):
    if isinstance(idx, list):
      return type(self)(self[i] for i in idx)
    res = super().__getitem__(idx)
    if isinstance(idx, slice):
      return type(self)(res)
    return res

  def split(self, pred, keep_empty=True):
    if not callable(pred):
      pred = lambda x, y=pred: x == y

    cur = []
    for x in self:
      if pred(x):
        if keep_empty or cur:
          yield type(self)(cur)
        cur = []
      else:
        cur.append(x)
    if keep_empty or cur:
      yield type(self)(cur)



class timed_string(table):
  COLUMNS = ('time', 'char')

  def push(self, char):
    self.append(timer(), char)


# This is a test.
# Ths\b is a test.

# ABCD
# A|     type C
# AC|    type D
# A_CD|
#
#
# ABCD
# A|     type Q
# AQ|    type B
# AQB|   type C
# AQBC|
#
#
# ABCD
# A|
# AC|
# ACB|

# ABCDEFGH
#
# ADEF

from functools import lru_cache


def dalev(a, b):
  @lru_cache(maxsize=None)
  def d(i, j):
    if i == 0 and j == 0:
        return ''
    cands = []
    if i > 0:
        cands.append(d(i-1,j) + 'd')
    if j > 0:
        cands.append(d(i,j-1) + 'i')
    if j > 0 and i > 0:
        x = d(i-1,j-1)
        cands.append(x + 'm' if a[i-1] != b[j-1] else x)
        if j > 1 and i > 1 and a[i-2] == b[j-1] and a[i-1] == b[j-2]:
          cands.append(d(i-2,j-2) + 't')
    return min(cands, key=len)

  return d(len(a), len(b))


class incremental_edit_distance():

  def push(self, char):

    self._d.append([self.tlen] * self.tlen)

    for j in range(1, self.tlen):
      self._d[i-1, j]

  def pop(self):


    for j in range(len(self._target)):
      pass



def on_press(key):
  print('press', key)
  if key.char == 'g':
    return False
  return True

def on_release(key):
  print('release', key)
  return True

from pynput import keyboard
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()


class matcher():
  COLUMNS = ('state', 'time', 'char')

  # ('correct', "..."), ('error', "..."), ('anyerror', "...")

  def append(self, char):

    #process as usual

    pass

  def fixup(self):
    prev = self[-2:]
    if len(prev) != 2:
      return


    if self.last and self.last.state == 'error':
      pass
    pass

  def backspace(self):
    if not self.last:
      return

    if not self.erase_correct and not self.any_error:
      return

    self.future.push(self.pop())


