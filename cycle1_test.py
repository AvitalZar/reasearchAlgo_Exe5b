import pytest
import networkx as nx, numpy as np
from cycle1 import has_cycle1, WeightedDiGraph, non_efficient_has_cycle1, random_weighted_digraph, random_weighted_dgnm
from testcases import parse_testcases

testcases = parse_testcases("testcases.txt")

def run_testcase(input:str):
    graph = WeightedDiGraph(*input)
    return has_cycle1(graph)
    

@pytest.mark.parametrize("testcase", testcases, ids=[testcase["name"] for testcase in testcases])
def test_cases(testcase):
    actual_output = run_testcase(testcase["input"])
    assert actual_output == testcase["output"], f"Expected {testcase['output']}, got {actual_output}"


def test_illegal_inputs():
    with pytest.raises(ValueError):
        has_cycle1(WeightedDiGraph([0,1,-0.5]))
    with pytest.raises(ValueError):
        has_cycle1(WeightedDiGraph([0,1,0],[1,2,0],[2,0,0]))

def test_random_inputs(): #takes graphs in growing sizes and compares the output to the non-efficient implementation
    for n in range(1, 10):
        graph = random_weighted_digraph(n, 0.2)
        assert has_cycle1(graph) == non_efficient_has_cycle1(graph)

def test_runtime():
    import time
    for n in range(500, 1000, 10):
        m = np.random.randint(0, 100*n)
        graph = random_weighted_dgnm(n, m)
        start_time = time.time()
        has_cycle1(graph)
        end_time = time.time()
        assert end_time - start_time < 1, f"Test failed for n={n}, m={m}. Time taken: {end_time - start_time} seconds"
