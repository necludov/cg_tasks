import numpy as np
import matplotlib
import sys

def calc_basis_function(value, knots, power):
    p = 0
    cur_basis = map(lambda tup: 1. if tup[0] <= value and value < tup[1] else .0, zip(knots[:-1], knots[1:]))
    cur_basis = np.array(cur_basis)
    while p < power:
        p += 1
        n_basis = len(knots) - p - 1
        next_basis = np.zeros(n_basis)
        for i in range(n_basis):
            if (knots[i+p] - knots[i]) != 0:
                next_basis[i] = (value - knots[i]) / (knots[i+p] - knots[i]) * cur_basis[i]
            else:
                next_basis[i] = 0.0
            if (knots[i+p+1] - knots[i+1]) != 0:
                next_basis[i] += (knots[i+p+1] - value) / (knots[i+p+1] - knots[i+1]) * cur_basis[i+1]
        cur_basis = next_basis
    return cur_basis

if __name__ == "__main__":
    knots = sorted((np.random.random(30) * 10).round())
    power = 10
    if len(sys.argv) < 3:
        print "Undefined input"
        print "firstly give me a power"
        print "secondly give me an ascending values of knots"
        print "using knots", knots
        print "with power", power
    else:
        arrrgs = sys.argv
        power = int(arrrgs[1])
        knots = np.array(map(lambda s: int(s), arrrgs[2:]))

    support = np.linspace(min(knots), max(knots), num=1000)
    results = np.array(map(lambda v: calc_basis_function(v, knots, power), support)).T
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.subplot(2,1,1)
    for y in results:
        plt.plot(support, y)
    plt.title('basis functions')
    plt.show()
    plt.subplot(2,1,2)
    plt.title('sum of basis functions')
    plt.plot(support, results.sum(axis=0))
    plt.savefig('basis_funcs.ps')
    plt.show()
