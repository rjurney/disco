import argparse

from tqdm import tqdm

from disco.legaltype import search


def parse_args():
    parser = argparse.ArgumentParser(description="Profiling disco performance")
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        required=True,
        help="Provide filepath to the file with a list of names to process",
    )

    return parser.parse_args()


def read_names(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f_names:
        for line in f_names:
            yield line.strip()


def clean_all_names(filepath: str):
    for name in tqdm(read_names(filepath), leave=False):
        search(name)


def main():
    args = parse_args()
    filepath = args.data
    clean_all_names(filepath)


if __name__ == "__main__":
    main()
