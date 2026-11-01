
#!/usr/bin/env python3
"""Person 3: Monitoring and Performance for Smart Content Delivery."""

import argparse
import csv
import socket
import time
from statistics import mean


def request_server(host, port, message, timeout):
    """Send one TCP request and measure its response time."""
    start = time.perf_counter()
    response = ""
    error = ""

    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.sendall(message.encode("utf-8"))
            sock.shutdown(socket.SHUT_WR)

            chunks = []
            while True:
                data = sock.recv(65536)
                if not data:
                    break
                chunks.append(data)

            response = b"".join(chunks).decode(
                "utf-8", errors="replace"
            )

    except (OSError, TimeoutError) as exc:
        error = str(exc)

    elapsed_ms = (time.perf_counter() - start) * 1000

    return response, elapsed_ms, error


def main():
    parser = argparse.ArgumentParser(
        description="Monitor TCP content servers and measure performance."
    )
    parser.add_argument("--servers", required=True,
                        help="Example: Server1=10.0.0.2:5001,Server2=10.0.0.3:5002")
    parser.add_argument("--rounds", type=int, default=10)
    parser.add_argument("--content", default="file1")
    parser.add_argument("--timeout", type=float, default=2.0)
    parser.add_argument("--output", default="performance_results.csv")
    parser.add_argument("--label", default="normal")
    args = parser.parse_args()

    if args.rounds < 1:
        parser.error("--rounds must be at least 1")

    servers = []
    for item in args.servers.split(","):
        name, address = item.strip().split("=", 1)
        host, port = address.rsplit(":", 1)
        servers.append((name.strip(), host.strip(), int(port)))

    results = []

    print("\nSMART CONTENT DELIVERY - PERFORMANCE MONITOR")
    print("Experiment:", args.label)

    # First, check basic TCP availability.
    print("\n--- Server availability ---")
    for name, host, port in servers:
        response, elapsed, error = request_server(
            host, port, "HEALTH", args.timeout
        )
        available = not error and bool(response.strip())

        print(
            f"{name}: {'RESPONDING' if available else 'NOT RESPONDING'} "
            f"({elapsed:.2f} ms)"
        )

        if error:
            print("  Reason:", error)
        elif response:
            print("  Response:", response[:100].replace("\n", " "))

    # Then measure content requests.
    print("\n--- Performance tests ---")

    for round_no in range(1, args.rounds + 1):
        for name, host, port in servers:
            response, elapsed, error = request_server(
                host, port, f"GET {args.content}", args.timeout
            )

            success = not error and bool(response)
            size = len(response.encode("utf-8")) if success else 0
            throughput = size / (elapsed / 1000) if success and elapsed > 0 else 0

            row = {
                "experiment": args.label,
                "round": round_no,
                "server": name,
                "host": host,
                "port": port,
                "success": success,
                "response_time_ms": round(elapsed, 3),
                "response_bytes": size,
                "throughput_bytes_per_sec": round(throughput, 3),
                "error": error,
            }
            results.append(row)

            status = "OK" if success else "FAILED"
            print(
                f"Round {round_no} | {name} | {status} | "
                f"Response time: {elapsed:.2f} ms | "
                f"Throughput: {throughput:.2f} B/s"
            )

    # Save raw measurements for the project report.
    fields = [
        "experiment", "round", "server", "host", "port", "success",
        "response_time_ms", "response_bytes",
        "throughput_bytes_per_sec", "error"
    ]

    with open(args.output, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print("\n--- Summary ---")

    for name, _, _ in servers:
        server_results = [
            row for row in results
            if row["server"] == name and row["success"]
        ]
        failures = sum(
            1 for row in results
            if row["server"] == name and not row["success"]
        )

        if server_results:
            avg_time = mean(
                row["response_time_ms"] for row in server_results
            )
            avg_throughput = mean(
                row["throughput_bytes_per_sec"] for row in server_results
            )
            print(
                f"{name}: {len(server_results)} successful, "
                f"{failures} failed, average response time "
                f"{avg_time:.2f} ms, average throughput "
                f"{avg_throughput:.2f} B/s"
            )
        else:
            print(f"{name}: 0 successful requests, {failures} failed")

    print("\nCSV results saved to:", args.output)
    print("Note: throughput is application-level, not physical link capacity.")


if __name__ == "__main__":
    main()

