import argparse
from datetime import datetime
from pathlib import Path
import shutil
import sys
from typing import Sequence


def split_date_from_filename(file_name):
    """Returns a tuple of (system, date)"""

    split_parts = file_name.split()
    system = " ".join(split_parts[:-1])
    date = datetime.strptime(split_parts[-1][:-4], r"(%Y%m%d-%H%M%S)")

    return (system, date)


def parse_dat_files_in_dir(dat_path):
    dat_structure = {}
    for dat_file in dat_path.glob("**/*.dat"):
        try:
            system, date = split_date_from_filename(dat_file.name)
        except ValueError:
            # Skip files which do not have a supported date in their name
            continue

        dat_structure[system] = {"timestamp": date, "path": dat_file}

    return dat_structure


def determine_transformations(new_files, current_files):
    transformations = []

    for system, file_data in new_files.items():
        # Check if the system is present in dest_files
        if system in current_files:
            current_file = current_files[system]

            # Check if the source file is newer than the dest file
            if file_data["timestamp"] > current_file["timestamp"]:
                transformations.append((file_data["path"], current_file["path"]))

    return transformations


def apply_transformations(transformations):
    for new_file, old_file in transformations:
        dest_dir = old_file.parent

        print(f"Deleting {old_file.name}")
        old_file.unlink()

        print(f"Copying {new_file.name} to {dest_dir}")
        shutil.copy(new_file, dest_dir)


def run(new_files_dir, current_files_dir):
    new_files = parse_dat_files_in_dir(new_files_dir)
    current_files = parse_dat_files_in_dir(current_files_dir)

    transformations = determine_transformations(new_files, current_files)

    for new_file, old_file in transformations:
        print(f"{old_file.name} -> {new_file.name} ")

    if len(transformations) > 0:
        response = None
        while response not in ["y", "n"]:
            response = input("Transform? (y/n): ").lower()

        if response == "y":
            apply_transformations(transformations)


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="datpack-update", description="Update No-Intro DAT files"
    )
    parser.add_argument("src", type=Path, help="Source directory of new DAT files")
    parser.add_argument(
        "dest", type=Path, help="Destination directory of updated DAT files"
    )

    args = parser.parse_args(argv)

    run(args.src, args.dest)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
