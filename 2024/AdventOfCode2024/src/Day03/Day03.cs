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
                .Select(m => m.Groups.Values.Skip(1).Take(2))       // The first entry in regex matches is the whole string, ignore it
                .Select(e => int.Parse(e.First().Value) * int.Parse(e.Last().Value))// Multiply both sides
                .Sum()
                .ToString();

    }

    public string Part2(string[] input)
    {
        return "UNIMPLEMENTED";
    }
}