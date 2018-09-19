#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# file from https://github.com/Nircek/minesweeper-solver
# licensed under MIT license

# MIT License

# Copyright (c) 2018 Nircek

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class Minesweeper_solver:
  def __init__(self, W, H):
    self.s = []
    for y in range(H):
      self.s += [[]]
      for x in range(W):
        self.s[y] += [-1] # -1 = not known
  def add(self, x, y, s):
    self.s[y][x] = s
  def view(self):
    for y in self.s:
      for x in y:
        if x == -1:
          x = '?'
        print(x, end='')
      print()

def inp(s,l=True):
  m = True
  while m or l:
    x = input()
    x = x.split()
    for i in range(len(x)):
      x[i] = int(x[i])
    while len(x):
      s.add(x[0],x[1],x[2])
      x = x[3:]
    m = False

s = Minesweeper_solver(10, 10)
s.add(1,0,1)
s.add(1,1,2)
s.add(1,2,2)
s.add(2,2,1)
s.add(2,3,1)
s.add(2,4,2)
s.add(3,4,1)
s.add(4,4,1)
s.add(4,3,1)
s.add(4,2,1)
s.add(4,1,1)
s.add(4,0,1)
s.add(2,0,0)
s.add(2,1,0)
s.add(3,0,0)
s.add(3,1,0)
s.add(3,2,0)
s.add(3,3,0)
while 1:
  s.view()
  inp(s, False)
