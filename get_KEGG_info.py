import pandas as pd
from Bio.KEGG import REST
import argparse
import re
from rich.progress import Progress
import pathlib


def main():
    args = arguments_parse()
    ids = args.ids_list.split(",")
    data = []

    with Progress() as progress:
        task1 = progress.add_task("[cyan]Retrieving info...", total=len(ids))

        while not progress.finished:
            for id in ids:
                info = get_info(id)
                data.append(info)
                progress.update(task1, advance=1)

    path = pathlib.Path("./KEGG_info_results")
    path.mkdir(exist_ok=True)
    to_df(data, args.name, path)


def arguments_parse():
    parser = argparse.ArgumentParser(prog="KEGG Info",
                                     description="python module to help get"
                                     "IDs translated with KEGG info")
    parser.add_argument("ids_list")
    parser.add_argument("--name")
    args = parser.parse_args()
    return args


def get_info(id):
    info = REST.kegg_get(id).read()
    if "DESCRIPTION" in info:
        return (list(re.search(r"NAME\s+(.+)\nDESCRIPTION\s+(.+)\nCLASS\s+(.+)",
                               info).groups()))

    return (list(re.search(r"NAME\s+(.+)\n", info).groups()) + [None, None])


def to_df(data, name, path):
    df = pd.DataFrame(data, columns=["Name", "Description", "Class"])
    df.to_csv(f"{path}/ids_translated_KEGG_{name}.csv", sep=",", index=False)


if __name__ == "__main__":
    main()
