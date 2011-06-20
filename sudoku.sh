#!/usr/bin/env bash

# 
#  sudoku.sh
#  Sudoku solver usign sudoku2sat.py and minisat.
#  
#  Created by Libor Wagner on 2011-04-27.
#  Copyright 2011 Libor Wagner. All rights reserved.
# 


TMPDIR=`mktemp -d /tmp/sudoku.XXXXX`
INFILE="$TMPDIR/sudoku.txt"
CNFFILE="$TMPDIR/sudoku.cnf"
SATFILE="$TMPDIR/sudoku.result"

cat >$INFILE <<EOF
2 - 7 1 - 8 - 4 -
5 - - 2 - - - 1 7
- 6 - - 7 4 - - -
- - 8 - - 2 - 3 -
4 - 9 - 1 - 5 - 8
- 3 - 9 - - 4 - -
- - - 6 3 - - 2 -
8 7 - - - 9 - - 3
- 4 - 8 - 1 7 - 6
EOF

python sudoku2sat.py -b 9 -p $INFILE >$CNFFILE
minisat $CNFFILE $SATFILE
python sudoku2sat.py -b 9 -r $SATFILE

# Clean up
rm -r "$TMPDIR"
