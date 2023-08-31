import socket
import struct
import time
import sys
import os

def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            checksum += (data[i] << 8) + data[i + 1]
        else:
            checksum += data[i]
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    return ~checksum & 0xFFFF

def generate_icmp_packet(id, seq_num, data):
    icmp_type = 8  # ICMP Echo Request
    icmp_code = 0
    icmp_id = id
    icmp_seq_num = seq_num

    # Prepare the payload data
    payload_data = bytes([data]) + b'\x00' * 7 + b"!\"#$%&'()*+,-./01234567"

    # Create the ICMP header (without checksum)
    icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, 0, icmp_id, icmp_seq_num)

    # Create the ICMP payload (including timestamp)
    current_time = int(time.time())
    icmp_payload = payload_data + b'\x00' * (48 - len(payload_data)) 

    # Calculate the checksum
    checksum = calculate_checksum(icmp_header + icmp_payload)
    icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, checksum, icmp_id, icmp_seq_num)

    icmp_packet = icmp_header + icmp_payload
    return icmp_packet
    
def send_ping(dest_ip, message):
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
        packet_id = os.getpid() & 0xFFFF
        seq_num = 1  # Starting sequence number
        for char in message:
            icmp_packet = generate_icmp_packet(packet_id, seq_num, ord(char))
            sock.sendto(icmp_packet, (dest_ip, 0))
            seq_num += 1
            print("Sent 1 packet to", dest_ip)
            time.sleep(0.2)  # Wait a short time between packets

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <destination_ip> <message>")
        sys.exit(1)

    destination_ip = sys.argv[1]
    message = sys.argv[2]

    send_ping(destination_ip, message)
