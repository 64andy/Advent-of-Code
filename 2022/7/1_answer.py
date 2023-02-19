"""
NOTE: Requires Python 3.9+
Day 7.1 - No Space Left On Device

Input:
Commands and their outputs of a bash-like terminal.
- Lines starting with '$ ' are commands
- All the following non-command lines are that command's output:
- - `$ cd <dir>` changes the current directory
- - - ('..' moves up, '/' moves to root, other names move to the named subdirectory)
- - `$ ls` lists this directory's contents
- - - `dir <name>` represents a subdirectory
- - - `<int> <name>` represents a file with a size
e.g. ```
  $ ls
  100 a.ext
  342 doc
  dir x
  $ cd /
```

Logic:
These commands are used to build a directory structure (containing files and sub-directories).
The 'size' of a directory is the sum of its files, **plus the size of its subdirectories, recursively**

Output:
In Part 1, we ignore directories with a size larger than 100 000.
Sum the total size of every directory smaller than 100 000
[REMINDER: A directory's size counts its subdirectories sizes, so you can repeatedly count the same files]

Example:
/a:
  50 cheese.txt
  /a/b:
    100 burger.jpg
The size of `/a/b` is 100, the size of `/a` is (50 + `/a/b`) = 150.
The sum of all directories would be 250 (burger.jpg is counted twice)
...
"""

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, List, Optional, TextIO
p = Path(__file__).with_name("input")

# Vars
CMD_LS_PATTERN = r"\$ ls"
CMD_CD_PATTERN = r"\$ cd (.+)"
OUT_FILE_PATTERN = r"(\d+) (.+)"
OUT_DIR_PATTERN = r"dir (.+)"


@dataclass
class File:
    """
    Represents a line of output from `ls`
    """
    name: str
    size: int

    def pprint(self, indent=0):
        """
        Format: <indent_spaces>- <name> (file, size=<size>)
        Example: "  - i (file, size=55)"
        """
        return f"{' '*indent}- {self.name} (file, size={self.size})"


@dataclass
class LSOutput:
    files: List[File]
    dir_names: List[str]


@dataclass
class Command:
    name: str                   # Command name (`ls` or `cd`)
    # Any data associated with a command (`cd` only)
    arg: Optional[str]
    data: Optional[LSOutput]    # The output of a command (`ls` only)


@dataclass
class Directory:
    """
    A pseudo-directory. Has a name, contains files and subdirectories.
    """
    parent: "Directory"
    name: str
    sub_dirs: "Dict[str, Directory]"
    files: List[File]

    def _empty_child(self, dir_name: str) -> "Directory":
        return Directory(parent=self, name=dir_name, sub_dirs={}, files=[])
    
    @staticmethod
    def create_root_node():
        return Directory(parent=None, name="/", sub_dirs={}, files=[])


    def populate_from_ls_output(self, out: LSOutput):
        self.sub_dirs.update({name: self._empty_child(name) for name in out.dir_names})
        self.files.extend(out.files)

    def cd(self, dir_name: str) -> "Directory":
        """
        Returns the subdirectory of the given name:
        - If the name is '..', it returns the parent
        - If the name is '/', it'll recursively find the root
        If it doesn't exist, it creates one.
        """
        if dir_name == "/":
            directory = self
            while directory.parent is not None:
                directory = directory.parent
            return directory

        if dir_name == "..":
            return self.parent

        if dir_name not in self.sub_dirs:
            directory = self._empty_child(dir_name)
            self.sub_dirs[dir_name] = directory
        else:
            directory = self.sub_dirs[dir_name]
        return directory
    
    def size(self) -> int:
        """
        Returns the size of this directory's files, and all sub directories, recursively
        """
        n = sum(x.size for x in self.files)
        n += sum(d.size() for d in self.sub_dirs.values())
        return n
    
    def pprint(self, indent=0):
        out_lines = []
        out_lines.append("{}- {} (dir)".format(" "*indent, self.name))
        out_lines.extend(d.pprint(indent+2) for d in self.sub_dirs.values())
        out_lines.extend(f.pprint(indent+2) for f in self.files)

        return "\n".join(out_lines)


# Funcs
def parse_into_commands_and_data(file: TextIO) -> List[Command]:
    commands: List[Command] = []
    for line in file:
        line = line.strip()

        if (m := re.match(CMD_CD_PATTERN, line)):
            # $ cd <dir_name>
            dir_name = m.group(1)
            commands.append(Command("cd", dir_name, None))
        elif (m := re.match(CMD_LS_PATTERN, line)):
            # $ ls
            commands.append(Command("ls", None, LSOutput([], [])))
        elif (m := re.match(OUT_FILE_PATTERN, line)):
            # <size> <filename>
            size, name = m.groups()
            commands[-1].data.files.append(File(name, int(size)))
        elif (m := re.match(OUT_DIR_PATTERN, line)):
            # dir <dir_name>
            dir_name = m.group(1)
            commands[-1].data.dir_names.append(dir_name)
        else:
            raise Exception("Unknown input: " + repr(line))
    return commands

def pt1_size_below_max(directory: Directory) -> int:
    MAX = 100_000
    size = directory.size()
    if size > MAX:
        size = 0
    return size + sum(pt1_size_below_max(subdir) for subdir in directory.sub_dirs.values())

def main():
    file_system = Directory.create_root_node()
    with p.open('r') as file:
        commands = parse_into_commands_and_data(file)

    for cmd in commands:
        if cmd.name == "cd":
            file_system = file_system.cd(cmd.arg)
        elif cmd.name == "ls":
            file_system.populate_from_ls_output(cmd.data)

    file_system = file_system.cd("/")
    print("Total size:", file_system.size())
    print("Size below the 100000 limit:", pt1_size_below_max(file_system))





if __name__ == "__main__":
    main()
