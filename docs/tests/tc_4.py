#!/usr/bin/env python3
import argparse
import os

def main() -> int:
    ap = argparse.ArgumentParser(description="Print integer mtime of a file (seconds since epoch).")
    ap.add_argument("path", help="Path to file (e.g., fileB.txt)")
    args = ap.parse_args()

    mtime = int(os.path.getmtime(args.path))
    print(mtime)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())