namespace AdventOfCode2024.src.Day02;

class Day02 : ISolution
{
    public int GetDay() => 2;

    private static bool IsSafe(int[] level)
    {
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

    public string Part2(string[] input)
    {
        return "INCOMPLETE";
    }
}
