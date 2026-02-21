#!/usr/bin/env python3
import argparse
import socket
import sys

BUF = 8192

def recv_until_newline(sock: socket.socket) -> tuple[bytes, bytes]:
    """Return (line_without_newline, remaining_bytes_after_newline)."""
    buf = b""
    while b"\n" not in buf:
        chunk = sock.recv(BUF)
        if not chunk:
            raise ConnectionError("Connection closed before newline header")
        buf += chunk
    line, rest = buf.split(b"\n", 1)
    return line, rest

def main() -> int:
    ap = argparse.ArgumentParser(description="Request a file from a peer and verify Content-Length framing.")
    ap.add_argument("--ip", default="127.0.0.1")
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--file", required=True, help="Filename to request (e.g., fileC.txt)")
    ap.add_argument("--timeout", type=float, default=8.0)
    args = ap.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(args.timeout)

    try:
        s.connect((args.ip, args.port))
        s.sendall((args.file + "\n").encode("utf-8"))

        hdr_line, rest = recv_until_newline(s)
        hdr_text = hdr_line.decode("utf-8", errors="replace").strip()
        print(hdr_text)

        if not hdr_text.lower().startswith("content-length:"):
            print("ERROR: Missing/invalid Content-Length header", file=sys.stderr)
            return 2

        size = int(hdr_text.split(":", 1)[1].strip())

        data = bytearray()
        if rest:
            data.extend(rest[:size])

        while len(data) < size:
            chunk = s.recv(min(BUF, size - len(data)))
            if not chunk:
                break
            data.extend(chunk)

        print(f"bytes={len(data)} expected={size}")
        return 0 if len(data) == size else 3

    finally:
        try:
            s.close()
        except Exception:
            pass

if __name__ == "__main__":
    raise SystemExit(main())