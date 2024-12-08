namespace AdventOfCode2024.src.Day05;

/// <summary>
/// We're given two types of input, separated by a blank line.
/// 1. A list of "ordering rules", with two numbers separated by a pipe
///     e.g. "5|7"
/// 2. A list of "updates", which are comma-separated numbers.
///     e.g. "5,6,7,8"
/// </summary>
class Day05 : ISolution
{
    public int GetDay() => 5;

    /// <summary>
    /// <para>
    /// Gets the "ordering rules", formatted as a one-to-many mapping of every
    ///   LHS to RHS pairing
    /// </para>
    /// e.g. <c>"1|2 \n 1|3 \n 2|3" => {1: [2,3], 2: [3]}</c>
    /// </summary>
    private static Dictionary<int, ISet<int>> ParseOrderingRules(string[] input)
    {
        var pairs = input.TakeWhile(line => line.Length > 0)
                            .Select(line => line.Split('|'));

        Dictionary<int, ISet<int>> mapping = [];
        foreach (var pair in pairs)
        {
            int left = int.Parse(pair[0]);
            int right = int.Parse(pair[1]);
            if (mapping.TryGetValue(left, out var entry))
            {
                entry.Add(right);
            }
            else
            {
                mapping.Add(left, new HashSet<int>([right]));
            }
        }
        return mapping;
    }

    /// <summary>
    /// Gets the "updates" at the end of the input, parsed into numbers lists
    /// </summary>
    private static List<List<int>> ParseUpdates(string[] input)
        => input.SkipWhile(line => line.Length > 0)     // Go to the "blank line" separator
                .Skip(1)                                // Ignore the blank line
                // Convert each line into list of nums
                .Select(line => line.Split(','))
                .Select(line => line.Select(int.Parse))
                .Select(line => line.ToList())
                .ToList();

    /// <summary>
    /// Checks if the given line matches the ordering specified
    /// </summary>
    /// <param name="update">The input line we're validating</param>
    /// <param name="rules">The ordering rules</param>
    /// <returns>true if the update follows the rules</returns>
    private static bool IsValidUpdate(IEnumerable<int> update, Dictionary<int, ISet<int>> rules)
    {
        /* Logic:
            Iterate through the list, keeping track of what numbers we've already seen.
            Each time, check what numbers should come after the current number.
            If any of the numbers that should come after have already been seen, it's wrong.
           Note:
            There is no extrapolation, we simply check the mapping directly.
            e.g. if "1|2" & "2,1" are inputs, first step adds '2' to `seen`,
            second step violates the rules as `2` is in `seen`
        */
        HashSet<int> seen = [];
        foreach (int num in update)
        {
            if (rules.TryGetValue(num, out var after) && after.Intersect(seen).Any())
            {
                return false;
            }
            seen.Add(num);
        }

        return true;
    }

    /// <summary>
    /// Page ordering rules specify that the LHS number must appear before the RHS.
    ///   e.g. "5|7" means "5,6,7" is good, "7,6,5" is wrong.
    /// We must find all of the "updates" which comply with the ordering rules, and
    /// to prove we found it, get the number in the middle of it.
    ///   e.g. "3,4,5" -> 4
    /// </summary>
    /// <returns>The sum of each middle number of the "valid" updates</returns>
    public string Part1(string[] input)
    {
        var mapping = ParseOrderingRules(input);

        return ParseUpdates(input)
                .Where(update => IsValidUpdate(update, mapping))
                .Select(update => update[update.Count / 2])
                .Sum()
                .ToString();
    }

    public string Part2(string[] input)
    {
        return "INCOMPLETE";
    }
}