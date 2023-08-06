import gurobipy as gp
from gurobipy import GRB
import numpy


def flux_variability_analysis(S, c: numpy.ndarray, v_min: numpy.ndarray, v_max: numpy.ndarray):
    r"""
    Finds the extent of the fluxes,v , at the optimal value between 2 bounds

    .. math::

        \begin{align}
        \max_{v}\quad\quad& c^Tv\\
        Sv &=0\\
        \underline{v} \leq v \leq \overline{v}
        \end{align}

    :return: The upper and lower bounds of the optimal values
    """

    # create the model
    m = gp.Model()

    # quite gurobi output
    m.Params.OutputFlag = 0

    # determine count to the fluxes
    metabolite_count = numpy.size(v_min)

    # create the variables
    v = m.addMVar((metabolite_count,), vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY)

    # build the model
    m.setObjective(c.flatten() @ v, GRB.MAXIMIZE)
    m.addConstr(S @ v == 0, name='network')
    m.addConstr(v <= v_max.flatten(), name='maxs')
    m.addConstr(v >= v_min.flatten(), name='mins')

    # solve the initial optimization problem
    m.optimize()

    # add the constraint that the fluxes stay on the primal degenerate plane
    max_value = m.getObjective().getValue()
    m.addConstr(c.flatten() @ v == max_value, 'Optimal Plane')

    fva_min = numpy.zeros(metabolite_count)
    fva_max = numpy.zeros(metabolite_count)

    # solve n lp to find max values
    for i in range(metabolite_count):
        # update the objective
        m.setObjective(v[i], GRB.MAXIMIZE)

        # re-optimize the model
        m.optimize()
        m.update()

        # store the new max flux value
        fva_max[i] = m.getObjective().getValue()

    # solve n lp to find min values
    for i in range(metabolite_count):
        # update the objective
        m.setObjective(v[i], GRB.MINIMIZE)

        # re-optimize the model
        m.optimize()
        m.update()

        # store the new min flux value
        fva_min[i] = m.getObjective().getValue()

    return fva_min, fva_max
