#!python3.10
import sys, timeit, glob, random, os, string
import collections
from collections import UserDict, deque


#~ class DictOfLists(UserDict):
class DictOfLists(UserDict):
    """Dictionary of lists, used to split sequences"""
    def __setitem__(self, key, item):
        """If key does not exist, set item to empty list"""
        if key in self.data:
            self.data[key].append(item)
        else:
            self.data[key] = [item]
    def __getitem__(self, key):
        """Return item, empty list if not there"""
        if key in self.data:
            return self.data[key]
        else:
            return [] # return empty list if not found

    def reset(self, key):
        """Reset key to empty list self.date[key] = []"""
        if key in self.data:
            self.data[key] = []

    def newkey(self, old, new):
        """Rename Key if exists, if new exists it is overwritten"""
        if old in self.data:
            item = self.data[old]
            del self.data[old]
            self.data[new] = item
        else:
            self.data[new] = []

class DictOfDeque(UserDict):
    """Dictionary of lists, used to split sequences"""
    def __setitem__(self, key, item):
        """If key does not exist, set item to empty list"""
        if key in self.data:
            self.data[key].append(item)
        else:
            self.data[key] = deque([item])
    def __getitem__(self, key):
        """Return item, empty list if not there"""
        if key in self.data:
            return self.data[key]
        else:
            return [] # return empty list if not found

    def reset(self, key):
        """Reset key to empty list self.date[key] = []"""
        if key in self.data:
            self.data[key] = []

    def newkey(self, old, new):
        """Rename Key if exists, if new exists it is overwritten"""
        if old in self.data:
            item = self.data[old]
            del self.data[old]
            self.data[new] = item
        else:
            self.data[new] = []


DOL = DictOfLists
DOD = DictOfDeque

if __name__ == '__main__':

    a = DOL()
    a[1] = 2
    a[1] = 2
    a[1] = 2
    a[3] = 7
    a[3] = 'fred'
    print('The dictionary',a)
    two = a[1].pop()
    print('The dictionary missing a 2 in 1',a, 'Two poped', two)
    a.newkey(1, 5)
    print('After 1 renamed to 5', a)
    a.newkey(4, 8)
    print('After 4 renamed to 8', a)
    a.newkey(5, 3)
    print('After 5 renamed to 3', a)
    print('Individual items', a[2], a[3])
    a.reset(3)
    print('3 reset', a)
    a[50] = 100
    print('50 inserted', a)
    a[50].clear()
    print('50 reset', a)
    a.clear()
    print('All Cleared', a)

    print('DEQUE')
    d = deque([1,2,3,4,5])
    print(d)
    print(len(d))
    for i in range(len(d)):
        print(d[i])

    a = DOD()
    a[1] = 2
    a[1] = 2
    a[1] = 2
    a[3] = 7
    a[3] = 'fred'
    print('The dictionary',a)
    two = a[1].pop()
    print('The dictionary missing a 2 in 1',a, 'Two poped', two)
    a.newkey(1, 5)
    print('After 1 renamed to 5', a)
    a.newkey(4, 8)
    print('After 4 renamed to 8', a)
    a.newkey(5, 3)
    print('After 5 renamed to 3', a)
    print('Individual items', a[2], a[3])
    a.reset(3)
    print('3 reset', a)
    a[50] = 100
    print('50 inserted', a)
    a[50].clear()
    print('50 reset', a)
    a.clear()
    print('All Cleared', a)
