namespace AdventOfCode2024.src.Day10;

/// <summary>
/// Input: A 2D grid of digits from 0-9
/// e.g.
/// 0123
/// 7654
/// 8911
/// </summary>
class Day10 : ISolution
{
    public int GetDay() => 10;

    /// <summary>
    /// Searches the 2D matrix input for the given target, yielding their positions. 
    /// </summary>
    /// <param name="input">Puzzle input</param>
    /// <returns>An enumerable of (i, j) coordinates</returns>
    private static IEnumerable<(int, int)> FindCoordsOfEveryOccurance(string[] input, char target)
    {
        for (int i = 0; i < input.Length; i++)
            for (int j = 0; j < input[i].Length; j++)
                if (input[i][j] == target)
                    yield return (i, j);
    }

    /// <summary>
    /// Looks at the 4 cardinal neighbours. If they are 1 bigger than the current digit,
    /// it yields their coordinates
    /// </summary>
    /// <returns>An enumerable of (i, j) coordinates</returns>
    private static IEnumerable<(int, int)> FindNextStepsAscending(string[] input, (int, int) currPos)
    {
        var (ci, cj) = currPos;
        char currVal = input[ci][cj];
        // Look one space up, down, left, right
        (int, int)[] directions = [(ci - 1, cj), (ci + 1, cj), (ci, cj - 1), (ci, cj + 1)];
        foreach (var (i, j) in directions)
            // In-bounds?
            if (i >= 0 && i < input.Length && j >= 0 && j < input[i].Length)
                // Ascending?
                if (input[i][j] == currVal + 1)
                    yield return (i, j);
    }

    /// <summary>
    /// Returns <c>true</c> if we've reached the goal.
    /// </summary>
    private static bool IsGoal(string[] input, (int, int) pos)
    {
        var (i, j) = pos;
        return input[i][j] == '9';
    }

    private enum WeAreCounting : byte { Paths, Goals };

    /// <summary>
    /// A standard path-searching algorithm.
    /// Returns the number of 9s we can reach from the given pos
    /// </summary>
    /// <param name="input">Puzzle input</param>
    /// <param name="start">Starting point</param>
    /// <param name="logic">
    ///     Determines if we're counting the number of goals reached (Part 1)
    ///     or the number of paths to get there (Part 2)
    /// </param>
    private static int FindNumPaths(string[] input, (int, int) start, WeAreCounting logic)
    {
        int numGoalsFound = 0;

        HashSet<(int, int)> visited = [];
        Queue<(int, int)> frontier = new([start]);
        while (frontier.Count > 0)
        {
            var pos = frontier.Dequeue();
            if (visited.Contains(pos) && logic == WeAreCounting.Goals)
                continue;
            if (IsGoal(input, pos))
                numGoalsFound++;
            else
                foreach (var next in FindNextStepsAscending(input, pos))
                    frontier.Enqueue(next);

            visited.Add(pos);
        }

        return numGoalsFound;
    }

    /// <summary>
    /// In our grid of digits, we start at a given '0', with the goal of reaching '9's.
    /// We can only move one step at a time in the 4 cardinal directions, and only to a
    ///   neighbour with a digit one larger than our current digit. (0>1>2>3...)
    /// For each starting point, we keep count of how many '9's we can reach.
    /// </summary>
    /// <returns>The sum of how many goals each start-point can reach</returns>
    public string Part1(string[] input)
    {
        return FindCoordsOfEveryOccurance(input, '0')
                .Select(s => FindNumPaths(input, s, WeAreCounting.Goals))
                .Sum()
                .ToString();
    }

    /// <summary>
    /// Now instead of exclusively counting how many individual goals each start can
    ///   reach, now we count how many paths it can go down to reach any goal.
    /// </summary>
    /// <returns>The sum of how many paths a start-point can go to reach a '9'</returns>
    public string Part2(string[] input)
    {
        // From a logic standpoint, the only difference is that we no longer ignore
        // nodes we've already visited.
        // This is safe, as "paths" can't be cyclic
        return FindCoordsOfEveryOccurance(input, '0')
                .Select(s => FindNumPaths(input, s, WeAreCounting.Paths))
                .Sum()
                .ToString();
    }
}
