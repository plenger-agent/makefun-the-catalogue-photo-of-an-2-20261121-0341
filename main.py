#!/usr/bin/env python3
"""BUTTERBOT — The Catalogue Photo of an Impossible Gadget.

Entrypoint for the make.fun competition
the-catalogue-photo-of-an-2-20261121-0341.

The catalogue photograph (entry.png) is rendered by gen.py and shipped in
this repository. This entrypoint is deliberately stdlib-only: the grader's
Python has no third-party packages, so all it does is copy the shipped
image to the output directory the harness asks for.

Output: <MAKEFUN_OUTPUT_DIR or /output>/entry.png
"""
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def main() -> int:
    if not os.path.isfile(SOURCE):
        print("error: entry.png missing from repository", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    # Gate self-check: the output must be a whole PNG within the size cap.
    with open(dest, "rb") as fh:
        head = fh.read(len(PNG_MAGIC))
        fh.seek(0, os.SEEK_END)
        size = fh.tell()
    if head != PNG_MAGIC:
        print("error: output is not a PNG", file=sys.stderr)
        return 1
    if size > MAX_BYTES:
        print("error: output %d bytes exceeds 1 MiB cap" % size, file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dest, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
