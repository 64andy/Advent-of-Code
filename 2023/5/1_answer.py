"""
Day 5.1 - If You Give A Seed A Fertilizer 

Python 3.9+

Input:
  Firstly, a space-separated list of seeds
    e.g. "seeds: 1 2 3 4 5"
  Afterwards, there is a list of mappings, starting with the text "x-to-y map:",
    followed by 3-pairs of numbers, and terminated by a blank line.
    (See the input files as examples, it's easier to just see)

Logic:
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
from typing import Iterator, Optional

p = Path(__file__).with_name("test_input")

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

@dataclasses.dataclass
class MappingInfo:
    dest_start: int
    src_start: int
    length: int

    
    def map_number(self, other: int) -> Optional[int]:
        """
        If the given number is within this mapping's range, returns the mapped value.

        Otherwise, it returns None
        """
        if self.src_start <= other < self.src_start+self.length:    # If it maps to this
            delta = other - self.src_start
            return self.dest_start + delta
        else:
            return None


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
            a, b, c = map(int, line.split())
            mapping.append(MappingInfo(a, b, c))
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
def handle_mapping_stage(value: int, mapping: list[MappingInfo]) -> int:
    """
    Runs the number through this stage of the mapping.
    """
    for mapping_info in mapping:
        outcome = mapping_info.map_number(value)
        if outcome is not None:
            return outcome
    
    # No mapping exists, therefore it maps to itself
    return value
    

def follow_the_mapping_chain(
        value: int,
        mapping: dict[str, list[MappingInfo]],
        order: list[str]
        ) -> int:
    """
    Takes the `input_num`, runs every step in `order` through `mapping`,
    then returns the result 
    """
    for stage in order:
        value = handle_mapping_stage(value, mapping[stage])
    return value


# =====

def main():
    # Firstly, parse the file
    with p.open('r') as file:
        parsed_file = ParsedFile.parse(file)

    # Feed every seed through the machine, and get the smallest output
    smallest_location = min(
        follow_the_mapping_chain(seed, parsed_file.all_mappings, ORDER)
          for seed in parsed_file.seeds
    )
    print("Smallest location:", smallest_location)

if __name__ == "__main__":
    main()
