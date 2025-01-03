namespace AdventOfCode2024.src.Day07;

/// <summary>
/// Our input is a list of mappings, pairing one number to
/// a list of numbers.
/// e.g. `190: 10 19`
/// </summary>
class Day07 : ISolution
{
    public int GetDay() => 7;

    private static IEnumerable<(long, List<long>)> ParseInput(string[] input)
    => input.Select(line => line.Split(':'))
            .Select(line => (
                        long.Parse(line[0]),
                        line[1].Split(' ', StringSplitOptions.RemoveEmptyEntries)
                            .Select(long.Parse)
                            .ToList()
            ));


    public static bool IsSolvable(long target, IEnumerable<long> nums, Func<long, long, long>[] operations)
    {
        bool SolveRecursive(long current, IEnumerable<long> nums)
        {
            // Base cases
            // If we've reached the target, it's solved
            if (!nums.Any())
                return current == target;
            // If we've overshot the number, we're in a doomed timeline
            if (current > target)
                return false;
            // Consume the next number
            var next = nums.First();
            nums = nums.Skip(1);

            return operations.Any(f => SolveRecursive(f(current, next), nums));
        }
        return SolveRecursive(nums.First(), nums.Skip(1));
    }

    /// <summary>
    /// Each row represents an equation, where the LHS is the result,
    /// and the RHS list of nums are the numbers to reach it.
    /// In-between each number is either an add or multiply operator.
    /// This equation is strictly evaluated left-to-right (no PEDMAS).
    /// What equations are possible to solve given these rules?
    /// </summary>
    /// <returns>The sum of every solvable equation's LHS</returns>
    public string Part1(string[] input)
    {
        Func<long, long, long>[] operations = [
            (a, b) => a+b,  // Add
            (a, b) => a*b   // Multiply
        ];
        return ParseInput(input)
                .AsParallel()
                .Where(p => IsSolvable(p.Item1, p.Item2, operations))
                .Select(p => p.Item1)
                .Sum()
                .ToString();
    }

    public string Part2(string[] input)
    {
        Func<long, long, long>[] operations = [
            (a, b) => a+b,  // Add
            (a, b) => a*b,  // Multiply
            (a, b) => long.Parse(a.ToString() + b.ToString())   // Concat
        ];
        return ParseInput(input)
                .AsParallel()
                .Where(p => IsSolvable(p.Item1, p.Item2, operations))
                .Select(p => p.Item1)
                .Sum()
                .ToString();
    }
}