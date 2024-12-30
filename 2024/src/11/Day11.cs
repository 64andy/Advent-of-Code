namespace AdventOfCode2024.src.Day11;

/// <summary>
/// Input: A single line of space-separated numbers
/// </summary>
class Day11 : ISolution
{
    public int GetDay() => 11;

    private static IEnumerable<KeyValuePair<string, long>> ApplyRules(KeyValuePair<string, long> pair)
    {
        var (key, count) = pair;
        if (key == "0")
        {
            return [new("1", count)];
        }
        else if (key.Length % 2 == 0)
        {
            long firstHalf = long.Parse(key[..(key.Length / 2)]);
            long secondHalf = long.Parse(key.Substring(key.Length/2, key.Length/2));
            return [new(firstHalf.ToString(), count), new(secondHalf.ToString(), count)];
        }
        else
        {
            return [new((long.Parse(key)*2024).ToString(), count)];
        }
    }

    private static Dictionary<string, long> CrushIntoDict(IEnumerable<KeyValuePair<string, long>> pairs)
    {
        Dictionary<string, long> output = [];
        foreach (var kv in pairs)
        {
            if (output.TryGetValue(kv.Key, out var count))
            {
                output[kv.Key] = count + kv.Value;
            }
            else
            {
                output[kv.Key] = kv.Value;
            }
        }

        return output;
    }

    private static long CalculateNumStones(string input, int numBlinks)
    {
        Dictionary<string, long> occurrences = [];
        foreach (string val in input.Split())
        {
            long count = occurrences.GetValueOrDefault(val, 0);
            occurrences[val] = count+1;
        }

        for (int i=0; i<numBlinks; i++)
        {
            occurrences = CrushIntoDict(occurrences.SelectMany(ApplyRules));
        }

        return occurrences.Select(kv => kv.Value).Sum();
    }

    public string Part1(string[] input)
    {
        return CalculateNumStones(input[0], 25).ToString();
    }

    public string Part2(string[] input)
    {
        return CalculateNumStones(input[0], 75).ToString();
    }
}