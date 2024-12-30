namespace AdventOfCode2024.src.Day11;

/// <summary>
/// Input: A single line of space-separated numbers
/// </summary>
class Day11 : ISolution
{
    public int GetDay() => 11;

    private static IEnumerable<string> ApplyRules(string num)
    {
        if (num == "0")
        {
            return ["1"];
        }
        else if (num.Length % 2 == 0)
        {
            long firstHalf = long.Parse(num[..(num.Length / 2)]);
            long secondHalf = long.Parse(num.Substring(num.Length/2, num.Length/2));
            return [firstHalf.ToString(), secondHalf.ToString()];
        }
        else
        {
            return [(long.Parse(num)*2024).ToString()];
        }
    }

    public string Part1(string[] input)
    {
        IEnumerable<string> stones = input[0].Split().AsParallel();
        for (int i=0; i<25; i++)
        {
            stones = stones.SelectMany(ApplyRules);
            // Console.WriteLine($"#{i}: {string.Join(' ', stones)}");
        }

        return stones.Count().ToString();
    }

    public string Part2(string[] input)
    {
        throw new NotImplementedException();
    }
}