"""
NOTE: Requires Python 3.9+
Day 7.2 - No Space Left On Device

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
In Part 2, we need to delete a directory to make space.
We have a disk with a maximum size of 70 000 000, and we need 30 000 000 of free space.
What is the smallest single directory we can delete to free up enough space?
...
"""

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, Iterable, List, Optional, TextIO
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
    
    def walk(self) -> "Iterable[Directory]":
        yield self
        for subdir in self.sub_dirs.values():
            yield from subdir.walk()
    
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

def pt2_delete_smallest_dir(root: Directory) -> int:
    TOTAL_SPACE = 70_000_000
    FREE_SPACE_NEEDED = 30_000_000
    free_space = TOTAL_SPACE - root.size()
    return min((d for d in root.walk() if d.size() + free_space >= FREE_SPACE_NEEDED), key=Directory.size)
    

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
    smallest_dir = pt2_delete_smallest_dir(file_system)
    print("Smallest directory that can be deleted:", smallest_dir)
    print("Size of smallest dir:", smallest_dir.size())





if __name__ == "__main__":
    main()
