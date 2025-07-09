import io
import itertools
from contextlib import redirect_stdout
from truth_table_generator import generate_truth_table

def test_truth_table(expr, variables, expected_outputs):
    expected_lines = [
        " | ".join(variables) + " | Output"
    ]
    for bits, output in zip(itertools.product([0, 1], repeat=len(variables)), expected_outputs):
        expected_lines.append(" | ".join(str(b) for b in bits) + f" |   {output}")

    f = io.StringIO()
    with redirect_stdout(f):
        generate_truth_table(expr)
    output = f.getvalue()

    for line in expected_lines:
        assert line in output, f"Missing line: {line}"
    print(f"Test passed for: {expr}")

test_truth_table("A+B", ["A", "B"], [
    0, 1, 1, 1
])

test_truth_table("AB'", ["A", "B"], [
    0, 0, 1, 0
])

test_truth_table("(A+B)'C", ["A", "B", "C"], [
    0, 1, 0, 0, 0, 0, 0, 0
])

test_truth_table("ABCD'", ["A", "B", "C", "D"], [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0
])

test_truth_table("A+(BC')'D", ["A", "B", "C", "D"], [
    0, 1, 0, 1, 0, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1
])

test_truth_table("A+B'+C'+D", ["A", "B", "C", "D"], [
    1, 1, 1, 1, 1, 1, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1
])

test_truth_table("((AB)')C", ["A", "B", "C"], [
    0, 1, 0, 1, 0, 1, 0, 0
])

test_truth_table("A'B'C'", ["A", "B", "C"], [
    1, 0, 0, 0, 0, 0, 0, 0
])

test_truth_table("A'+B'+C'+D'", ["A", "B", "C", "D"], [
    1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 0
])

test_truth_table("(A'(B'(C'(D'))))", ["A", "B", "C", "D"], [
    1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0
])
