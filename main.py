"""Copy the bundled steaming ramen picture to /output/entry.png.

Stdlib only, deterministic, no network. The image lives in this
repository as entry.png; the program just places it where the judge
expects it.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    with open(DST, "rb") as f:
        magic = f.read(8)
    assert magic == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
    print("wrote", DST, os.path.getsize(DST), "bytes")


if __name__ == "__main__":
    main()
