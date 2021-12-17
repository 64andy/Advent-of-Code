"""
Day 16.1: Packet Decoder

Oh boy, we're working with parsing, AND bit streams :)
Input is hex, read as bits (big endian, e.g. 01 -> 0, 1)

There are different packet types, But every packet starts
with a 3-bit version, followed by a 3-bit ID.

Packet IDs:
4: Represents literal value.
- Its contents are arbitrary length 5-bit segments,
  with the 1st bit saying if the sequence continue, and
  the remaining 4-bits being the data.
  e.g. 10100 11001 01000 is the sequence 0100 1001 1000

Any other ID: Represents nested operator packets
- If the immediate next bit is '0', then the next 15 bits
  is the total number of bits the subpackets take up
- If the immediate next bit is '1', then the next 11 bits
  are the number of subpackets.

Part 1 question: Parse the packets, and sum up the version numbers.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Union, List


def bit_generator(hexdata):
    for char in hexdata:
        num = int(char, base=16)
        for i in reversed(range(4)):
            bit = (num >> i) & 1
            yield bit


class BitStream:
    def __init__(self, hexdata: str):
        self.stream = bit_generator(hexdata)
        self.n_bits_read = 0

    def read_bit(self) -> int:
        bit = next(self.stream)
        self.n_bits_read += 1
        return bit

    def read_int(self, n_bits) -> int:
        num = 0
        for i in reversed(range(n_bits)):
            bit = self.read_bit()
            num += bit * 2**i
        return num

    def read_str(self, n_bits) -> str:
        return ''.join(str(self.read_bit()) for _ in range(n_bits))

    def read_literal(self) -> int:
        """
        Packets with ID=4 have their data as a sequence of
        5-bit segments. 1st bit is if it's the final segment,
        the remaining 4 are part of the number.

        Reads the stream upto and including the final segment,
        and turns it into an integer.
        """
        binary_string = ""
        terminated = False
        while not terminated:
            segment = self.read_str(5)
            number = segment[1:5]
            if segment[0] == '0':
                terminated = True
            binary_string += number
        return int(binary_string, base=2)


LITERAL_DATA_ID = 4


@dataclass
class Packet:
    id: int
    version: int
    content: "Union[int, List[Packet]]"


def parse_multiple_packets(stream: BitStream) -> List[Packet]:
    packets = []
    length_type_id = stream.read_int(1)
    if length_type_id == 0:
        total_subpacket_length = stream.read_int(15)
        start = current = stream.n_bits_read
        while current - start < total_subpacket_length:
            packets.append(parse_packet(stream))
            current = stream.n_bits_read
    else:
        n_subpackets = stream.read_int(11)
        for _ in range(n_subpackets):
            packets.append(parse_packet(stream))
    return packets


def parse_packet(stream: BitStream) -> Packet:
    version = stream.read_int(3)
    id = stream.read_int(3)
    if id == LITERAL_DATA_ID:
        content = stream.read_literal()
    else:
        content = parse_multiple_packets(stream)
    return Packet(id, version, content)


def sum_packet_versions(packet: Packet) -> int:
    if type(packet.content) is not list:
        return packet.version
    else:
        return packet.version + sum(sum_packet_versions(sub_packet) for sub_packet in packet.content)



p = Path(__file__).with_name("input")

with p.open('r') as file:
    data = file.read().strip()

stream = BitStream(data)
packet = parse_packet(stream)

print(packet)
print(sum_packet_versions(packet))
