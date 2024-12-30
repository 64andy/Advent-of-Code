namespace AdventOfCode2024.src.Day11;

/// <summary>
/// Input: A single line of space-separated numbers
/// </summary>
class Day11 : ISolution
{
    public int GetDay() => 11;

    private static IEnumerable<string> ApplyRules(string key)
    {
        if (key == "0")
        {
            return ["1"];
        }
        else if (key.Length % 2 == 0)
        {
            long firstHalf = long.Parse(key[..(key.Length / 2)]);
            long secondHalf = long.Parse(key.Substring(key.Length / 2, key.Length / 2));
            return [firstHalf.ToString(), secondHalf.ToString()];
        }
        else
        {
            return [(long.Parse(key) * 2024).ToString()];
        }
    }

    /// <summary>
    /// Turns a stream of KeyValuePairs into a dictionary, adding together
    /// any pair's values that share a key.
    /// </summary>
    private static Dictionary<string, long> SumIntoDict(IEnumerable<KeyValuePair<string, long>> pairs)
    {
        Dictionary<string, long> output = [];
        foreach (var (key, val) in pairs)
        {
            if (output.TryGetValue(key, out var count))
                output[key] = count + val;
            else
                output[key] = val;
        }

        return output;
    }

    /// <summary>
    /// Calculates the number of blinks
    /// </summary>
    /// <param name="input">Puzzle input</param>
    /// <param name="numBlinks">How many times the logic should be run</param>
    /// <returns></returns>
    private static long CalculateNumStones(string input, int numBlinks)
    {
        // Count the number of initial stones
        Dictionary<string, long> occurrences = SumIntoDict(
            input.Split().Select(s => new KeyValuePair<string, long>(s, 1))
        );

        for (int i = 0; i < numBlinks; i++)
        {
            var transformed = occurrences.SelectMany(
                // Split the strings
                kv => ApplyRules(kv.Key)
                    // Then reapply the "count" from earlier
                    .Select(key => new KeyValuePair<string, long>(key, kv.Value))
            );
            occurrences = SumIntoDict(transformed);
        }

        return occurrences.Select(kv => kv.Value).Sum();
    }

    /// <summary>
    /// We have a line of "rocks", which each contain a number.
    /// Every blink these numbers change:
    /// - If the number is 0, it turns into a 1
    /// - Else if the number is even, it splits in half ('1201' -> ['12', '01'] -> [12, 1])
    /// - Else the number is multiplied by 2024 ('100' => '202400')
    /// 
    /// Be warned, the number of rocks grows VERY fast
    /// </summary>
    /// <returns>The number of stones remaining after 25 "blinks"</returns>
    public string Part1(string[] input)
    {
        return CalculateNumStones(input[0], 25).ToString();
    }

    /// <summary>
    /// We've increased the required number of blinks to 75
    /// </summary>
    public string Part2(string[] input)
    {
        return CalculateNumStones(input[0], 75).ToString();
    }
}