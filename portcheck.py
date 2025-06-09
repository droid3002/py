#!/usr/bin/env python3
"""
Parallel Minecraft port-and-crack scanner
----------------------------------------
∙ Requires:  python-mcstatus  ( pip install mcstatus )
"""
import os
import time
print("Installing MCstatus...")
os.system("pip install mcstatus socket struct argparse sys")

print("Success!")
print("Initializing...")
time.sleep(5)
import socket, struct, argparse, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from mcstatus import JavaServer

# ---------- helpers for the Minecraft protocol ----------

def _varint_encode(value: int) -> bytes:
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        out.append(byte | (0x80 if value else 0))
        if not value:
            return bytes(out)

def _write_string(s: str) -> bytes:
    data = s.encode("utf-8")
    return _varint_encode(len(data)) + data

def _make_packet(pkt_id: int, payload: bytes = b"") -> bytes:
    full = _varint_encode(pkt_id) + payload
    return _varint_encode(len(full)) + full

def _read_varint(sock) -> int:
    num, shift = 0, 0
    while True:
        byte = sock.recv(1)
        if not byte:
            raise EOFError
        val = byte[0]
        num |= (val & 0x7F) << shift
        if not val & 0x80:
            return num
        shift += 7
        if shift >= 35:
            raise RuntimeError("VarInt too big")

# ---------- cracked / premium detector ----------

print("Done init")

def cracked_status(host: str, port: int, timeout: float = 2.0):
    """
    Returns:
        True   → server at port is offline-mode (cracked)
        False  → server is premium (online-mode)
        None   → port isn't a Java server or gave an unexpected reply
    """
    try:
        status = JavaServer.lookup(f"{host}:{port}", timeout=timeout).status()
        proto = status.version.protocol
    except Exception:
        return None  # not a Minecraft Java status response

    try:
        s = socket.create_connection((host, port), timeout)
        # handshake (state 2 → LOGIN)
        hs = (_varint_encode(proto)
              + _write_string(host)
              + struct.pack(">H", port)
              + _varint_encode(2))
        s.sendall(_make_packet(0x00, hs))
        # login-start with dummy name
        s.sendall(_make_packet(0x00, _write_string("PortCheck")))
        # read first response header
        _read_varint(s)          # length (ignored)
        pid = _read_varint(s)    # packet id
        s.close()
        # pid 0x01 = Encryption Request  → premium
        # pid 0x02 or 0x03 appear before encryption in offline mode
        if pid == 0x01:
            return False
        elif pid in (0x02, 0x03):
            return True
    except Exception:
        pass
    return None

# ---------- port scanner ----------

def scan_port(host: str, port: int, timeout: float = 0.6):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
        except Exception:
            return None  # closed / filtered
    cracked = cracked_status(host, port)
    return port, cracked

def main():
    ap = argparse.ArgumentParser(
        description="Parallel Minecraft port & cracked scanner")
    ap.add_argument("host", help="hostname or IP to scan")
    ap.add_argument("start", type=int, help="start port (inclusive)")
    ap.add_argument("end",   type=int, help="end port   (inclusive)")
    ap.add_argument("-t", "--threads", type=int, default=300,
                    help="max parallel workers (default 300)")
    args = ap.parse_args()

    if not (1 <= args.start <= 65535 and 1 <= args.end <= 65535
            and args.start <= args.end):
        ap.error("Port range must be within 1-65535 and start <= end.")

    print(f"Scanning {args.host}:{args.start}-{args.end} "
          f"with up to {args.threads} threads …\n")

    open_ports = []
    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        futures = {ex.submit(scan_port, args.host, p): p
                   for p in range(args.start, args.end + 1)}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                port, cracked = res
                status = {True: "cracked", False: "premium", None: "unknown"}[cracked]
                print(f"● {port:<5}  open   ({status})")
                open_ports.append((port, status))

    if not open_ports:
        print("\nNo open ports found in that range.")
    else:
        print("\nSummary:")
        for port, st in open_ports:
            print(f"  {port}: {st}")

if __name__ == "__main__":
    main()
