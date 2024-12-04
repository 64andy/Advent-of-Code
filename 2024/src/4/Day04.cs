namespace AdventOfCode2024.src.Day04;
class Day04 : ISolution
{
    public int GetDay() => 4;

    private static bool FindWordInDirection(string[] grid, string needle, (int, int) startPos, (int, int) direction)
    {
        var (i, j) = startPos;
        var (di, dj) = direction;

        try
        {
            foreach (char c in needle)
            {
                if (grid[i][j] != c) return false;
                i += di;
                j += dj;
            }
        }
        catch (IndexOutOfRangeException)
        {
            return false;
        }

        return true;
    }

    public string Part1(string[] input)
    {
        (int, int)[] directions = [
            (-1, 0), (+1, 0), (0, -1), (0, +1),     // Up, Down, Left, Right
            (-1, -1), (+1, -1), (-1, +1), (+1, +1)  // Diagonals
        ];
        int total = 0;
        for (int i = 0; i < input.Length; i++)
        {
            for (int j = 0; j < input[i].Length; j++)
            {
                total += directions
                        .Select(dir => FindWordInDirection(input, "XMAS", (i, j), dir))
                        .Select(b => b ? 1 : 0)
                        .Sum();
            }
        }

        return total.ToString();
    }

    public string Part2(string[] input)
    {
        return "UNIMPLEMENTED";
    }
}
