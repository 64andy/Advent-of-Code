INPUT_FILE = "day8test.in"

def execute_instruction(instruction: (str, int), acc: int, pc: int) -> (int, int):
    """
    Reads the given instruction and returns the new (acc, pc)
    ### Input:
    instruction: A 2-tuple of (instruction_name, value) e.g. ('jmp', +99)
    acc: int, The current running "sum", modified by the "acc" instruction
    pc: int, The program counter, automatically incremented, modified further by "jmp"
    ### Returns:
    2-tuple representing the new (acc, pc) after the instruction's been executed
    """
    cmd, val = instruction
    if cmd == 'jmp':
        pc += val - 1   # -1 because the auto-increment won't apply
    elif cmd == 'acc':
        acc += val
    elif cmd == 'nop':
        pass
    pc += 1         # Incremented after each instruction
    return (acc, pc)


def main():
    acc = 0
    pc = 0
    instructions = []
    with open(INPUT_FILE, 'r') as file:
        for line in file:
            cmd, val = line.split(' ', maxsplit=1)
            instructions.append((cmd, int(val)))
    
    seen_numbers = set()
    while True:
        if pc in seen_numbers:
            raise ValueError(f"{pc} has been executed twice")
        if not (0 <= pc < len(instructions)):
            raise ValueError(f"{pc} has flown out of bounds [0, {len(instructions)})")
        if pc == len(instructions):
            print(pc, "has reached the end cleanly")
            break
        seen_numbers.add(pc)
        print(instructions[pc], end=" -> ")
        acc, pc = execute_instruction(instructions[pc], acc, pc)
        print(instructions[pc], acc, pc)


if __name__ == "__main__":
    main()