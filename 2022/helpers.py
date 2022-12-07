class AoCSolution:
    """
    Base class for Advent of Code problems.

    Point is to reuse code that is used over and over, such as
    loading the input file, so that the dayX.py file contains just
    problem solving logic.

    Usage:
    Subclass this and override the clean_input() and main() methods.
    Then use the RUN method, not the main() method, to start.

    Note:
    The inputs/dayX.txt file should use the line "___INPUTSEP___"
    to separate different input sets.
    """
    def __init__(self, day: int):
        input_file = f"inputs/day{day}.txt"

        with open(input_file) as f:
            self.raw_true_input, *self.raw_test_inputs = f.read().split("___INPUTSEP___\n")

    def run(self, input_select: int=1):
        """
        Run solution on the specified input.

        input_select=0: Use the "true" input for the problem
        input_select=1: Use the first set of test data,
        input_select=2: Use the second set of test data,
        ...
        """
        if input_select == 0:
            raw_input = self.raw_true_input
        else:
            raw_input = self.raw_test_inputs[input_select - 1]

        return self.main(self.clean_input(raw_input))

    def clean_input(self, raw_input):
        """
        Converts the puzzle input into a form useful for the problem.

        (override this)
        """
        raise NotImplementedError

    def main(self, cleaned_input):
        """
        Implements the step sequence from cleaned input to solution.

        (override this)
        """
        raise NotImplementedError
