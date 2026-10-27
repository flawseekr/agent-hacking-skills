#!/usr/bin/env python3

"""Send an HTTP request and print the result as a single JSON object.

Arguments:
    -X METHOD     HTTP method (default: GET).
    -u URL        Full endpoint URL.
    -H HEADER     Request header "Name: value" (repeatable).
    --data DATA   Request body.
"""

import sys
import json
import socket
import ssl
import argparse
from urllib.parse import urlsplit

TIMEOUT = 30
RECV_SIZE = 65536

def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        description="Send an HTTP request and print the result as JSON."
    )
    parser.add_argument("-X", dest="method", default="GET", help="HTTP method")
    parser.add_argument("-u", dest="url", required=True, help="Full endpoint URL")
    parser.add_argument(
        "-H",
        dest="headers",
        action="append",
        default=[],
        metavar="HEADER",
        help="Request header 'Name: value' (repeatable)",
    )
    parser.add_argument("--data", dest="data", default=None, help="Request body")
    return parser.parse_args(argv)

def parse_header(raw):
    """Split a "Name: value" header string into a (name, value) pair."""
    name, sep, value = raw.partition(":")
    if not sep:
        raise ValueError(f"invalid header, missing ':' -> {raw!r}")
    return name.strip(), value.strip()

def split_url(url):
    """Parse a URL into its components, defaulting the scheme to https."""
    if "://" not in url:
        url = "https://" + url
    split = urlsplit(url)
    if not split.hostname:
        raise ValueError(f"invalid URL, missing host -> {url!r}")

    scheme = split.scheme.lower()
    host = split.hostname
    port = split.port or (443 if scheme == "https" else 80)
    path = split.path or "/"
    # Host header reflects the authority as given, minus any userinfo.
    host_header = split.netloc.rsplit("@", 1)[-1]
    return scheme, host, port, path, split.query, host_header

def build_request_lines(method, request_target, host_header, headers, data):
    """Build the ordered request lines (status line + headers)."""
    present = {name.lower() for name, _ in headers}
    lines = [f"{method} {request_target} HTTP/1.1"]

    if "host" not in present:
        lines.append(f"Host: {host_header}")
    for name, value in headers:
        lines.append(f"{name}: {value}")
    if data is not None and "content-length" not in present:
        lines.append(f"Content-Length: {len(data.encode())}")
    if "connection" not in present:
        lines.append("Connection: close")
    return lines

def send_request(scheme, host, port, wire):
    """Open a connection, send the raw request, and return the raw response bytes."""
    sock = socket.create_connection((host, port), timeout=TIMEOUT)
    try:
        sock.settimeout(TIMEOUT)
        if scheme == "https":
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = context.wrap_socket(sock, server_hostname=host)

        sock.sendall(wire)

        chunks = []
        while True:
            try:
                data = sock.recv(RECV_SIZE)
            except socket.timeout:
                break
            if not data:
                break
            chunks.append(data)
        return b"".join(chunks)
    finally:
        sock.close()

def parse_response_head(head):
    """Return (status_code, content_type) parsed from the response head bytes."""
    lines = head.decode("iso-8859-1").split("\r\n")

    status_code = None
    status_parts = lines[0].split(" ", 2)
    if len(status_parts) >= 2 and status_parts[1].isdigit():
        status_code = int(status_parts[1])

    content_type = None
    for line in lines[1:]:
        name, sep, value = line.partition(":")
        if sep and name.strip().lower() == "content-type":
            content_type = value.strip().split(";")[0].strip().lower()
            break

    return status_code, content_type

def main(argv):
    args = parse_arguments(argv)

    headers = [parse_header(h) for h in args.headers]
    scheme, host, port, path, query, host_header = split_url(args.url)

    request_target = path + ("?" + query if query else "")
    lines = build_request_lines(
        args.method, request_target, host_header, headers, args.data
    )

    body_bytes = args.data.encode() if args.data is not None else b""
    wire = ("\r\n".join(lines) + "\r\n\r\n").encode() + body_bytes
    raw_request = "\n".join(lines) + "\n\n" + (args.data or "")

    raw = send_request(scheme, host, port, wire)

    separator = raw.find(b"\r\n\r\n")
    if separator == -1:
        head, response_body = raw, b""
    else:
        head, response_body = raw[:separator], raw[separator + 4:]

    status_code, content_type = parse_response_head(head)
    raw_response = raw.decode("utf-8", errors="replace").replace("\r\n", "\n")

    result = {
        "endpoint": f"{args.method} {scheme}://{host_header}{path}",
        "query_string": query or None,
        "content_type": content_type,
        "status_code": status_code,
        "response_size_bytes": len(response_body),
        "raw_request": raw_request,
        "raw_response": raw_response,
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
