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
  p = [(-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1, 0) ,
            (-1,  1), (0,  1), (1, 1) ]
  def __init__(self, W, H):
    self.W = W
    self.H = H
    self.s = []
    for y in range(H):
      self.s += [[]]
      for x in range(W):
        self.s[y] += [[-2, 0, 0]] # -2 = not known
  def add(self, x, y, s):
    self.s[y][x] = [s, 0, 0]
  def view(self):
    for y in self.s:
      for x in y:
        if x[0] == -2:
          x = ['?']
        elif x[0] == -1:
          x = ['#']
        elif x[0] == 0:
          x = [' ']
        elif x[0] == -3:
          x = ['X']
        print(x[0], end='')
      print()
  def get(self, x, y, p=5):
    # 123
    # 456
    # 789
    p -= 1
    x += self.p[p][0]
    y += self.p[p][1]
    if x<0 or x>=self.W or y<0 or y>=self.H:
      return [-1] # -1 = out of range
    return self.s[y][x]
  def set(self, x, y, z, p=5):
    # 123
    # 456
    # 789
    p -= 1
    x += self.p[p][0]
    y += self.p[p][1]
    if x<0 or x>=self.W or y<0 or y>=self.H:
      return
    self.s[y][x] = [z, 0, 0]
  def update(self):
    b = 0
    ob = -1
    while b != ob:
      for y in range(self.H):
        for x in range(self.W):
          bs = 0
          nk = 0
          for p in range(1, 10):
            if p == 5:
              continue
            a = self.get(x, y, p)
            if a[0] == -2: # not known
             nk += 1
             if a[0] == -3: # bombs
               bs += 1
          self.s[y][x][1] = bs
          self.s[y][x][2] = nk
          a = self.s[x][y]
          if a[0]-bs > nk:
            print('WARN: impossible (x', x, ' y', y, ' a', a, ')', sep='')
          elif a[0]-bs == nk:
            for p in range(1,10):
              if p == 5:
                continue
              a = self.get(x, y, p)
              if a[0] == -2:
                self.set(x, y, -3, p)
                b += 1
      ob = b
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

if __name__ == '__main__':
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
    s.update()
    s.view()
    inp(s, False)
