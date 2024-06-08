import pandas as pd
from Bio.KEGG import REST
import argparse
import re
from rich.progress import Progress
import pathlib
import urllib
from termcolor import colored
import sys


def main():
    args = arguments_parse()
    ids = args.ids_list.split(",")
    list_data = []

    with Progress() as progress:
        task1 = progress.add_task("[cyan]Retrieving info...", total=len(ids))
        while not progress.finished:
            for id in ids:
                data = get_info(id)
                filtered_data = filter_info(data)
                list_data.append(filtered_data)
                progress.update(task1, advance=1)

    path = pathlib.Path("./KEGG_info_results")
    path.mkdir(exist_ok=True)
    to_df(list_data, args.name, path)


def arguments_parse():
    parser = argparse.ArgumentParser(
        prog="KEGG Info",
        description="python module to help get" "IDs translated with KEGG info",
    )
    parser.add_argument("ids_list")
    parser.add_argument("--name")
    args = parser.parse_args()
    return args


def get_info(id):
    try:
        return REST.kegg_get(id).read()
    except urllib.error.HTTPError as e:
        if e.code == 400:
            print(
                colored(
                    "ID invalid. Are you sure it is correct? Please, input a valid ID.",
                    "magenta",
                )
            )
        sys.exit()


def filter_info(info):
    if "DESCRIPTION" in info:
        return list(
            re.search(r"NAME\s+(.+)\nDESCRIPTION\s+(.+)\nCLASS\s+(.+)", info).groups()
        )

    return list(re.search(r"NAME\s+(.+)\n", info).groups()) + [None, None]


def to_df(data, name, path):
    df = pd.DataFrame(data, columns=["Name", "Description", "Class"])
    df.to_csv(f"{path}/ids_translated_KEGG_{name}.csv", sep=",", index=False)


if __name__ == "__main__":
    main()
