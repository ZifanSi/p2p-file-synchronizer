#!/usr/bin/env python3
import argparse
import os
import sys

def main() -> int:
    ap = argparse.ArgumentParser(description="Print integer mtime and size of a file.")
    ap.add_argument("path", help="Path to file (e.g., Peer2/fileB.txt)")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 2

    mtime = int(os.path.getmtime(args.path))
    size = os.path.getsize(args.path)
    print(f"{args.path}: mtime={mtime} size={size}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())