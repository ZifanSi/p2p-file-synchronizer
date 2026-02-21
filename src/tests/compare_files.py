#!/usr/bin/env python3
import argparse
import hashlib
import os
import sys

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser(description="Compare two files by size and SHA-256.")
    ap.add_argument("a")
    ap.add_argument("b")
    args = ap.parse_args()

    if not os.path.exists(args.a) or not os.path.exists(args.b):
        print("ERROR: One or both paths do not exist", file=sys.stderr)
        return 2

    sa, sb = os.path.getsize(args.a), os.path.getsize(args.b)
    ha, hb = sha256_file(args.a), sha256_file(args.b)

    print(f"{args.a}: size={sa} sha256={ha}")
    print(f"{args.b}: size={sb} sha256={hb}")

    if sa == sb and ha == hb:
        print("MATCH")
        return 0
    else:
        print("DIFFER")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())