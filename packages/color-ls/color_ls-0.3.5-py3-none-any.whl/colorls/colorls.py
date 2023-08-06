#!/usr/bin/python3
# -*- coding: utf-8 - *-
__author__ = "Romeet Chhabra"
__copyright__ = "Copyright 2020, Romeet Chhabra"
__license__ = "MIT"

import os
import shutil
import sys
import site
from pathlib import Path
import argparse
import time
from configparser import ConfigParser


# https://en.wikipedia.org/wiki/ANSI_escape_code
def print_format_table():
    for style in range(9):
        for fg in range(30, 40):
            s1 = ''
            for bg in range(40, 50):
                fmt = ';'.join([str(style), str(fg), str(bg)])
                s1 += f'\x1b[{fmt}m {fmt} \x1b[0m'
            print(s1)
        print('\n')


def get_config():
    config = ConfigParser()
    config.read([
                os.path.join(sys.prefix, 'colorls/config/colorls.ini'),
                os.path.join(site.USER_BASE, 'colorls/config/colorls.ini'),
                os.path.expanduser('~/.config/colorls.ini'),
                os.path.expanduser('~/.colorls.ini'),
                os.path.join(Path(__file__).parent.absolute(), 'config/colorls.ini'),
                ], encoding='utf8')
    return dict(config['FORMATTING']), dict(config['ICONS']), dict(config['ALIASES'])


ANSI, ICONS, ALIAS = get_config()
SUFFIX = {'dir': '/', 'link': '@', 'exe': '*', 'mount': '^'}


if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    from pwd import getpwuid
    from grp import getgrgid
    UID_SUPPORT = True
else:
    UID_SUPPORT = False


METRIC_PREFIXES = ['b', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
METRIC_MULTIPLE = 1024.
SI_MULTIPLE = 1000.


def get_human_readable_size(size, base=METRIC_MULTIPLE):
    for pre in METRIC_PREFIXES:
        if size < base:
            return f"{size:4.0f}{pre}"
        size /= base


def get_keys(path):
    n, ext = path.stem.lower(), path.suffix.lower()
    if ext == '':
        ext = n             # Replace ext with n if ext empty
    if ext.startswith('.'):
        ext = ext[1:]       # Remove leading period

    if path.is_symlink():
        key1 = "link"
    elif path.is_dir():
        key1 = "dir"
    elif path.is_file():
        key1 = "file"
    elif path.is_mount():
        key1 = "mount"
    elif n.startswith('.'):
        key1 = "hidden"
    else:
        key1 = "none"

    if ext in ALIAS:
        if ALIAS[ext] in ANSI:
            key1 = ALIAS[ext]
        key2 = ALIAS[ext]
    else:
        key2 = key1
    return key1.lower(), key2.lower()


def print_tree_listing(path, level=0, pos=0, tag=False, clear=False):
    tree_str = "   |   " * level + "   " + "---"
    print(tree_str, end="")
    print_short_listing(path, expand=True, tag=tag, clear=clear, end='\n')


def print_long_listing(path, is_numeric=False, size_base=METRIC_MULTIPLE, tag=False, clear=False):
    try:
        st = path.stat()
        size = st.st_size
        sz = get_human_readable_size(size, size_base)
        mtime = time.ctime(st.st_mtime)
        mode = os.path.stat.filemode(st.st_mode)
        ug_string = ""
        if UID_SUPPORT:
            uid = getpwuid(st.st_uid).pw_name if not is_numeric else str(st.st_uid)
            gid = getgrgid(st.st_gid).gr_name if not is_numeric else str(st.st_gid)
            ug_string = f"{uid:4} {gid:4}"
        hln = st.st_nlink
        print(f"{mode} {hln:3} {ug_string} {sz} {mtime} ", end="")
        print_short_listing(path, expand=True, tag=tag, clear=clear, end='\n')
    except FileNotFoundError:
        ...


def print_short_listing(path, expand=False, tag=False, clear=False, sep_len=None, end='\t'):
    if clear:
        fmt, ico = 'none', 'none'
    else:
        fmt, ico = get_keys(path)
    name = path.name + (SUFFIX.get(fmt, '') if tag else '')
    if expand and path.is_symlink():
        name += " -> " + str(path.resolve())
    # Pretty certain using default sep_len is going to create issues
    sep_len = sep_len if sep_len else len(name)
    print(f"\x1b[{ANSI[fmt]}m{' ' + ICONS.get(ico, '') + '  '}{name:<{sep_len}}\x1b[0m", end=end)


def process_dir(directory, args, level=0, size=None):
    report = dict()
    end = '\n' if vars(args)['1'] else '\t'
    contents, files, subs = list(), list(), list()

    try:
        p = Path(directory)
        if p.exists() and p.is_dir():
            if level == 0:
                print()
                print_short_listing(p.absolute(), clear=True, end=':\n')
            contents = list(p.iterdir())
            if args.ignore:
                remove_list = list(p.glob(args.ignore))
                contents = [c for c in contents if c not in remove_list]
            files = [x for x in contents if x.is_file()]
            subs = [x for x in contents if x.is_dir()]
        elif p.exists() and p.is_file():
            contents = [p]
        else:
            contents = list(Path('.').glob(directory))
    except Exception as e:
        print(e, file=sys.stderr)

    if args.directory:
        entries = subs
    elif args.file:
        entries = files
    else:
        entries = contents

    entries = sorted(entries, key=lambda s: str(s)[1:].lower() if str(s).startswith('.') else str(s).lower())

    # TODO: A more elegant solution to aligning short print listing. This is an awful hack!
    longest_entry = max([len(str(x.name)) for x in entries]) if len(entries) > 0 else None
    if longest_entry and size:
        max_items = size[0] // (longest_entry + 10)     # 10 is just a buffer amount. can be updated if not pretty
    else:
        max_items = 9999999
    run = 0
    for path in entries:
        if not args.all and path.name.startswith('.'):
            continue
        if args.ignore_backups and path.name.endswith('~'):
            continue
        if args.long or args.numeric_uid_gid:
            if args.si:
                print_long_listing(path, is_numeric=args.numeric_uid_gid, size_base=SI_MULTIPLE, tag=args.classify)
            else:
                print_long_listing(path, is_numeric=args.numeric_uid_gid, tag=args.classify)
        elif args.tree and args.tree > 0:
            print_tree_listing(path, level=level, tag=args.classify)
            if path.is_dir() and level < args.tree - 1:
                report[path.name] = process_dir(path, args, level=level + 1, size=size)[path]
        else:
            print_short_listing(path, sep_len=longest_entry, tag=args.classify, end=end)
            run += 1
            if run >= max_items:
                print()
                run = 0

    if args.recursive and not args.tree:
        for sub in subs:
            report[sub.name] = process_dir(sub, args, size=size)[sub]

    rep = dict()
    rep['files'] = len(files)
    rep['dirs'] = len(subs)
    report[directory] = rep
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-1", action="store_true", default=False, help="list items on individual lines")
    parser.add_argument("-a", "--all", action="store_true", default=False, help="do not ignore entires starting with .")
    parser.add_argument("-B", "--ignore-backups", action="store_true", default=False,
                        help="do not list implied entires ending with ~")
    parser.add_argument("-d", "--directory", action="store_true", default=False,
                        help="list directories themselves, not their contents")
    parser.add_argument("-f", "--file", action="store_true", default=False, help="list files only, not directories")
    parser.add_argument("-F", "--classify", action="store_true",
                        default=False, help="append indicator (one of */=>@|) to entries")
    parser.add_argument("-I", "--ignore", metavar="PATTERN", help="do not list implied entries matching shell PATTERN")
    parser.add_argument("-l", "--long", action="store_true", default=False, help="use a long listing format")
    parser.add_argument("-n", "--numeric-uid-gid", action="store_true",
                        default=False, help="like -l, but list numeric user and group IDs")
    parser.add_argument("-R", "--recursive", action="store_true", default=False, help='list subdirectories recursively')
    parser.add_argument("--report", action="store_true", default=False,
                        help="brief report about number of files and directories")
    parser.add_argument("-t", "--tree", metavar="DEPTH", type=int, nargs='?', const=3, help="max tree depth")
    parser.add_argument("--version", action="store_true", default=False, help="display current version number")
    parser.add_argument("--si", action="store_true", default=False, help="display current version number")
    parser.add_argument("FILE", default=".", nargs=argparse.REMAINDER,
                        help="List information about the FILEs (the current directory by default).")
    args = parser.parse_args()
    if args.version:
        with open(os.path.join(Path(__file__).parent.absolute(), '_version.py')) as VERSION_FILE:
            version = VERSION_FILE.read()
        print("colorls version " + version.split('"')[1])

    if not args.FILE:
        args.FILE = ["."]

    report = list()
    term_size = shutil.get_terminal_size()
    for FILE in args.FILE:
        report.append(process_dir(FILE, args, size=term_size))
        print()

    # TODO: Fix report - only shows current directory and next correctly. Likely overwritten dictionary values
    if args.report and report:
        print("\n --- REPORT ---")
        for n in report:
            for k, v in reversed(n.items()):
                print(f"{k} -> {v}")


if __name__ == '__main__':
    main()


# vim: ts=4 sts=4 sw=4 et syntax=python:
