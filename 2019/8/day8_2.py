INPUT_FILE = "day8.in"


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


def part1(instructions: list) -> int:
    """
    Returns the final acc value before an instruction is read twice
    ---
    Algorithm logic: Just keep track of PC values, return on repeat
    """
    acc = 0
    pc = 0
    seen_numbers = set()
    while pc not in seen_numbers:
        seen_numbers.add(pc)
        acc, pc = execute_instruction(instructions[pc], acc, pc)
    return acc


def execute_program(instructions: list) -> int:
    """
    Takes instructions, returns acc if correctly executed.
    Raises `IndexError` if invalid (loop or out-of-bounds)
    """
    acc = 0
    pc = 0
    seen_numbers = set()
    while True:
        if pc in seen_numbers:
            raise ValueError(f"{pc} has been executed twice")
        if not (0 <= pc <= len(instructions)):
            raise ValueError(
                f"{pc} has flown out of bounds [0, {len(instructions)})")
        if pc == len(instructions):
            print(pc, "has reached the end cleanly")
            break
        seen_numbers.add(pc)
        acc, pc = execute_instruction(instructions[pc], acc, pc)
    return acc


def part2(commands: list) -> int:
    """
    Terminating on a repeat instruction is bad actually,
    one nop/jmp has been replaced by a jmp/nop
    Returns the final acc value of a *fixed* instruction set.
    ---
    A working program ends when the program counter reaches one beyond
    the final instruction.

    e.g. list[10] instructions, list[9] is the last index,
    so terminate when PC == 10
    ---
    Algorithm logic: Just run the program with replaced nop/jmps until
    it works
    """
    commands = commands.copy()
    for i, (cmd, val) in enumerate(commands):
        if cmd not in ('nop', 'jmp'):
            continue
        commands[i] = (('nop' if cmd == 'jmp' else 'jmp'), val)
        try:
            acc = execute_program(commands)
            return acc
        except ValueError as e:
            print(i, '|', e)
            commands[i] = (cmd, val)

    raise ValueError("Valid program not found")


def main():
    acc = 0
    pc = 0
    instructions = []
    with open(INPUT_FILE, 'r') as file:
        for line in file:
            cmd, val = line.split(' ', maxsplit=1)
            instructions.append((cmd, int(val)))

    # part1(instructions)
    print(part2(instructions))


if __name__ == "__main__":
    main()
