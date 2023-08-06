import numpy as np
import os
from time import perf_counter as tpc


from fpcross import EquationOUP
from fpcross import FPCross


def run():
    print(f'>>>>>  OUP-3D')
    t = tpc()
    eq = EquationOUP(d=3)
    eq.set_coef_rhs(np.array([
        [1.5, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.5, 0.3, 1.0],
    ]))
    eq.set_cross_opts(
        # with_cache=True
    )
    eq.init()
    fpc = FPCross(eq)
    fpc.solve()
    print(f'-----  Solved > Time : {tpc()-t:-8.4f} sec\n\n')


if __name__ == '__main__':
    run()
