"""Parse input data methods"""

import os
import sys


def parse(inpt=None):
    """
    Parse input
    returns list meta as below
    R – number of rows of the grid (1 ≤ R ≤ 10000)
    C – number of columns of the grid (1 ≤ C ≤ 10000)
    F – number of vehicles in the fleet (1 ≤ F ≤ 1000)
    N – number of rides (1 ≤ N ≤ 10000)
    B – per-ride bonus for starting the ride on time (1 ≤ B ≤ 10000)
    T – number of steps in the simulation (1 ≤ T ≤ 10 )

    returns list of ride tuples as below
    (a,b) (x,y) (s,f)
    a – the row of the start intersection (0 ≤ a < R)
    b – the column of the start intersection (0 ≤ b < C)
    
    x – the row of the finish intersection (0 ≤ x < R)
    y – the column of the finish intersection (0 ≤ y < C)
    
    s – the earliest start(0 ≤ s < T)
    f – the latest finish (0 ≤ f ≤ T) , (f ≥ s + |x − a| + |y − b|)
    """
    data = os.path.abspath(inpt or sys.argv[1])

    with open(data) as fp:
        meta = fp.readline().split()
        rides = []
        for l in fp.readlines():
            l = l.split()
            if len(l) >= 6:
                r = (l[0],l[1]), (l[2],l[3]), (l[4],l[5])
                rides.append(r)
    
    return meta, rides


if __name__ == "__main__":
    print(parse())
