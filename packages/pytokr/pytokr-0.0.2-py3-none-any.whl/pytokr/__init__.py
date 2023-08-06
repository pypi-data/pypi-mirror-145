"""
Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528, balqui at GitHub
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
Start date: Germinal 2022.

This source: version 0.0.2.

Very simple tokenizer for stdin and similar objects. Finds items
(simple tokens white-space separated) in a string-based iterable
such as stdin (default). Ends of line are counted as white space 
but are otherwise ignored. 

Provides: 
- item() that obtains the next item and 
- iterator items() on which one can run a for loop to traverse 
all the items.
 
Both combine naturally: item() can be called inside the for
loop and this advances the items; so the next item at the loop 
will be the current one after the local advances.

Token items are returned as strings; user should cast them as
int or float or whatever when appropriate.

Programmed using lexical closure strategy.

Usage: for reading in items from stdin, just import item and/or
items; for usage on another string-based iterable, import and
call make_tokr.
"""


def make_tokr(f = None):
    "make iterator and next functions out of iterable of split strings"

    from itertools import chain

    def sp(ln):
        "to split the strings with a map"
        return ln.split()

    def the_it():
        "so that both, items and item, are called with parentheses"
        return it

    if f is None:
        from sys import stdin as f
    it = chain.from_iterable(map(sp, f))
    return the_it, it.__next__


items, item = make_tokr()

if __name__ == "__main__":
    "example usages"
    print("Please write some lines and end with a line containing only control-D:")
    print("First word of first line was:", item()) 
    print("Then comes the rest of the lines.")
    for w in items():
        "traverse rest of stdin"
        print(w)
    print("\n\nNow with another iterable made of splittable strings,")
    g = [ "10 11 12", "13 14", "15 16 17 18" ]
    print("namely:", g)
    items, item = make_tokr(g) # new variant to traverse g
    for w in items():
        "see how we can mix them up"
        print("\nCurrent value of w at for w in items() loop:", w)
        print("item() grabbed within the loop:", item())
        print("another item() grabbed also within the loop:", item())
