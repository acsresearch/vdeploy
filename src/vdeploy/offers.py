import subprocess
import prettytable


def find_offer(query: str):
    offers = subprocess.check_output(
        ["vastai", "search", "offers", query, "-o", "dph+"]
    )

    offers = offers.decode().split("\n")
    header = offers[0].split()
    print(header)
    data = []
    columns = ("$/hr", "Net_up", "Net_down", "N", "Model", "RAM", "country")
    assert "country" in header
    for offer in offers[1:6]:
        if not offer:
            continue
        d = dict(zip(header, offer.split()))
        print(d)
        data.append([d[column] for column in columns])

    table = prettytable.PrettyTable()
    table.field_names = columns
    table.add_rows(data)
    print(table)
