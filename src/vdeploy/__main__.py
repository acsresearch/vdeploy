import argparse

from .deploy import deploy_instance
import os
from . import watchdog


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("offer", type=int)
    deploy_parser.add_argument("--image", default="pytorch/pytorch")
    deploy_parser.add_argument("--timeout", default="pytorch/pytorch")
    deploy_parser.add_argument(
        "--timeout",
        default=watchdog.DEFAULT_TIMEOUT,
        type=int,
        help="Instance timeout (in minutes)",
    )

    watchdog_parser = subparsers.add_parser("start-watchdog")
    watchdog_parser.add_argument("--path", default=watchdog.DEFAULT_PATH)
    watchdog_parser.add_argument(
        "--timeout",
        default=watchdog.DEFAULT_TIMEOUT,
        type=int,
        help="Instance timeout (in minutes)",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "start-watchdog":
        watchdog.start_watchdog(args.path, args.timeout)
    if args.command == "deploy":
        # config = Config.read_config(args.filename)
        # find_offer(config.query)
        with open(os.path.expanduser("~/.vast_api_key"), "r") as f:
            key = f.read()
        os.environ["VAST_AI_API_KEY"] = key
        deploy_instance(
            offer_id=args.offer, docker_image=args.image, timeout=args.timeout
        )
    print("HelloX")


if __name__ == "__main__":
    main()
