#!python3.10
#~ import fnmatch as fn
from fnmatch import translate, fnmatch, fnmatchcase
from fnmatch import filter as fnfilter
import re
from splitseq import *

if __name__ == '__main__': # testing and performance
    import sys, timeit, glob, random, os, string
    from enum import Enum, auto
    import wcmatch.fnmatch as wc
    from time import process_time as time
    from more_itertools import partition
    from itertools import tee, filterfalse
    from more_itertools import bucket

    from collections import UserDict
    from boltons import dictutils
    #~ import split as ssplit

    import dictoflists

    def funcTimer(func):
        """This function returns the execution time of the function object passed."""
        def wrap_func(*args, **kwargs):
            t1 = time()
            result = func(*args, **kwargs)
            t2 = time()
            return t2 - t1, result
        return wrap_func

    class Test(Enum):
        Null = auto()
        Split = auto()
        Positive = auto()
        Negative = auto()
        UpperCase = auto()
        WCmatch = auto()
        IWCmatch = auto()
        Easy = auto()

        FNmatch = auto()

        Re = auto()
        Bucket = auto()
        DOL = auto()
        DOD = auto()
        DODX = auto()

        Both = auto()
        IBoth = auto()
        Partition = auto()
        MRAB = auto()
        METZ = auto()
        CA = auto()
        CAPmess = auto()
        SJB = auto()
        ITPartition = auto()
        OMD1 = auto()
        Basic = auto()
        Basic4 = auto()
        OMD2 = auto()
        Basic2 = auto()
        Basic3 = auto()
        DODX2 = auto()
        DOD2 = auto()
        DOL2 = auto()
        Bucket2 = auto()
        FSEQ = auto()
        FSEQ2 = auto()
        Remove = auto()
        Comp = auto()
        FT1 = auto()
        FT2 = auto()
        FT3 = auto()
        FT4 = auto()
        FT5 = auto()
        FT6 = auto()
        FT7 = auto()
        FT8 = auto()
        FT9 = auto()
        FT10 = auto()
        FT11 = auto()
        FT12 = auto()

    def CApartition(pred, iter):
        results = [], []
        for thing in iter:
            results[not pred(thing)].append(thing)
        return results

    def itrpartition(pred, iterable):
        "Use a predicate to partition entries into false entries and true entries"
        # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
        t1, t2 = tee(iterable)
        ipred = lambda x: not pred(x)
        a, b =  filterfalse(pred, t1), filter(pred, t2)
        #~ print(type(a), type(b))
        return a, b

    def CApartition(pred, iter):
        results = [], []
        for thing in iter:
                results[ bool(pred(thing))].append(thing)
        return results

    def mess(s):
        if 'Z' in s:
            return s
        else:
            return ''

    def fseq(seq, pred, keys = []):
        """ fseq: splits list into partitions controled by 'pred', option to pre-specy the keys."""
        """
        seq: List to split up
        pred: function returning keys.
        keys: Optional key valuues to initialise the result.
        returns a dictionary, indexed by key containg lists
        """
        out = {}
        if keys:
            for k in keys:
                out[k] = []
            for s in seq:
                out[pred(s)].append(s)
        else:
            for s in seq:
                k = pred(s)
                if k not in out:
                    out[k] = []
                out[k].append(s)
        return out

    @funcTimer
    def test(a: list[str], test: Test, n: int = 1):
        note = ''
        b = c = []
        s = 'Z'                         # single character used to generate patern, see later
        for ch in s:                    # Once through this loop as using remove is distructive and polutes the answer
            pat = F'*[{ch}]*'
            for i in range(n):          # Only once round test loop as spliting sequence using remove is destructive.
                match test: # patern matching used toparse test cases rather than if ,,. elif ... else .. chain
                    case Test.FSEQ:
                        note = 'Function with preset N classes'
                        b = []
                        c = []
                        pred = lambda x: x[0]
                        base = string.ascii_letters + string.digits + '._-'
                        e = fseq(a, pred, base)
                    case Test.FSEQ2:
                        note = 'Function with unknown N classes'
                        b = []
                        c = []
                        pred = lambda x: x[0]
                        base =None
                        e = fseq(a, pred, base)
                    case Test.Bucket:
                        note = 'Binary with Bucket Function'
                        res = translate(pat)
                        predx = re.compile(res).match
                        pred = lambda x: bool(predx(x))
                        s = bucket(a, key = pred)
                        b = list(s[True])
                        c = list(s[False])
                    case Test.Bucket2:
                        note = 'N classes with Bucket Function'
                        pred = lambda x: x[0]
                        s = bucket(a, key = pred)
                        b = []
                        c = []
                        e= {}
                        for k in list(s):
                            e[k] = list(s[k])
                    case Test.Split:
                        note = 'Binary: Using "split" module and iterables, cant make it work'
                        #~ res = translate(pat)
                        #~ predx = re.compile(res).match
                        #~ pred = lambda x: bool(predx(x))
                        #~ tt, tf = ssplit.partition(pred, a)
                        #~ b = list(tt)
                        #~ c = list(tf)
                        b = c = []
                    case Test.DOL:
                        note = 'Binary with Dictionary of lists'
                        res = translate(pat)
                        pred = re.compile(res).match
                        results = [bool(pred(x)) for x in a]
                        e =  dictoflists.DOL((i, j) for i, j in zip(results, a))
                        b = e[0]
                        c = e[1]
                    case Test.DOD:
                        note = 'Binary with Dictionary of Deque'
                        res = translate(pat)
                        pred = re.compile(res).match
                        results = [bool(pred(x)) for x in a]
                        e =  dictoflists.DOD((i, j) for i, j in zip(results, a))
                        b = e[0]
                        c = e[1]
                    case Test.DODX:
                        note = 'Binary, alternative Deque'
                        res = translate(pat)
                        predx = re.compile(res).match
                        pred = lambda x: bool(predx(x))
                        e = dictoflists.DOD( (pred(x), x) for x in a)
                        b = e[0]
                        c = e[1]
                    case Test.DODX2:
                        note = 'N Class, Deque and dict comprehension'
                        pred = lambda x: x[0]
                        e =  dictoflists.DOD((pred(x), x) for x in a)
                        b = []
                        c = []
                    case Test.DOD2:
                        note = 'N Class, Deque, precalculate clases'
                        pred = lambda x: x[0]
                        results = [pred(x) for x in a]
                        e =  dictoflists.DOD((i, j) for i, j in zip(results, a))
                        b = []
                        c = []
                    case Test.DOL2:
                        note  = 'N Class, dict of lists, precalculate clases'
                        pred = lambda x: x[0]
                        results = [pred(x) for x in a]
                        e =  dictoflists.DOL((i, j) for i, j in zip(results, a))
                        b = []
                        c = []
                    case Test.OMD1:
                        note = 'Binary, using "dictutils.OMD"'
                        res = translate(pat)
                        pred = re.compile(res).match
                        results = [bool(pred(x)) for x in a]
                        e =  dictutils.OMD((i, j) for i, j in zip(results, a))
                        b = e.getlist(0)
                        c = e.getlist(1)
                    case Test.OMD2:
                        note = 'N-Case, using "dictutils.OMD"'
                        pred =lambda x: x[0]
                        e =  dictutils.OMD((i, j) for i, j in zip([pred(x) for x in a], a))
                        b = e.getlist('x')
                        c = e.getlist('3')
                    case Test.CA:
                        note = 'Binary inspired by CA'
                        res = translate(pat)
                        pred = re.compile(res).match
                        b, c = CApartition(pred, a)
                    case Test.CAPmess:
                        note = 'Binary, inspired by CAP and simple character check'
                        res = translate(pat)
                        pred = re.compile(res).match
                        b, c = CApartition(mess, a)
                    case Test.Re:
                        note = 'Binary, testing split with re.'
                        b, c = split(a, F'.*{ch}.*', (True, False), is_re = True)
                    case Test.WCmatch: # Compares with the wcmatch module
                        note = 'True using "wcmatch"'
                        b = wc.filter(a, pat)
                        c = []
                    case Test.IWCmatch:
                        note =  'falce using invweted "wcmatch"'
                        pat = '!' + pat
                        c = wc.filter(a, pat)
                        b = []
                    case Test.FNmatch:
                        note = 'True only, using filter from "fnmatch"'
                        b = fnfilter(a, pat)
                        c = []
                    case Test.UpperCase:
                        note = 'True only, uppercase'
                        b, c = split(a, pat, True, False, True)
                    case Test.Positive:
                        note = 'Positve only'
                        b, c = split(a, pat, True)
                    case Test.Negative:
                        note = 'Negative only'
                        b, c = split(a, pat, (False, ))
                    case Test.Remove: # removes matches  from a shallowcopy.
                        note = 'Binary, via external filter, vey slow'
                        #~ b = filter(a, pat)
                        #~ c = a.copy()
                        #~ for b1 in b:
                            #~ c.remove(b1)
                    case Test.Comp: # list comprehension used to filter out matches. This is slow bt if nuner of cases is small (10's) is ok.
                        note = 'Binary using st comprehension used to filter out matches, slow.'
                        #~ b = filter(a, pat)
                        #~ c = [x for x in a if x not in b]
                    case Test.Both:
                        note = 'Binary using my split'
                        c, b = split(a, pat, (True, False))
                    case Test.IBoth:
                        note = 'Binary inverted'
                        c, b = split(a, pat, (False, True))
                    case Test.Null: # Legacy of early code testing
                        note = 'Legacy of early code testing'
                        b = []
                        c = []
                    case Test.Easy: # Simply checking test character exists in name (ss)
                        note = 'Binary, Simply checking test character exists in name (ss)'
                        b = []
                        c = []
                        for ss in a:
                            if ch in ss:
                                b.append(ss)
                            else:
                                c.append(ss)
                    case Test.Partition:
                        note = 'Binary using patition(using iterators) from "more_itertolls*'
                        res = translate(pat)
                        pred = re.compile(res).match
                        tname, fname = partition(pred, a)
                        #~ b = c = []
                        b = [x for x in tname]
                        c = [x for x in fname]
                    case Test.MRAB:
                        note = 'Binary inspired by MRAB'
                        b, c = split(a, pat, True)
                        s = set(b)
                        c = [x for x in a if x not in s]
                    case Test.METZ:
                        note = 'Binary inspired by METZ'
                        b, c = split(a, pat, True)
                        c = list(set(a) - set(b))
                    case Test.ITPartition:
                        note = 'Binary using functional tools'
                        res = translate(pat)
                        pred = re.compile(res).match
                        ti, fi = itrpartition(pred, a)
                        b = [x for x in ti]
                        c = [x for x in fi]
                    case Test.Basic2:
                        note = 'N clases, inline, precomputing dictionary entries'
                        base = string.ascii_letters + string.digits + '._-'
                        e = {}
                        b = []
                        c = []
                        for c in base:
                            e[c] = []
                        for s in a:
                            k = s[0]
                            e[k].append(s) # no check
                    case Test.Basic3:
                        note = 'N clases, inline, testing dictionary entries'
                        e = {}
                        b = []
                        c = []
                        for s in a:
                            k = s[0]
                            if k in e:
                                e[k].append(s)
                            else:
                                e[k] = [a]
                    case Test.Basic:
                        note = 'Binary, predefined clalses, re and inline'
                        e = {True: [], False: []}
                        res = translate(pat)
                        predx = re.compile(res).match
                        pred = lambda x: (predx(x))
                        for s in a:
                            k = predx(s)
                            if  k:
                                 e[True].append(s)
                            else:
                                e[False].append(s)
                        b = e[True]
                        c = e[False]
                    case Test.Basic4:
                        note = 'Binary, predefined clalses, direct check and inline'
                        e = {True: [], False: []}
                        for s in a:
                            if ch in s:
                                 e[True].append(s)
                            else:
                                e[False].append(s)
                        b = e[True]
                        c = e[False]
                    case Test.FT1:
                        note = 'Binary RE predicate'
                        res = translate(pat)
                        predx = re.compile(res).match
                        pred = lambda x: bool(predx(x))
                        e = fseq(a, pred)
                        b = e[True]
                        c = e[False]
                    case Test.FT2:
                        note = 'Binary RE predicate, predicted'
                        res = translate(pat)
                        predx = re.compile(res).match
                        pred = lambda x: bool(predx(x))
                        e = fseq(a, pred, keys = [True, False])
                        b = e[True]
                        c = e[False]
                    case Test.FT3:
                        note = 'Binary direct predicate, not predicted'
                        pred = lambda x: 'a' in x
                        e = fseq(a, pred)
                        b = e[True]
                        c = e[False]
                    case Test.FT4:
                        note = 'Binary direct predicate, predicted'
                        pred = lambda x: 'a' in x
                        e = fseq(a, pred, keys = [True, False])
                        b = e[True]
                        c = e[False]
                    case Test.FT6:
                        note = 'N Classes, predicted'
                        pred = lambda x: x[0]
                        base = string.ascii_letters + string.digits + '._-'
                        e = fseq(a, pred, keys = base)
                    case Test.FT5:
                        note = 'N Classes, not predicted'
                        pred = lambda x: x[0]
                        e = fseq(a, pred)
                    case Test.FT7:
                        note = 'Binary, predefined clalses, direct check and inline'
                        e = {True: [], False: []}
                        for s in a:
                            if ch in s:
                                 e[True].append(s)
                            else:
                                e[False].append(s)
                        b = e[True]
                        c = e[False]
                    case Test.FT8:
                        note = 'Binary, predefined clalses, direct check and inline'
                        e = {True: [], False: []}
                        for s in a:
                            if ch in s:
                                 e[True].append(s)
                            else:
                                e[False].append(s)
                        b = e[True]
                        c = e[False]
                    case Test.FT9:
                        note = 'Binary, predefined clalses, direct check and inline'
                        e = {True: [], False: []}
                        for s in a:
                            if ch in s:
                                 e[True].append(s)
                            else:
                                e[False].append(s)
                        b = e[True]
                        c = e[False]
                    case Test.FT10:
                        note = 'Binary, predefined clalses, direct check and inline'
                        e = {True: [], False: []}
                        for s in a:
                            if ch in s:
                                 e[True].append(s)
                            else:
                                e[False].append(s)
                        b = e[True]
                        c = e[False]
                    case Test.FT11:
                        note = 'Binary, predefined clalses, direct check and inline'
                        e = {True: [], False: []}
                        for s in a:
                            if ch in s:
                                 e[True].append(s)
                            else:
                                e[False].append(s)
                        b = e[True]
                        c = e[False]
                    case Test.FT12:
                        note = 'Binary, predefined clalses, direct check and inline'
                        e = {True: [], False: []}
                        for s in a:
                            if ch in s:
                                 e[True].append(s)
                            else:
                                e[False].append(s)
                        b = e[True]
                        c = e[False]
                        c = e[False]
                    case Test.SJB:
                        note = 'Binary inspired by SJB'
                        res = translate(pat)
                        pred = re.compile(res).match
                        b = []
                        c = []
                        for elem in a:
                            (b if pred(elem) else c).append(elem)
                    case _:
                        b = []
                        c= []
        return b, c, note

    output = 'loglin' # one of [bar, loglog, loglin, text]
    #~ testlist = Test
    testlist = [Test.FT1, Test.FT2, Test.FT3, Test.FT4,  Test.Easy, Test.CAPmess, Test.FT5, Test.FT6,
        Test.Basic2, Test.Basic3]
    match output:
        case 'bar':
            import matplotlib.pyplot as plt
            import numpy as np
            base = string.ascii_letters + string.digits + '._-'
            random.seed(123457)
            names = []
            limit = 10000000
            times = [10, 30,
                100, 300,
                1000, 3000,
                10000, 30000,
                100000, 300000,
                1000000]
            print('Check Times', times)
            labels = []
            for tc in testlist:
                labels.append(tc.name)
            allnames = []
            for i in range(times[-1]):
                allnames.append(''.join(random.choices(base, k = 10)))
            dup = times[-1] // 100
            for j in range(dup):
                i = random.randrange(dup)
                allnames[i] = allnames[j]
            nlabels = []
            y = []
            for i, tc in enumerate(testlist):
                for testnames in [10000]:
                    testnames = min(limit, testnames)
                    repeat = min(100, limit // testnames)
                    names = allnames[:testnames]
                    t, (r, s, note) = test(names, tc, repeat)
                    t = t / repeat
                    t =round( t * 1000., 1)
                    if t == 0.:
                        t = 30.
                    y.append(t)
                    print(tc, testnames, t)
                nlabels.append(note)
            width = 0.9 # the width of the bars
            fig, ax = plt.subplots()
            fig.set_figwidth(8)
            fig.set_figheight(9)
            x = np.arange(len(nlabels))  # the label locations
            rects1 = ax.bar(x - width/2, y, width, label='Time')
            ax.set_ylabel('Times')
            ax.set_title('Time (ms) per 10000')
            ax.set_xticks(x, nlabels, rotation = 'vertical')
            ax.legend()
            ax.bar_label(rects1, padding=3)
            fig.tight_layout()
            plt.show()

        case 'loglog' | 'loglin' as gtype:
            import matplotlib.pyplot as plt
            import numpy as np
            TestCase = Test.FNmatch
            base = string.ascii_letters + string.digits + '._-'
            random.seed(123457)
            names = []
            limit = 10000000
            times = [10, 30,
                100, 300,
                1000, 3000,
                10000, 30000,
                100000, 300000,
                1000000]
            print('Check Times', times)
            fig, ax = plt.subplots()
            ax.set_xscale("log", base=10)
            if gtype == 'loglog':
                ax.set_yscale("log", base = 10)
            elif gtype == 'loglin':
                ax.set_yscale("linear")
            else:
                raise Exception('Unknown graph request')
            ax.set_title('Time (ms)')
            ax.set_ylabel('Times')
            ax.set_xlabel('Number of enteries in list')
            allnames = []
            for i in range(times[-1]):
                allnames.append(''.join(random.choices(base, k = 10)))
            dup = times[-1] // 100
            for j in range(dup):
                i = random.randrange(dup)
                allnames[i] = allnames[j]
            for tc in testlist:
                y = []
                for testnames in times:
                    testnames = min(limit, testnames)
                    repeat = min(1000, limit // testnames)
                    names = allnames[:testnames]
                    t, (r, s, note) = test(names, tc, repeat)
                    t = t / repeat
                    #~ t = max(t, 1.56e-8)
                    y.append(t)
                    print(tc, testnames, t, repeat, len(names), limit)

                ax.plot(times, y, linewidth=1.0)
            plt.show()
        case 'text':
            TestCase = Test.FNmatch
            base = string.ascii_letters + string.digits + '._-'
            random.seed(123457)
            names = []
            limit = 1000000
            testnames = 1000000
            repeat = min(10, limit // testnames)
            for i in range(testnames):
                names.append(''.join(random.choices(base, k = 10)))
            fullnames = set(names)
            dup = testnames // 100
            for j in range(dup):
                i = random.randrange(dup)
                names[i] = names[j]
            res = translate('*Z*')
            pred = re.compile(res).match
            ref_b = []
            ref_c = []
            for el in names:
                if pred(el):
                    ref_b.append(el)
                else:
                    ref_c.append(el)
            def order(a, b):
                for e, f in zip(a, b):
                    if e != f:
                        return False
                return True
            print(F'Number of tests cases {len(names)} as set {len(fullnames)} as repeat is {repeat}')
            print(F'{dup} Duplicates as set {len(set(names))}')
            print(F'Reference lists { len(ref_b)}  {len(ref_c)}')
            print('Example data', names[0:5])
            print(F'{"Test":12s} {"Time":12s} {"True":8} {"False":8} {"Total":8} {"Correct ":8} {"   Note":20}')
            for tc in testlist:
                t, (r, s, note) = test(names, tc, repeat)
                print(F'{tc.name:12s} {t:12.6f} {len(r):8d} {len(s):8} {len(r) + len(s):8} {order(ref_b, r):8b} {note:20}')
        case _:
            print('No output')

