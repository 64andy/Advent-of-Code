using System.Text.RegularExpressions;

namespace AdventOfCode2024.src.Day03;

/// <summary>
/// We are given multiple lines of text input, however it has been corrupted.
/// </summary>
class Day03 : ISolution
{
    public int GetDay() => 3;

    /// <summary>
    /// In the text input, we must look for mul(?,?), which is a multiply command.
    /// The pattern is <c>mul({1-3 digit number},{1-3 digit number})</c>, with no spaces or
    /// any other characters in the way e.g. <c>mul(1, 3)</c> is wrong, <c>mul(1,3!)</c> is wrong.
    /// 
    /// For each of these commands we find, multiply the two numbers in them
    /// </summary>
    /// <returns>The sum of every mul(a,b) in the data</returns>
    public string Part1(string[] input)
    {
        Regex pattern = new(@"mul\((\d{1,3}),(\d{1,3})\)", RegexOptions.Compiled);

        return input.SelectMany(line => pattern.Matches(line))      // Flatten from lines of matches to simply all matches
                .Select(m => m.Groups.Values.Skip(1).Take(2))       // The first entry in regex matches is the matched substr, ignore it
                .Select(e => int.Parse(e.First().Value) * int.Parse(e.Last().Value))// Multiply both sides
                .Sum()
                .ToString();
    }

    /// <summary>
    /// Similar logic, however we now look for "do()" and "don't()" strings.
    /// - "do()" means multiply any proceeding mul's
    /// - "don't()" means ignore any proceeding mul's
    /// We start in a "do()" state, and use/ignore until it changes
    /// </summary>
    /// <returns>The sum of all non-ignored mul's</returns>
    public string Part2(string[] input)
    {
        // I'm so glad I know regex
        Regex pattern = new(@"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\)", RegexOptions.Compiled);

        bool enabled = true;
        int sum = 0;
        // Match, flatten, and grab the groups
        var entries = input.SelectMany(line => pattern.Matches(line))
                            .Select(t => t.Groups.Values);
        foreach (var match in entries)
        {
            // Reminder: The first "group" is always the matched substr
            if (match.First().Value == "do()")
            {
                enabled = true;
            }
            else if (match.First().Value == "don't()")
            {
                enabled = false;
            }
            else if (enabled)
            {
                sum += match.Skip(1)
                            .Select(i => int.Parse(i.Value))
                            .Aggregate(1, (a, b) => a * b);

            }
        }

        return sum.ToString();
    }
}