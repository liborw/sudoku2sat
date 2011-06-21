`sudoku2sat.py` is simple python script to convert [Sudoku][sudoku] to [Boolean satisfiability problem][sat] the scripts reads sudoku table in specific format and converts int to boolean formulas in format used by SAT solvers, it can also read output of SAT solver and output solved sudoku. I used [minisat][minisat] SAT solver.

### Input format example

    # Comment
    9 - 5 - - - - - 8
    4 - - 5 7 - 1 - 6
    - 2 7 6 - - - 4 -
    - 9 6 - - 3 5 1 2
    7 - 4 - 1 - 3 - -
    2 1 - 9 8 - - - 4
    - 8 1 - - 4 - 9 -
    3 - - 8 - - - 5 1
    - - 2 - - 7 - 6 -
    # Comment

### Usage

    $ sudoku2sat.py -h
    sudoku2sat.py: [options]

    Options:
        -h --help           This help
        -b --board X        Size of board
        -d                  Debug
        -p --problem file   Problem to be converted to sat.
        -r --result file    File containing results

### Acknowledgement
This project is part of the [A4M33AU: Automatic Reasoning][a4m33au] course on [Faculty of Electrical Engineering][fee].

[fee]: http://www.fel.cvut.cz
[a4m33au]: https://cw.felk.cvut.cz/doku.php/courses/a4m33au/
[sat]: http://en.wikipedia.org/wiki/Boolean_satisfiability_problem
[sudoku]: http://en.wikipedia.org/wiki/Sudoku
[minisat]: http://minisat.se/
[sat_input]: 