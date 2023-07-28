import ast
import typing
from checkpy import *

only("tunnel.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

def validate_sim1(actual, expected):
    rl, vl, tl = actual
    assert len(rl) == len(vl) == len(tl), "Function is expected to return three lists of the same length."
    assert len(rl) > 0, "Each returned list must contain at least one element."

    min_height, max_height, min_speed, max_speed = expected
    _min_height, _max_height, _min_speed, _max_speed = min(rl), max(rl), min(vl), max(vl)

    tol = max_height // 1000
    assert _min_height == approx(min_height, abs=tol),\
        f"Incorrect minimum distance (got {_min_height}, expected approximately {min_height})"

    assert _max_height == approx(max_height, abs=tol),\
        f"Incorrect maximum distance (got {_max_height}, expected approximately {max_height})"

    assert _min_speed == approx(min_speed, abs=2),\
        f"Incorrect minimum speed (got {_min_speed}, expected approximately {min_speed})"

    assert _max_speed == approx(max_speed, abs=2),\
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

testTunnel1 = passed(testDef, timeout=90, hide=False)(
    simulate_ultimate_free_fall
    .call(6.38e6, 0.01)
    .do(lambda state: validate_sim1(state.returned, (-6380124.4,  6380249, -7925, 7925.2)))
    .description("Correct speeds and distances starting at height 6.38e6.")
)

def assertCorrectTime(timeList):
    if timeList[-1] != approx(5058.3, abs=4):
        raise AssertionError(
            f"Did not expect the time of the simulated free fall to be {timeList[-1]} seconds."
        )

testTunnel2 = passed(testTunnel1, timeout=90, hide=False)(
    simulate_ultimate_free_fall
    .call(6.38e6, 0.01)
    .do(lambda state: assertCorrectTime(state.returned[2]))
    .description("Correct simulation length.")
)

testTunnel3 = passed(testDef, timeout=90, hide=False)(
    simulate_ultimate_free_fall
    .call(3474, 0.01)
    .do(lambda state: validate_sim1(state.returned, (-3474, 3474, -4.315, 4.315)))
    .description("Correct speeds and distances starting at height 3474")
)

@test()
def showsGraph():
    """Either saves a graph into a file, or shows a graph on the screen."""
    assert "savefig" in static.getFunctionCalls() or "show" in static.getFunctionCalls()
