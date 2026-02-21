#!/usr/bin/env python3
import argparse
import os

def main() -> int:
    ap = argparse.ArgumentParser(description="Create a big binary file for partial-transfer testing.")
    ap.add_argument("--out", default="big.bin")
    ap.add_argument("--mb", type=int, default=10, help="Size in MB (default 10)")
    args = ap.parse_args()

    size = args.mb * 1024 * 1024
    with open(args.out, "wb") as f:
        f.write(os.urandom(size))

    print(f"Wrote {args.out} ({size} bytes)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())