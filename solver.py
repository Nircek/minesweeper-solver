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

import getch
from os import system, name
import random
from copy import deepcopy

class Minesweeper_solver:
  p = [(-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1, 0) ,
            (-1,  1), (0,  1), (1, 1) ]
  cursor = u'\u001b[41m'
  def __init__(self, W, H):
    self.W = W
    self.H = H
    self.color = True
    self.s = []
    for y in range(H):
      self.s += [[]]
      for x in range(W):
        self.s[y] += [[-2, 0, 0, u'']] # -2 = not known
    self.X = 0
    self.Y = 0
    self.cur(0,0)
    self.msg = ''
  def cur(self, x, y):
    X = self.X + x
    Y = self.Y + y
    if X<0 or X>=self.W or Y<0 or Y>=self.H:
      return
    self.s[self.Y][self.X][3] = u''
    self.X += x
    self.Y += y
    self.s[self.Y][self.X][3] = self.cursor
  def key(self, k):
    zero = ord('0')
    if k == 'w':
      self.cur(0, -1)
    elif k == 's':
      self.cur(0, 1)
    elif k == 'a':
      self.cur(-1, 0)
    elif k == 'd':
      self.cur(1, 0)
    elif k == 'c':
      exit()
    elif ord(k) >= zero and ord(k) < zero+9:
      self.set(self.X, self.Y, ord(k)-zero)
    elif ord(k) == zero+9:
      self.set(self.X, self.Y, -2)
  def add(self, x, y, s):
    self.s[y][x] = [s, 0, 0, self.s[y][x][3]]
  def view(self, clr=True):
    if clr:
        print('\033[2J') # clear screen
    for y in self.s:
      for x in y:
        c = x
        if x[0] == -2:
          x = [u'\u001b[37m.']
        elif x[0] == -1:
          x = ['#']
        elif x[0] == 0:
          x = [' ']
        elif x[0] == -3:
          x = [u'\u001b[91mX']
        elif x[0] == -4:
          x = [u'\u001b[92m@']
        if self.color and len(c)>=4:
          print(c[3], end='')
        print(x[0], end='')
        if self.color:
          print(u'\u001b[0m',end='')
      print()
    if self.msg:
      print(self.msg)
      self.msg = ''
  def good(self):
    for y in range(self.H):
      for x in range(self.W):
        a = self.get(x,y)[0]
        if a < 0:
          continue
        b = 0
        for p in range(1, 10):
          if self.get(x,y,p)[0] == -3:
            b += 1
        if a != b:
          return False
    return True
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
    self.s[y][x] = [z, 0, 0, u'']
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
          a = self.get(x, y)
          if a[0]-bs > nk:
            print('WARN: impossible (x', x, ' y', y, ' a', a, ')', sep='')
          elif a[0]-bs == nk:
            for p in range(1,10):
              if p == 5:
                continue
              c = self.get(x, y, p)
              if c[0] == -2:
                self.set(x, y, -3, p)
                b += 1
          elif a[0] == bs:
            for p in range(1,10):
              if p == 5:
                continue
              c = self.get(x, y, p)
              if c[0] == -2:
                self.set(x, y, -4, p) # -4 = clear
      ob = b
    for y in range(self.H):
      for x in range(self.W):
        if self.get(x,y)[0] == -4:
          return
    rnd = []
    for y in range(self.H):
      for x in range(self.W):
        if self.get(x,y)[0] == -2:
          tb = True
          for p in range(1,10):
           if self.get(x,y,p)[0] > -1:
             tb = False
          if tb:
            continue
          rnd += [(x,y)]
    if not rnd:
      return
    jj = [0]*len(rnd)
    overflow = len(rnd) < 15
    n = len(rnd) if overflow else 14
    for i in range(2**n):
    if i%len(rnd) == 0:
        print(u'\u001b[1000D',n,' ',100*i/2**len(rnd), '%',sep='', end='              ')
    i = random.randrange(2**len(rnd)) if overflow else i
    m = Minesweeper_solver(self.W, self.H)
    m.s = deepcopy(self.s)
    ij = []
    for j in rnd:
        ii = i%2
        i //= 2
        ij += [ii]
    for j, e in enumerate(rnd):
        if ij[j]:
        m.set(e[0],e[1],-3)
    # m.view(False)
    # print(ij, m.good())
    if m.good():
        for j in range(len(rnd)):
        jj[j] += ij[j]
    # print(rnd)
    # print(jj)
    # input()
    rndc = rnd[jj.index(min(jj))]
    # rndc = random.choice(rnd)
    self.set(rndc[0],rndc[1],-4)
    if max(jj) == 0:
      self.msg = '0/0 0%'
    else:
      self.msg = str(min(jj)) + '/' + str(max(jj)) + ' ' + str(int(1000*min(jj)/max(jj))/10) + '%'


def inp(s,l=True):
  m = True
  while m or l:
    x = input()
    x = x.split()
    for i, e in enumerate(x):
      x[i] = int(e)
    while x:
      s.add(x[0],x[1],x[2])
      x = x[3:]
    m = False

def inInt(msg):
  return int(input(msg))

if __name__ == '__main__':
  s = Minesweeper_solver(inInt('WIDTH: '), inInt('HEIGHT: '))
  while 1:
    s.update()
    s.view()
    s.key(getch.getch())
