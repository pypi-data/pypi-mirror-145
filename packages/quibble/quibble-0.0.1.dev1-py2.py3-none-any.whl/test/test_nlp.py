import numpy as np

from quibble import NonLinearProgramming


def test_basic_nlp():
    nlp = NonLinearProgramming(verbose=True)

    x_1 = nlp.add_decision_variable('x_1', lower_bound=-10, upper_bound=10)
    x_2 = nlp.add_decision_variable('x_2', lower_bound=-10, upper_bound=10)
    x_3 = nlp.add_decision_variable('x_3', lower_bound=-1, upper_bound=1)

    nlp.add_constraint(x_1 * x_2 ** 3 - np.sin(x_3 - x_2 / 2), lower_bound=-2, upper_bound=2.5)
    nlp.add_constraint(abs(x_1 + x_2 + x_3), lower_bound=-1, upper_bound=1)

    nlp.add_objective(x_1 + x_2 + x_3)

    res = nlp.solve(trials=1)
