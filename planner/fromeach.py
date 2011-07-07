#
# fromeach.py
#
# Copied from http://blog.jarrodmillman.com/2010/10/whats-best-way-to-interleave-two-python.html
#

from itertools import cycle,imap

def fromeach(*iters):
    """Take elements one at a time from each iterable, cycling them
    all.

    It returns a single iterable that stops whenever any of its
    arguments is exhausted.

    Note: it differs from roundrobin in the itertools recipes, in that
    roundrobin continues until all of its arguments are exhausted (for
    this reason roundrobin also needs more complex logic and thus has
    more overhead).
    
    Examples:
    
    >>> list(fromeach([1,2],[3,4]))
    [1, 3, 2, 4]
    >>> list(fromeach('ABC', 'D', 'EF'))
    ['A', 'D', 'E', 'B']
    """
    return (x.next() for x in cycle(imap(iter,iters)))
