import argparse
from src.config import InitialConfig
from src.task.args import TaskArgParser

if __name__ == "__main__":
    config = InitialConfig.load()
    parser = argparse.ArgumentParser()

    # Score task subparser
    task_arg_parser = TaskArgParser()
    task_arg_parser.add_subparsers(parser)

    # Parse all arguments
    args = parser.parse_args()

    # Get action based on task
    action = task_arg_parser.get_action(args)
    action()
