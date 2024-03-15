import ast
import typing
from checkpy import *

only("tunnel.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

def validate_sim(actual, expected):
    rl, vl, tl = actual
    assert len(rl) == len(vl) == len(tl), "Function is expected to return three lists of the same length."
    assert 0 < len(rl), "Each returned list must contain at least one element."

    min_height, max_height, min_speed, max_speed = expected
    _min_height, _max_height, _min_speed, _max_speed = min(rl), max(rl), min(vl), max(vl)

    tol = max_height // 1000
    assert approx(min_height, abs=tol) == _min_height,\
        f"Incorrect minimum distance (got {_min_height}, expected approximately {min_height})"

    assert approx(max_height, abs=tol) == _max_height,\
        f"Incorrect maximum distance (got {_max_height}, expected approximately {max_height})"

    assert approx(min_speed, abs=2) ==_min_speed,\
        f"Incorrect minimum speed (got {_min_speed}, expected approximately {min_speed})"

    assert approx(max_speed, abs=2) == _max_speed,\
        f"Incorrect maximum speed (got {_max_speed}, expected approximately {max_speed})"


def restrict(state: declarative.FunctionState):
    assert ast.Break not in static.AbstractSyntaxTree(state.fileName)

simulate_ultimate_free_fall = (
    declarative.function("simulate_ultimate_free_fall")
    .do(restrict)
    .params('r_start', 'dt')
    .returnType(typing.Tuple[typing.List[float], typing.List[float], typing.List[float]])
)

testDef = test()(simulate_ultimate_free_fall)

@passed(testDef, timeout=90, hide=False)
def testTunnel1():
    """Correct speeds and distances starting at height 6.38e6."""
    state = simulate_ultimate_free_fall.call(6.38e6, 0.01)()
    validate_sim(state.returned, (-6380124.4, 6380249, -7925, 7925.2))

@passed(testTunnel1, timeout=90, hide=False)
def testTunnel2():
    """Correct simulation length."""
    state = simulate_ultimate_free_fall.call(6.38e6, 0.01)()

    timeList = state.returned[2]
    if timeList[-1] != approx(5058.3, abs=4):
        raise AssertionError(
            f"Did not expect the time of the simulated free fall to be {timeList[-1]} seconds."
        )

@passed(testDef, timeout=90, hide=False)
def tustTunnel3():
    """Correct speeds and distances starting at height 3474"""
    state = simulate_ultimate_free_fall.call(3474, 0.01)()
    validate_sim(state.returned, (-3474, 3474, -4.315, 4.315))

@test()
def showsGraph():
    """Either saves a graph into a file, or shows a graph on the screen."""
    methods = [x.split(".")[-1] for x in static.getFunctionCalls()]
    assert "savefig" in methods or "show" in methods
