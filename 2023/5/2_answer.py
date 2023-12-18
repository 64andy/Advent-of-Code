"""
Day 5.2 - If You Give A Seed A Fertilizer 

Python 3.9+

Input:
  Firstly, a space-separated list of 2-pair seed ranges
    e.g. "seeds: 1 2 3 4 5 6"
  Afterwards, there is a list of mappings, starting with the text "x-to-y map:",
    followed by 3-pairs of numbers, and terminated by a blank line.
    (See the input files as examples, it's easier to just see)

Logic:
  New in Part Two: The seeds line are actually a list of 2-pair ranges.
  So, "seeds: 1 2 11 4" is [(1, 2), (11, 4)].
  Each (start, length) pair represents a range of seeds between [start, start+length)
  Example: (11, 4) represents the seeds [11, 12, 13, 14]

  Every "a-to-b" conversion has a list of 3-pair numbers.
  These numbers represent a mapping, and show the:
  - Destination range start
  - Source range start (the ordering is unintuitive I know)
  - Range length
  This means that all numbers in [src_start, src_start+length) map to the same offset
  in [dest_start, dest_start+length).
  Example:
    "11 1 5" means that the numbers in [1, 6) map to the numbers in [11, 16).
    Thus 1->11, 2->12, 3->13, 4->14, and 5->15
  If your source number doesn't have any mapping, it maps to itself.
  

Output:
  Each seed, after feeding it all the way through, will give a location number.
  What is the lowest location number from any of the seeds
"""

import dataclasses
from pathlib import Path
from typing import Iterator

p = Path(__file__).with_name("input")

# Vars
ORDER = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
]


# Classes

@dataclasses.dataclass(frozen=True)
class MappingInfo:
    src_range: range
    dest_range: range
    
    def map_number(self, other: int) -> int:
        """
        If the given number is within this mapping's range, returns the mapped value.

        Otherwise, it returns itself
        """
        if other in self.src_range:
            pos = self.src_range.index(other)
            return self.dest_range[pos]
        else:
            return other


@dataclasses.dataclass
class ParsedFile:
    seeds: list[int]
    all_mappings: dict[str, list[MappingInfo]]

    @staticmethod
    def parse(file: Iterator[str]) -> 'ParsedFile':
        file_lines = iter(file)

        # Firstly, handle the seeds
        seeds_line = next(file_lines).strip().removeprefix("seeds: ")
        seeds = [int(seed) for seed in seeds_line.split()]
        next(file_lines)    # Skip the blank line

        # Then, handle the mappings
        mappings = ParsedFile.__parse_all_mappings(file_lines)

        return ParsedFile(seeds, mappings)

    @staticmethod
    def __parse_next_mapping(input: Iterator[str]) -> tuple[str, list[MappingInfo]]:
        mapping = []
        header = next(input).strip().removesuffix(" map:")
        for line in input:
            line = line.strip()
            if len(line) == 0:
                break
            dst, src, length = map(int, line.split())
            mapping.append(MappingInfo(
                src_range=range(src, src+length),
                dest_range=range(dst, dst+length)
            ))
        return (header, mapping)
        
    @staticmethod
    def __parse_all_mappings(input: Iterator[str]) -> dict[str, list[MappingInfo]]:
        """
        Consumes the input for as long as it can
        """
        all_mappings = {}
        try:
            while True:
                type_of_mapping, mapping = ParsedFile.__parse_next_mapping(input)
                all_mappings[type_of_mapping] = mapping
        except StopIteration:
            return all_mappings
        

# Funcs
def flatten_mapping(a_to_b: list[MappingInfo], b_to_c: list[MappingInfo]) -> list[MappingInfo]:
    """
    Collapses a mapping from a->b, and a mapping from b->c, into a mapping from a->b->c.

    If we collapse the entire mapping chain, we can throw a number from the first->last mapping in one step
    """
    a_to_b.sort(key=lambda mi: mi.dest_range.start)
    b_to_c.sort(key=lambda mi: mi.src_range.start)

    # ! INCOMPLETE !
    r"""
    How do we figure this out?
test_input: seed-to-soil + soil-to-fertilizer: 
A>B [98, 100) => [50, 52)
A>B [50, 98)  => [52, 100)
B>C              [15, 52) => [0, 37)
B>C              [52, 54) => [37, 39)
B>C              [0, 15)  => [39, 54)

Merge & Sort by B.first:
B>C              [0, 15)  => [39, 54)
B>C              [15, 52) => [0, 37)
A>B [98, 100) => [50, 52)
A>B [50, 98)  => [52, 100)
B>C              [52, 54) => [37, 39)

Go through each individually:
1.           [0, 15)  => [39, 54)
             No overlap, kept unchanged

2.           [15, 52) => [0, 37)
             No overlap, kept unchanged

3.
[98, 100) => [50, 52)
Overlaps (fully subset) with mapping #2, so it gets turned into:
- [98, 100) => [50, 52) ~> [37, 39)

4.
[50, 98)  => [52, 100)
Overlaps with mapping #5, but only partially, so it gets split up:
- [50, 52) => [52, 54)  # Split the original mapping
- [52, 54) => [37, 39)  # From mapping #5   (duplicate of 5, do we keep it?)
- [54, 98) => [56, 100) # Split the original mapping 

5.
             [52, 54) => [37, 39)
             Overlaps (fully subset) with mapping #4, but it's a B->C mapping so idc

Final mapping:
             [0, 15)  => [39, 54)   #1
             [15, 52) => [0, 37)    #2
[98, 100) ~> [37, 39)               #3
[50, 52)  ~> [52, 54)               #4
[52, 54)  ~> [37, 39)
[54, 98)  ~> [56, 100)
             [52, 54) => [37, 39)   #5

"""


# =====
def passthrough(value, a, b):     
    first_val = a.map_number(value)
    return b.map_number(first_val)
x = MappingInfo(range(4, 6), range(11, 13))
y = MappingInfo(range(4, 9), range(20, 25))
def main():
    # # Firstly, parse the file
    # with p.open('r') as file:
    #     parsed_file = ParsedFile.parse(file)

    for i in range(16):
      val = passthrough(i, x, y)
      print(i, "->", val, "!"*(val!=i))


if __name__ == "__main__":
    main()
