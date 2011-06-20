#!/usr/bin/env python
# encoding: utf-8
"""
sudoku2sat.py

Sudoku to sat converter, the input proble is specified in input file:

# Comment (Sudoku 4x4)
- - - -
1 2 - -
3 4 2 1

Created by Libor Wagner on 2011-04-21.
Copyright (c) 2011. All rights reserved.


"""

import sys
import getopt
import fileinput
from math import sqrt


help_message = '''[options]

Options:
    -h --help           This help
    -b --board X        Size of board
    -d                  Debug
    -p --problem file   Problem to be converted to sat.
    -r --result file    File containing results
'''

BOARD = 9
BLOCK = int(sqrt(BOARD))
DEBUG = False

def sign(i):
    if i >= 0:
        return 1
    if i < 0:
        return -1

def tuple2index(tp):
    """Converts tuple (var, x, y, val, neg) to running index."""
    var, x, y, val, neg = tp
    if var == 'x':
        index = neg*(x + BOARD*(y + BOARD*(val)) + 1)
    if var == 'y':
        index = neg*(x + BOARD*(y + BOARD*(val + BOARD)) + 1)
    return index
    
def tuple2str(tp):
    """Converts tupe (var, x, y, val, neg) to string."""
    var, x, y, val, neg = tp
    if neg == -1:
        return '~{0}{1}{2}{3}'.format(var, x+1, y+1, val+1)
    else:
        return '{0}{1}{2}{3}'.format(var, x+1, y+1, val+1)
        
def index2tuple(index):
    """Convert running index to tuple."""
    neg = sign(index)
    index = (neg * index) - 1
    x = 0
    y = 0
    val = 0
    var = 0
    
    while index - (BOARD**3) >= 0:
        var = var + 1
        index = index - (BOARD**3)
    
    while index - (BOARD**2) >= 0:
        val = val + 1
        index = index - (BOARD**2)
    
    while index - (BOARD) >= 0:
        y = y + 1
        index = index - (BOARD)
    
    x = index

    if var == 0:
        return ('x', x, y, val, neg)
    if var == 1:
        return ('y', x, y, val, neg)
        

def gencell(x,y):
    """Generate formulas for each cell."""
    # (y1 v y2 v ... v y9)
    formula = [0]*BOARD
    for val in range(BOARD):
        formula[val] = ('y', x, y, val, 1)
    print_formula(formula)
    
    # y <= (x1 & x2 ... x9)
    formula = [0]*BOARD
    for valy in range(BOARD):
        for val in range(BOARD):
            if val == valy:
                formula[val] = ('x', x, y, val, -1)
            else:
                formula[val] = ('x', x, y, val, 1)
        print_formula([('y',x,y,valy,1)] + formula)
    
    # y => (x1 & x2 ... x9)
    for valy in range(BOARD):
        for valx in range(BOARD):
            if valx == valy:
                print_formula([('y', x, y, valy, -1), ('x', x, y, valx, 1)])
            else:
                print_formula([('y', x, y, valy, -1), ('x', x, y, valx, -1)])

def genrow(y):
    """Generate formula for row."""
    formula = [0]*BOARD
    for val in range(BOARD):
        for x in range(BOARD):
            formula[x] = ('x', x, y, val, 1)
        print_formula(formula)

def gencol(x):
    """Generate formulas for column."""
    formula = [0]*BOARD
    for val in range(BOARD):
        for y in range(BOARD):
            formula[y] = ('x', x, y, val, 1)
        print_formula(formula)

def genblock(bx, by):
    """Generate formulas for each block."""
    for val in range(BOARD):
        formula = []
        for x in range(BLOCK):
            for y in range(BLOCK):
                formula.append(('x', BLOCK*bx + x, BLOCK*by + y, val, 1))
        print_formula(formula)

CNT = 0
def print_formula(formula):
    """Print formula"""
    global CNT
    CNT = CNT + 1
    if DEBUG:
        print str(CNT) + ': ' + ' | '.join(tuple2str(x) for x in formula)
    else:
        print ' '.join(str(tuple2index(x)) for x in formula) + ' 0'

def prefix_filter(generator, prefix='#'):
    """Prefix filter for string generator functions."""
    l = len(prefix)
    for s in generator:
        if s[-1] == '\n':
            s = s[:-1]
        if len(s) > 0 and (not s[:l] == prefix):
            yield s

def geninput(filename):
    """Generate input problem"""
    x = 0
    for line in prefix_filter(fileinput.input(filename), '#'):
        row = line.split(' ')
        if not len(row) == BOARD:
            raise Usage("Wrong input size!" + line)
        for y in range(BOARD):
            if not row[y] == '-':
                print_formula( [('x', x, y, int(row[y])-1, 1)] )
        x = x + 1
        if x > BOARD:
            raise Usage("Wrong input size!" + line)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def new_list(xmax,ymax):
    """Create 2D list."""
    l = [0]*xmax
    for i in range(xmax):
        l[i] = [0]*ymax
    return l

def main(argv=None):
    global BOARD
    global DEBUG
    global BLOCK
    
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hb:dp:r:", ["help", "board", \
                        "debug", "problem", "result"])
        except getopt.error, msg:
            raise Usage(msg)
        
        # option processing
        for option, value in opts:
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-b", "--board"):
                BOARD = int(value)
                BLOCK = int(sqrt(BOARD))
            if option in ("-d", "--debug"):
                DEBUG = True
            if option in ("-p", "--poblem"):
                print "c Sudoku {0}x{0}".format(BOARD)
                print "p cnf {0} {1}".format(BOARD**3*2, \
                    (1+BOARD+BOARD**2)*BOARD**2 + 3*BOARD**2)

                for x in range(BOARD):
                    for y in range(BOARD):
                        gencell(x,y)
                for y in range(BOARD):
                    genrow(y)
                for x in range(BOARD):
                    gencol(x)
                for x in range(BLOCK):
                    for y in range(BLOCK):
                        genblock(x,y)
                geninput(value)
            if option in ("-r", "--result"):
                sudoku = new_list(BOARD, BOARD)
                for line in prefix_filter(fileinput.input(value), 'SAT'):
                    indexes = line.split(' ')
                    for index in indexes:
                        if not index == '0':
                            var, x, y, val, neg = index2tuple(int(index))
                            if DEBUG:
                                print_formula([(var, x, y, val, neg)])
                            if var == 'x' and neg == 1:
                                sudoku[x][y] = val + 1
                for x in range(BOARD):
                    for y in range(BOARD):
                        print sudoku[x][y],
                    print
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())



