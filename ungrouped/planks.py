"""
Tasks:
Given an array:
[   [1, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1]
]
representing the following situation:
(where O is wooden planks, X means water)
|    0000X    |
|    XXX0X    |
|    X000X    |
|    X0XXX    |
|    X0000    |
Where a guy starting from the left side, walk on the wooden planks
to arrive at the right side.
You can say the wooden planks forms a bridge,
and in the above situation, the bridge is "passable", aka you can
walk from the left side to the right side via the bridge.

Write a function that receives an 2-dimensional array as input, return a boolean
value (True/False) indicating whether the bridge is "passable".

Using recursion is strongly recommended.
COMP2113 [2023 Sem2] Assignment 3 Q2
"""

example = [[1, 1, 1, 1, 0],
           [0, 0, 0, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 0, 0, 0],
           [0, 1, 1, 1, 1]
           ]


def passable(bridge: list[list]) -> bool:
    # define your own function parameters and code
    return False


assert passable(example) == True
