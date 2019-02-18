import os
import csv
import argparse
from datetime import datetime
from math import log
from hashlib import md5


def build_checksum_csv(input_dir, output_file):
    with open(output_file, "w") as fh:
        csv_writer = csv.DictWriter(fh, fieldnames=[
            "File Name",
            "File Size",
            "File Path",
            "File Extension",
            "Date Created",
            "Date Last Modified",
            "MD5"
        ])
        csv_writer.writeheader()
        add_dir_to_csv_recursive(input_dir, csv_writer)


def add_dir_to_csv_recursive(dir, csv_writer):
    for child in os.listdir(dir):
        fullpath = os.path.join(dir, child)
        if os.path.isdir(fullpath):
            add_dir_to_csv_recursive(fullpath, csv_writer)
        elif os.path.isfile(fullpath):
            datetime_format = "%m-%d-%Y %H:%M:%S"
            row = {
                "File Name": child,
                "File Size": format_filesize(os.path.getsize(fullpath)),
                "File Path": fullpath,
                "File Extension": child.split(".")[-1],
                "Date Created": get_file_created_datetime(fullpath, datetime_format),
                "Date Last Modified": get_file_modified_datetime(fullpath, datetime_format),
                "MD5": get_file_md5(fullpath)
            }
            csv_writer.writerow(row)


def format_filesize(num):
    unit_list = list(zip(['bytes', 'KB', 'MB', 'GB', 'TB', 'PB'], [0, 1, 2, 2, 2, 2]))
    if num > 1:
        exponent = min(int(log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'


def get_file_created_datetime(file, format):
    stat = os.stat(file)
    if hasattr(stat, "st_birthtime"):
        timestamp = int(stat.st_birthtime)
    else:
        timestamp = int(os.path.getctime(file))
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime(format)


def get_file_modified_datetime(file, format):
    timestamp = int(os.path.getmtime(file))
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime(format)


def get_file_md5(file):
    hasher = md5()
    with open(file, "rb") as fh:
        for chunk in iter(lambda: fh.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool to recurse through directories and generate a CSV of file metadata contained within")
    parser.add_argument("-d", "--directory", dest="directory", help="The directory to recurse through")
    parser.add_argument("-f", "--file", dest="file", help="The CSV file to create")
    args = parser.parse_args()

    build_checksum_csv(args.directory, args.file)