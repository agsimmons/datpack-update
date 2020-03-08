import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil


def parse_args():
    parser = argparse.ArgumentParser(description="Update no-intro DAT files")
    parser.add_argument("src", help="Source directory of new DAT files")
    parser.add_argument("dest", help="Destination directory of updated DAT files")

    return parser.parse_args()


def split_date_from_filename(file_name):
    """Returns a tuple of (system, date)"""

    split_parts = file_name.split()
    system = " ".join(split_parts[:-1])
    date = datetime.strptime(split_parts[-1][:-4], r"(%Y%m%d-%H%M%S)")

    return (system, date)


def parse_dat_files_in_dir(dat_path):
    dat_files = dat_path.glob("*.dat")

    dat_structure = {}
    for dat_file in dat_files:
        system, date = split_date_from_filename(dat_file.name)

        dat_structure[system] = {"timestamp": date, "path": dat_file}

    return dat_structure


def determine_transformations(source_files, dest_files):
    transformations = []

    for system, file_data in source_files.items():
        # Check if the system is present in dest_files
        if system in dest_files:
            dest_file = dest_files[system]

            # Check if the source file is newer than the dest file
            if file_data["timestamp"] > dest_file["timestamp"]:
                transformations.append((file_data["path"], dest_file["path"]))

    return transformations


def apply_transformations(transformations):
    for src, dst in transformations:
        print(f"{src.name} -> {dst.name}\n")

        dest_dir = dst.parent

        print(f"Deleting {dst.name}...")
        dst.unlink()

        print(f"Copying {src.name} to {dest_dir}...")
        shutil.copy(src, dest_dir)


def main(args):
    source_dir = Path(args.src)
    dest_dir = Path(args.dest)

    source_files = parse_dat_files_in_dir(source_dir)
    dest_files = parse_dat_files_in_dir(dest_dir)

    transformations = determine_transformations(source_files, dest_files)

    for src, dst in transformations:
        print(f"{src.name} -> {dst.name}")

    if len(transformations) > 0:
        response = None
        while response not in ["y", "n"]:
            response = input("Transform? (y/n): ").lower()

        if response == "y":
            apply_transformations(transformations)


if __name__ == "__main__":
    args = parse_args()
    main(args)