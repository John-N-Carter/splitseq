#!python3.10
"""Module to work with fnmatch: Filename matching with shell patterns returning matched and nonmatched.
Inspired by very simole patern matching, where constructing a regular expression is over kill
Uses fnmatch to compile glob pattern. Can post a raw re if mad enough.

b_split(NAMES: list[str], PATTERN: str, RESULTS: tupple[bool, bool], is_re: bool, ignore_case: bool) -> tupple[matched: list[str], notmatched: list[str]].
b_filter(NAMES: list[str], PATTERN: str, is_re: bool, ignore_case: bool) -> matched: list[str].
n_split(NAMES: list[], PRED, KEYS: list[] =  -> matched:dict[KEYS, list[]]

NAMES - list of strings, usually file names.
PATTERN - unix shell patern
PRED - function called on each element of NAMES returning the key.
KEYS - list of keys for predefinition or None.
RESULTS - tuple indicating which matched sewuences shoul be returned.
    True, (True, ) , (True, None) returns the match and an empty list.
    (True, False) returns the list split into matched and unmatched, etc.

Notes.
Python 3.10 Pattrn matching is used to give a rich set of returned posibilities.
_filter, _ifilter and _split do the work. based on fnmatch.filter with case normalization removed and logic modified.
Accumulating the unmatched in the inner loop is only a few percent slower than a single match.
It is faster without doing normalization to uppercas and back slash
"""
#~ import fnmatch as fn
from fnmatch import translate, fnmatch, fnmatchcase
from fnmatch import filter as fnfilter
import re

__all__ = ["b_split", "b_filter", "n_split"]

def _filter(names, pattern_match):
    """Return the subset of the list NAMES that match compiled re PAT."""
    result = []
    for name in names:
        if  pattern_match((name)):
            result.append(name)
    return result

def _ifilter(names, pattern_match):
    """Return the subset of the list NAMES that dont match compiled re PAT."""
    result = []
    for name in names:
        if not pattern_match((name)):
            result.append(name)
    return result

def _split(names, pattern_match):
    """
    Return the subset of the list NAMES that match compiled re PAT.
    Also returns those names that do not match PAT
    """
    result = []
    notresult = []
    for name in names:
        if not pattern_match((name)):
            result.append(name)
        else:
            notresult.append(name)
    return result, notresult

def _compile_pattern(pat, flags): # Code moved here to allow passing flags to re.compile
    if isinstance(pat, bytes):
        pat_str = str(pat, 'ISO-8859-1')
        res_str = translate(pat_str)
        res = bytes(res_str, 'ISO-8859-1')
    else:
        res = translate(pat)
    return re.compile(res, flags).match

def b_filter(names, pat,  is_re: bool = False, ignore_case: bool = False):
    """Return the subset of the list NAMES that match PAT.
        IS_RE indicates that PAT is a regular expression, the default is a glob style pattern.
        IGNORE_CASE indicates that should be case insensitive.
    """
    result = []
    reflags = re.IGNORECASE if ignore_case else 0
    pattern_match = re.compile(pat, reflags).match if is_re else _compile_pattern(pat, reflags)
    for name in names:
        if pattern_match(name):
            result.append(name)
    return result


def b_split(names: list[str], pat: str, test: bool = True, is_re: bool = False, ignore_case: bool = False):
    """
    Returns both subsets of NAMES that match and dont match PAT.
    TEST controls exactly what is matched and how it is returned.
    IS_RE indicates that PAT is a regular expression, the default is a glob style pattern
    IGNORE_CASE indicates that should be case insensitive
    """
    reflags = re.IGNORECASE if ignore_case else 0
    pattern_match = re.compile(pat, reflags).match if is_re else _compile_pattern(pat, reflags)
    match test:
        case (True, None) | (None, True) | (True, True) | (True,) | True:
            return _filter(names, pattern_match), []
        case (False, None) | (None, False) | (False, False) | (False,) | False | None:
            return [], _ifilter(names, pattern_match)
        case (False, True):
            t, f = _split(names, pattern_match)
            return t, f
        case (True, False):
            t, f = _split(names, pattern_match)
            return f, t
        case _:
            raise Exception('Target result not understood')
            print('bad')

def n_split(seq, pred, keys = []):
    """ n_seq: splits list into partitions controled by 'pred', option to pre-specy the keys."""
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


if __name__ == '__main__': # testing and performance
    import sys, timeit, glob, random, os, string
    base = string.ascii_letters + string.digits + '._-'
    random.seed(123457)
    names = []
    testnames = 100
    for i in range(testnames):
        names.append(''.join(random.choices(base, k = 10)))

    a, b = split(names, '*3*', test = [True, False])
    print('Testing "split"')
    print('Test Sequence', names[:5])
    print('Search for "3" in string')
    print('True', a[:5])
    print('False', b[:5])



