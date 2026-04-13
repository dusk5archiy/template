import argparse
from typing import Callable


class TaskArgParser:
    def add_subparsers(self, parser: argparse.ArgumentParser):
        # Add subparsers for modes
        subparsers = parser.add_subparsers(
            dest="mode", help="Available modes", required=True
        )

        # Train subparser
        train_parser = subparsers.add_parser("train", help="Train the model")
        train_parser.add_argument("--model_name", "-m", type=str, required=True)
        train_parser.add_argument("--batch_size", type=int, required=True)
        train_parser.add_argument("--epochs", type=int, required=True)

        # Eval subparser
        eval_parser = subparsers.add_parser("eval", help="Evaluate the model")
        eval_parser.add_argument("--model_path", "-m", type=str, required=True)

    def get_action(self, args: argparse.Namespace) -> Callable[[], None]:
        from src.task.train import train
        
        # Return action based on mode
        if args.mode == "train":
            return lambda: train(
                model_name=args.model_name,
                batch_size=args.batch_size,
                epochs=args.epochs
            )
        # elif args.mode == "eval":
        #     from src.task.eval import evaluate_asl
        #     return lambda: evaluate_asl(
        #         model_path=args.model_path,
        #         config=self.config,
        #     )

        return lambda: None
