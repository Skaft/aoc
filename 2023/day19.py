import re
from math import prod


with open("inputs/day19.txt") as f:
    true_input, *test_inputs = f.read().split("\n___INPUTSEP___\n")


class Workflow:
    def __init__(self, conditions, else_case):
        self.conditions = dict(cond.split(":") for cond in conditions)
        self.else_case = else_case

    def check(self, rating):
        x, m, a, s = (rating[c] for c in "xmas")
        for condition, destination in self.conditions.items():
            if eval(condition):
                return destination
        return self.else_case


class PartOne:
    def __init__(self, raw_input):
        workflows, ratings = raw_input.split("\n\n")

        self.workflows = {}
        pattern = re.compile(r"(\w+)\{(.*)\}")
        for line in workflows.splitlines():
            name, content = pattern.search(line).groups()
            *conditions, else_case = content.split(",")
            self.workflows[name] = Workflow(conditions, else_case)

        pattern = re.compile(r"(\w)=(\d+)")
        self.ratings = []
        for line in ratings.splitlines():
            rating = dict((attribute, int(digits)) for attribute, digits in pattern.findall(line))
            self.ratings.append(rating)

    def main(self):
        total = 0
        for rating in self.ratings:
            workflow = "in"
            while True:
                output = self.workflows[workflow].check(rating)
                if output == "R":
                    break
                elif output == "A":
                    total += sum(rating.values())
                    break
                else:
                    workflow = output
        return total

class Span:
    def __init__(self, lower=1, upper=4000):
        self.lower = lower
        self.upper = upper

    def __lt__(self, a: int):
        if a <= self.lower:
            return None
        if self.upper < a:
            return self
        return Span(self.lower, a - 1)

    def __gt__(self, a: int):
        if a >= self.upper:
            return None
        if self.lower > a:
            return self
        return Span(a + 1, self.upper)
    
    def __sub__(self, span):
        if span is None:
            return self
        if span.upper < self.lower:
            return self
        if span.lower > self.upper:
            return self
        if span.lower <= self.lower and span.upper >= self.upper:
            return None
        if self.lower <= span.upper < self.upper:
            return Span(span.upper + 1, self.upper)
        if self.lower < span.lower <= self.upper:
            return Span(self.lower, span.lower - 1)
        raise AssertionError(f"{self}, {span}")

    def __repr__(self):
        return f"({self.lower}, {self.upper})"


class SpanGroup:
    def __init__(self):
        self.spans = {
            "x": Span(),
            "m": Span(),
            "a": Span(),
            "s": Span(),
        }
    
    def restrict(self, condition):
        attr = condition[0]
        span = self.spans[attr]
        restricted_span = eval("span" + condition[1:])
        return attr, restricted_span
    
    def copy(self):
        sg = SpanGroup()
        sg.spans = {**self.spans}
        return sg

    def __repr__(self) -> str:
        return str(self.spans)

class PartTwo(PartOne):
    def dfs(self):

        q = [("in", SpanGroup())]
        successes = []
        while q:
            node, span_group = q.pop()
            if node == "R":
                continue
            if node == "A":
                successes.append(span_group)
                continue

            workflow = self.workflows[node]
            for condition, destination in workflow.conditions.items():
                changed_attr, new_span = span_group.restrict(condition)

                # condition true: add to queue
                if new_span:
                    new_group = span_group.copy()
                    new_group.spans[changed_attr] = new_span
                    q.append((destination, new_group))

                # condition false: restrict span_group
                flipped_span = span_group.spans[changed_attr] - new_span
                if flipped_span is None:
                    break
                new_group = span_group.copy()
                new_group.spans[changed_attr] = flipped_span
                span_group = new_group
            else:
                q.append((workflow.else_case, span_group))
        return successes

    def main(self):
        total = 0

        for span_group in self.dfs():
            print(span_group)
            ranges = span_group.spans.values()
            total += prod((s.upper + 1 - s.lower) for s in ranges)
        return total


if __name__ == "__main__":
    print(PartOne(true_input).main())
    print(PartTwo(true_input).main())


# TESTS

def test_subtracting_spans_handles_edge_cases():
    large = Span(1, 4000)
    sub = Span(1, 1350)
    assert (large - sub).lower == 1351

def test_part1_gives_correct_result_on_test_input():
    assert PartOne(test_inputs[0]).main() == 19114

def test_part2_gives_correct_result_on_test_input():
    assert PartTwo(test_inputs[0]).main() == 167409079868000
