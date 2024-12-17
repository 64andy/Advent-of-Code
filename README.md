### Advent of Code - 2019-2024 Solutions (Incomplete)
---

This repository, written in Python (2019-2023) and C# (2024), contains my solutions to AoC's challenges.


#### How to run:
- Python:
  - Simply execute the desired Python file
- C#:
  - `cd` to the relevant year folder (i.e. `/2024/`), execute `dotnet run`, then enter the day number you want to run


#### Structure:
- Each year has its own folder, and each day has a subfolder
- Python: `{year}/{day}`
  - Each 'day' folder contains:
    - `1_answer.py` - The Part 1 solution
    - `2_answer.py` - The Part 2 solution
    - `test_input` - A sample input given in the question's examples 
    - `input` - The problem's actual input
  - To create a solution, create a new folder with this structure, and use [`template.py`](./template.py) as your answer's template.
  - To switch between `test_input` and `input`, change which file is read at the top of the program.
- C#: `{year}/src/{day}`
  - Each 'day' folder contains:
    - `Day{day}.cs` - The Part 1 & 2 solution
    - `test_input` - A sample input given in the question's examples 
    - `input` - The problem's actual input
  - To create a solution, create a new folder with this structure, and ensure your solution implements [`ISolution`](./2024/src/ISolution.cs).
  - It will run either `test_input` or `input` depending on which is present. If both are present, it defaults to `input`. To switch, rename `input`

**Please Note**: This is __not__ a full answer list of every year, I usually stop before reaching the end.
