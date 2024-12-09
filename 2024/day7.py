import argparse
import itertools


def parse(data):
    equations = []

    for line in data.splitlines():
        value, rest = line.split(": ")
        value = int(value)
        operands = rest.split()

        equations.append((value, operands))

    return equations

def generate_valid_test_values(equations, operator_combos=[[]]):
    max_eq_len = max(len(operands) for _, operands in equations)

    # Generate operator combinations, if not already done
    for n_operators in range(len(operator_combos), max_eq_len):
        combos = list(itertools.product("+*", repeat=n_operators))
        operator_combos.append(combos)

    for test_value, operands in equations:

        for op_seq in operator_combos[len(operands) - 1]:
            result = int(operands[0])
            for i, op in enumerate(op_seq):
                if op == "+":
                    result += int(operands[i + 1])
                elif op == "*":
                    result *= int(operands[i + 1])

            if result == test_value:
                yield test_value
                break

def generate_valid_test_values_2(equations, operator_combos=[[]]):
    max_eq_len = max(len(operands) for _, operands in equations)

    # Generate operator combinations, if not already done
    for n_operators in range(len(operator_combos), max_eq_len):
        combos = list(itertools.product("+*|", repeat=n_operators))
        operator_combos.append(combos)

    for test_value, operands in equations:

        for op_seq in operator_combos[len(operands) - 1]:
            result = int(operands[0])
            for i, op in enumerate(op_seq):
                if op == "+":
                    result += int(operands[i + 1])
                elif op == "*":
                    result *= int(operands[i + 1])
                elif op == "|":
                    result = int(str(result) + operands[i + 1])
                if result > test_value:
                    break

            if result == test_value:
                yield test_value
                break

def part1(data):
    equations = parse(data)
    valid_test_vals = list(generate_valid_test_values(equations))

    return sum(valid_test_vals)


def part2(data):
    equations = parse(data)
    valid_test_vals = list(generate_valid_test_values(equations))

    total = sum(valid_test_vals)
    invalid_equations = [eq for eq in equations if eq[0] not in valid_test_vals]

    new_valid_test_vals = list(generate_valid_test_values_2(invalid_equations))
    total += sum(new_valid_test_vals)

    return total
    

if __name__ == "__main__":
    from common import get_input

    data = get_input(day=7)

    print(part1(data))
    print(part2(data))
