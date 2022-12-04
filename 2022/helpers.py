class AoCSolution:
    """
    Base class for Advent of Code problems.

    Point is to reuse code that is used over and over, such as
    loading the input file, so that the dayX.py file contains just
    problem solving logic.

    Usage:
    Subclass this and override the clean_input() and main() methods.
    Then use the RUN method, not the main() method, to start.
    """
    def __init__(self, day: int):
        input_file = f"inputs/day{day}.txt"

        with open(input_file) as f:
            self.raw_true_input, *self.raw_test_inputs = f.read().split("___INPUTSEP___\n")

        self.true_input = self.clean_input(self.raw_true_input)
        self.test_inputs = [self.clean_input(test) for test in self.raw_test_inputs]

    def run(self, input_select: int=1):
        if input_select == 0:
            cleaned_input = self.true_input
        else:
            cleaned_input = self.test_inputs[input_select - 1]

        return self.main(cleaned_input)

    def clean_input(self, raw_input):
        """
        Convert the puzzle input into a form useful for the problem

        (override this)
        """
        raise NotImplementedError

    def main(self, cleaned_input):
        """
        The step sequence from pruned input to solution

        (override this)
        """
        raise NotImplementedError
