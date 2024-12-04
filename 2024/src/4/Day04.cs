namespace AdventOfCode2024.src.Day04;

/// <summary>
/// Our input is a grid of characters, all of them either 'X', 'M', 'A', or 'S'
/// </summary>
class Day04 : ISolution
{
    public int GetDay() => 4;

    /// <summary>
    /// Check if we can find the <c>needle</c> in the <c>grid</c> by moving in a given <c>direction</c> from <c>startPos</c>
    /// </summary>
    /// <param name="grid">The grid of all letters</param>
    /// <param name="needle">The string we're looking for</param>
    /// <param name="startPos">The <c>(i,j)</c> coordinates we start from</param>
    /// <param name="direction">The <c>(i,j)</c> values we add to our coordinates on each step.
    ///                         e.g. (0,1) means we search by moving right, (1,-1) means we look bottom-left...
    /// </param>
    /// <returns><c>true</c> if the needle is in the given position with the given direction</returns>
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

    /// <summary>
    /// In the given list, "XMAS" occurs multiple times.
    /// They can occur horizontally, vertically, and diagonally, both forwards and backwards.
    /// </summary>
    /// <returns>The number of occurances of "XMAS"</returns>
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

    /// <summary>
    /// Checks if "MAS" occurs diagonally in both directions at the given position.
    /// e.g.
    /// M.S
    /// .A.
    /// M.S
    /// 
    /// Warning: There is no bounds checking, this isn't a problem if you
    /// simply don't give coords on the edges of the grid.
    /// </summary>
    private static bool IsMasInACross(string[] grid, int i, int j)
        // Letter in the middle must always be an 'A'
        => grid[i][j] == 'A'
        && (
            // Top-Left & Bottom-Right diagonal check
            grid[i - 1][j - 1] == 'M' && grid[i + 1][j + 1] == 'S'
            || grid[i - 1][j - 1] == 'S' && grid[i + 1][j + 1] == 'M'
        ) && (
            // Bottom-Left & Top-Right diagonal check
            grid[i + 1][j - 1] == 'M' && grid[i - 1][j + 1] == 'S'
            || grid[i + 1][j - 1] == 'S' && grid[i - 1][j + 1] == 'M'
        );

    /// <summary>
    /// Turns out "XMAS" is "MAS in an X shape"; where "MAS" occurs diagonally both ways
    /// </summary>
    /// <returns>The number of occurances of "MAS" in an X shape</returns>
    public string Part2(string[] input)
    {
        // Note: We're enumerating indices, however we're staying away from the edges,
        // since they can't be a cross as one of their sides is out of bounds.
        return Enumerable.Range(1, input.Length - 2)
                    // An iterator of all (i,j indices)
                    .SelectMany(i => Enumerable.Range(1, input[i].Length - 2).Select(j => (i, j)))
                    // Is there a cross in this position
                    .Where(t => IsMasInACross(input, t.i, t.j))
                    .Count()
                    .ToString();
    }
}
