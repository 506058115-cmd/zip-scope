#!/usr/bin/env python3
"""Inspect ZIP entry names and declared sizes without extracting files."""

import argparse
import ntpath
from pathlib import Path, PurePosixPath
import stat
import sys
from zipfile import BadZipFile, ZipFile


GIB = 1024 ** 3


def terminal_safe(value):
    return "".join(
        char if char.isprintable() else char.encode("unicode_escape").decode("ascii")
        for char in value
    )


def unsafe_path(name):
    normalized = name.replace("\\", "/")
    drive, _ = ntpath.splitdrive(normalized)
    parts = PurePosixPath(normalized).parts
    reasons = []
    if normalized.startswith("/") or drive:
        reasons.append("包含根路径或盘符")
    if ".." in parts:
        reasons.append("包含 .. 路径段")
    return reasons


def human_size(size):
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"):
        if value < 1024 or unit == "EiB":
            return f"{int(value)} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024


def inspect(path, show_entries):
    with ZipFile(path) as archive:
        # ponytail: zipfile holds central-directory entries in memory; use a
        # custom streaming parser only if million-entry archives matter.
        entries = archive.infolist()

    files = [entry for entry in entries if not entry.is_dir()]
    expanded = sum(entry.file_size for entry in files)
    compressed = sum(entry.compress_size for entry in files)
    print(
        f"{len(entries)} 个条目 · {len(files)} 个文件 · "
        f"展开大小 {human_size(expanded)} · 压缩大小 {human_size(compressed)}"
    )
    if expanded >= GIB:
        print("提示：声明的展开体积达到或超过 1 GiB。")

    findings = 0
    for entry in entries:
        reasons = unsafe_path(entry.filename)
        unix_mode = entry.external_attr >> 16
        if stat.S_ISLNK(unix_mode):
            reasons.append("符号链接")
        if reasons:
            findings += 1
            print(f"需留意: {ascii(entry.filename)} · {'、'.join(reasons)}")
    if not findings:
        print("未发现明显的路径越界条目；这不能证明压缩包安全。")

    if show_entries:
        print("\n压缩包条目")
        for entry in entries:
            kind = "目录" if entry.is_dir() else human_size(entry.file_size)
            print(f"  {kind:>10}  {ascii(entry.filename)}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="检查 ZIP 文件名和体积信息，不解压、不写入文件。"
    )
    parser.add_argument("archive", help="ZIP 文件路径")
    parser.add_argument(
        "--list", action="store_true", help="列出所有条目名称与声明大小"
    )
    args = parser.parse_args(argv)

    try:
        inspect(Path(args.archive).expanduser(), args.list)
    except (OSError, UnicodeError, BadZipFile, EOFError) as error:
        print(
            f"zip-scope: 无法读取 ZIP 文件：{terminal_safe(str(error))}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
