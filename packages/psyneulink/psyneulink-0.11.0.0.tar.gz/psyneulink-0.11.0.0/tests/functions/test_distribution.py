import numpy as np
import pytest

import psyneulink.core.llvm as pnlvm
import psyneulink.core.components.functions.nonstateful.distributionfunctions as Functions
from psyneulink.core.globals.utilities import _SeededPhilox

np.random.seed(0)
test_var = np.random.rand()

RAND1 = np.random.rand()
RAND2 = np.random.rand()
RAND3 = np.random.rand()
RAND4 = np.random.rand()
RAND5 = np.random.rand()

test_data = [
    (Functions.DriftDiffusionAnalytical, test_var, {}, None,
     (1.9774974807292212, 0.012242689689501842, 1.9774974807292207, 1.3147677945132479, 1.7929299891370192, 1.9774974807292207, 1.3147677945132479, 1.7929299891370192)),
    (Functions.DriftDiffusionAnalytical, test_var, {"drift_rate": RAND1, "threshold": RAND2, "starting_value": RAND3, "non_decision_time":RAND4, "noise": RAND5}, None,
     (0.4236547993389047, -2.7755575615628914e-17, 0.5173675420165031, 0.06942854144616283, 6.302631815990666, 1.4934079600147951, 0.4288991185241868, 1.7740760781361433)),
    (Functions.DriftDiffusionAnalytical, -test_var, {"drift_rate": RAND1, "threshold": RAND2, "starting_value": RAND3, "non_decision_time":RAND4, "noise": RAND5}, None,
     (0.42365479933890504, 0.0, 0.5173675420165031, 0.06942854144616283, 6.302631815990666, 1.4934079600147951, 0.4288991185241868, 1.7740760781361433)),
#    FIXME: Rounding errors result in different behaviour on different platforms
#    (Functions.DriftDiffusionAnalytical, 1e-4, {"drift_rate": 1e-5, "threshold": RAND2, "starting_value": RAND3, "non_decision_time":RAND4, "noise": RAND5}, "Rounding errors",
#     (0.5828813465336954, 0.04801236718458773, 0.532471083815943, 0.09633801362499317, 6.111833139205608, 1.5821207676710864, 0.5392724012504414, 1.8065252817609618)),
    # Two tests with different inputs to show that input is ignored.
    (Functions.NormalDist, 1e14, {"mean": RAND1, "standard_deviation": RAND2}, None, (1.0890232855122397)),
    (Functions.NormalDist, 1e-4, {"mean": RAND1, "standard_deviation": RAND2}, None, (1.0890232855122397)),
    (Functions.UniformDist, 1e14, {"low": min(RAND1, RAND2), "high": max(RAND1, RAND2)}, None, (0.6879771504250405)),
    (Functions.UniformDist, 1e-4, {"low": min(RAND1, RAND2), "high": max(RAND1, RAND2)}, None, (0.6879771504250405)),
    # Inf inputs select Philox PRNG, test_var should never be inf
    (Functions.NormalDist, np.inf, {"mean": RAND1, "standard_deviation": RAND2}, None, (0.5910357654927911)),
    (Functions.NormalDist, -np.inf, {"mean": RAND1, "standard_deviation": RAND2}, None, (0.5910357654927911)),
    (Functions.UniformDist, np.inf, {"low": min(RAND1, RAND2), "high": max(RAND1, RAND2)}, None, (0.6043448764869507)),
    (Functions.UniformDist, -np.inf, {"low": min(RAND1, RAND2), "high": max(RAND1, RAND2)}, None, (0.6043448764869507)),
]

# use list, naming function produces ugly names
names = [
    "DriftDiffusionAnalytical-DefaultParameters",
    "DriftDiffusionAnalytical-RandomParameters",
    "DriftDiffusionAnalytical-NegInput",
#    "DriftDiffusionAnalytical-SmallDriftRate",
    "NormalDist1",
    "NormalDist2",
    "UniformDist1",
    "UniformDist2",
    "NormalDist1 Philox",
    "NormalDist2 Philox",
    "UniformDist1 Philox",
    "UniformDist2 Philox",
]


@pytest.mark.function
@pytest.mark.transfer_function
@pytest.mark.benchmark
@pytest.mark.parametrize("func, variable, params, llvm_skip, expected", test_data, ids=names)
def test_execute(func, variable, params, llvm_skip, expected, benchmark, func_mode):
    benchmark.group = "TransferFunction " + func.componentName
    if func_mode != 'Python' and llvm_skip:
        pytest.skip(llvm_skip)

    f = func(default_variable=variable, **params)
    if np.isinf(variable):
        f.parameters.random_state.set(_SeededPhilox([0]))

    ex = pytest.helpers.get_func_execution(f, func_mode)
    res = ex(variable)

    assert np.allclose(res, expected)
    if benchmark.enabled:
        benchmark(ex, variable)
