from serde.toml import from_toml
from dataclasses import dataclass


def filter_frame(dataframe, request, name):
    value = getattr(request, name)
    if value is not None:
        return dataframe[dataframe[name] >= value]
    else:
        return dataframe


# @dataclass
# class MachineRequest:
#     gpu_total_ram: int | None
#     gpu_ram: int | None
#     cpu_ram: int | None
#     inet_down: int | None
#     inet_up: int | None
#
#     def filter_machines(self, dataframe):
#         for name in "gpu_total_ram", "gpu_ram", "cpu_ram", "inet_down", "inet_up":
#             dataframe = filter_frame(dataframe, self, name)
#         return dataframe


@dataclass
class Config:
    # machine: MachineRequest
    docker_image: str
    query: str

    @staticmethod
    def read_config(path) -> "Config":
        with open(path) as f:
            return from_toml(Config, f.read())
