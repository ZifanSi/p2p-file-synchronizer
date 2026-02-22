#!/usr/bin/env python3
import argparse
import os
import hashlib
import sys

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser(description="Create a big binary file for partial-transfer testing.")
    ap.add_argument("--out", default="big.bin", help="Output filename (default big.bin)")
    ap.add_argument("--mb", type=int, default=10, help="Size in MB (default 10)")
    args = ap.parse_args()

    if args.mb <= 0:
        print("ERROR: --mb must be > 0", file=sys.stderr)
        return 2

    size = args.mb * 1024 * 1024
    out_path = os.path.abspath(args.out)

    with open(out_path, "wb") as f:
        f.write(os.urandom(size))

    digest = sha256_file(out_path)
    print(f"Wrote {out_path} ({size} bytes) sha256={digest}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())