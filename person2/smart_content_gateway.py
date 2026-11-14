#!/usr/bin/env python3
"""Person 2: request gateway for dynamic backend selection and failover.

Runs inside Mininet host h1. It probes each TCP content server using HEALTH,
selects the healthy server with the lowest measured probe latency, forwards the
GET request, and retries another healthy server if the chosen backend fails.

This is an application-layer gateway over the SDN-controlled Mininet network;
it does not perform OpenFlow NAT or transparent packet rewriting.
"""

import argparse
import socket
import threading
import time


def parse_servers(value):
    servers = []
    for item in value.split(","):
        name, address = item.strip().split("=", 1)
        host, port = address.rsplit(":", 1)
        servers.append({"name": name.strip(), "host": host.strip(), "port": int(port)})
    if not servers:
        raise ValueError("At least one backend server is required")
    return servers


def exchange(host, port, message, timeout):
    start = time.perf_counter()
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        sock.sendall(message.encode("utf-8"))
        sock.shutdown(socket.SHUT_WR)
        chunks = []
        while True:
            data = sock.recv(65536)
            if not data:
                break
            chunks.append(data)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return b"".join(chunks).decode("utf-8", errors="replace"), elapsed_ms


def probe(server, timeout):
    try:
        response, elapsed = exchange(server["host"], server["port"], "HEALTH", timeout)
        if response.strip():
            return True, elapsed, response.strip()
    except OSError as exc:
        return False, float("inf"), str(exc)
    return False, float("inf"), "empty health response"


class Gateway:
    def __init__(self, servers, timeout):
        self.servers = servers
        self.timeout = timeout
        self.lock = threading.Lock()
        self.last_selected = None

    def healthy_backends(self):
        healthy = []
        for server in self.servers:
            ok, latency, detail = probe(server, self.timeout)
            print(f"[HEALTH] {server['name']}: {'UP' if ok else 'DOWN'}; "
                  f"probe={latency:.2f} ms; {detail}", flush=True)
            if ok:
                healthy.append((latency, server))
        healthy.sort(key=lambda item: item[0])
        return [server for _, server in healthy]

    def handle_client(self, client, address):
        with client:
            client.settimeout(self.timeout)
            try:
                request = client.recv(4096).decode("utf-8", errors="replace").strip()
                if not request:
                    return
                if request.startswith("GET "):
                    pass
                elif request in ("file1", "file2", "file3"):
                    request = "GET " + request
                else:
                    client.sendall(b"Invalid request. Use file1, file2, file3 or GET <file>.\n")
                    return

                candidates = self.healthy_backends()
                if not candidates:
                    client.sendall(b"No content servers are currently available.\n")
                    print(f"[REQUEST] {address}: no healthy backend", flush=True)
                    return

                errors = []
                for server in candidates:
                    try:
                        response, elapsed = exchange(
                            server["host"], server["port"], request, self.timeout
                        )
                        if response:
                            with self.lock:
                                self.last_selected = server["name"]
                            client.sendall(response.encode("utf-8"))
                            print(f"[SELECT] {server['name']} ({server['host']}:{server['port']}) "
                                  f"served {request!r}; backend time={elapsed:.2f} ms", flush=True)
                            return
                        errors.append(f"{server['name']}: empty response")
                    except OSError as exc:
                        errors.append(f"{server['name']}: {exc}")
                        print(f"[FAILOVER] {server['name']} failed during request; "
                              "trying next healthy backend", flush=True)

                client.sendall(("All backend attempts failed: " + "; ".join(errors)).encode())
            except (OSError, UnicodeError) as exc:
                print(f"[CLIENT ERROR] {address}: {exc}", flush=True)

    def serve(self, listen, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((listen, port))
            listener.listen(50)
            print(f"[GATEWAY] Listening on {listen}:{port}", flush=True)
            print("[GATEWAY] Backend selection: healthy server with lowest HEALTH probe latency", flush=True)
            while True:
                client, address = listener.accept()
                threading.Thread(target=self.handle_client,
                                 args=(client, address), daemon=True).start()


def main():
    parser = argparse.ArgumentParser(description="Smart Content Delivery backend-selection gateway")
    parser.add_argument("--listen", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--servers", required=True,
                        help="Server1=10.0.0.2:5001,Server2=10.0.0.3:5002")
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()
    Gateway(parse_servers(args.servers), args.timeout).serve(args.listen, args.port)


if __name__ == "__main__":
    main()
