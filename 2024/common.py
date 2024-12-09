
def get_input(day: int):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", nargs='?', const= True, default=False, type=int, help="Run with test data")
    args = parser.parse_args()

    if args.test is False:
        data_path = f"inputs/day{day}.txt"
    elif args.test is True:
        data_path = f"test_data/day{day}.txt"
    else:
        data_path = f"test_data/day{day}_{args.test}.txt"

    with open(data_path) as file:
        data = file.read()

    return data