namespace AdventOfCode2024.src.Day02;

/// <summary>
/// We are given a list of reports a.k.a. levels, where each line
/// is a space separated list of numbers
/// </summary>
class Day02 : ISolution
{
    public int GetDay() => 2;

    private static bool IsSafe(int[] level)
    {
        // Note: This would've been easier if I'd converted to deltas
        const int MIN_DIFF = 1;
        const int MAX_DIFF = 3;

        int initialDiff = level[0] - level[1];
        if (Math.Abs(initialDiff) < MIN_DIFF || Math.Abs(initialDiff) > MAX_DIFF)
            return false;

        bool shouldBeAscending = initialDiff > 0;

        for (int i = 1; i < level.Length - 1; i++)
        {
            int diff = level[i] - level[i + 1];
            // Check: Is ascending/descending the same
            if ((diff > 0) != shouldBeAscending) return false;
            // Check: Is the difference too small/large
            if (Math.Abs(diff) < MIN_DIFF || Math.Abs(diff) > MAX_DIFF) return false;
        }

        return true;
    }

    /// <summary>
    /// A report is considered "safe" if all numbers are increasing/decreasing,
    /// AND the difference between each adjacent number is between [1,3] inclusive
    /// </summary>
    /// <returns>The number of "safe" reports</returns>
    public string Part1(string[] input)
    {
        // Step 1: Parse to ints
        int[][] levels = input.Select(line => line.Split(' '))
                        .Select(nums => nums.Select(int.Parse).ToArray())
                        .ToArray();

        int numSafe = 0;
        foreach (var level in levels)
        {
            if (IsSafe(level)) numSafe++;
        }

        return numSafe.ToString();
    }

    /// <summary>
    /// Returns all versions of the level where one item's missing
    /// </summary>
    private static IEnumerable<int[]> AllListsMinusOneElement(int[] level) {
        for (int i=0; i<level.Length; i++) {
            yield return level.Where((_, idx) => idx != i).ToArray();
        }
    }

    /// <summary>
    /// Now we check if the list can be safe, if we remove at most one element
    /// </summary>
    /// <returns>The number of possibly "safe" reports</returns>
    public string Part2(string[] input)
    {
        // Step 1: Parse to ints
        int[][] levels = input.Select(line => line.Split(' '))
                        .Select(nums => nums.Select(int.Parse).ToArray())
                        .ToArray();

        int numSafe = 0;
        foreach (var level in levels)
        {
            if (AllListsMinusOneElement(level).Any(IsSafe)) numSafe++;
        }

        return numSafe.ToString();
    }
}
