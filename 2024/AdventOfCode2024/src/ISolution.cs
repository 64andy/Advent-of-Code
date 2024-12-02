namespace AdventOfCode2024.src;

/// <summary>
/// Interface that each day's solver class should implement
/// </summary>
interface ISolution
{
    /// <returns>The day of the current solution as a number</returns>
    int GetDay();

    string Part1(string[] input);
    string Part2(string[] input);
}