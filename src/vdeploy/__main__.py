import argparse
from vast_ai_api import VastAPIHelper

from .config import Config


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("filename")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "deploy":
        config = Config.read_config(args.filename)
        api = VastAPIHelper()
        instances = api.list_available_instances()
        instances = config.machine.filter_machines(instances)
        print(instances.columns)
        instances = instances.sort_values("dph_total")
        head = instances.head(5)
        for (i, (_, inst)) in enumerate(head.iterrows()):
            print(f"{i + 1}) ${inst['dph_total']:.3f}/h {inst['geolocation']}, dlperf={inst['dlperf']:.1f} {inst['num_gpus']}x {inst['gpu_name']} ({inst['gpu_ram'] / 1024:0.1f}GiB) down={inst['inet_down']} rel={inst['reliability']:.2f}")
        api.launch_instance(instances[])
    print("HelloX")


if __name__ == "__main__":
    main()