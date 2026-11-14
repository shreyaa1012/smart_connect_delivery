#!/usr/bin/env python3
"""Small client for the Person 2 gateway running on Mininet host h1."""
import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description="Request content through the smart gateway")
    parser.add_argument("content", choices=["file1", "file2", "file3"])
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--timeout", type=float, default=8.0)
    args = parser.parse_args()

    with socket.create_connection((args.host, args.port), timeout=args.timeout) as sock:
        sock.settimeout(args.timeout)
        sock.sendall(args.content.encode("utf-8"))
        sock.shutdown(socket.SHUT_WR)
        chunks = []
        while True:
            data = sock.recv(65536)
            if not data:
                break
            chunks.append(data)
    print(b"".join(chunks).decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
