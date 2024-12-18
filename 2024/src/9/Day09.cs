namespace AdventOfCode2024.src.Day09;

/// <summary>
/// The input is a single string of numbers, representing data in a file system.
/// These numbers represent run-lengths of numbers & blank spaces, oscillating
///   on each new digit.
/// In addition, each run's numbers should be set to the number of runs thusfar (from 0)
/// Example: 12345 => [run of one 0, 2 blanks, run of three 1s, 4 blanks, run of five 2s]
///                => "0..111....22222"
/// Example: 2333133121414131402 => "00...111...2...333.44.5555.6666.777.888899"
///                                 [ 2  3  3  31  3  31 21   41   41  31   402]
/// </summary>
class Day09 : ISolution
{
    public int GetDay() => 9;

    private static List<int> DecompressString(string denseLayout)
    {
        List<int> layout = [];
        
        for (int i=0; i<denseLayout.Length; i += 2)
        {
            layout.AddRange(Enumerable.Repeat(i/2, int.Parse(denseLayout[i].ToString())));
            if (i+1 < denseLayout.Length)
                layout.AddRange(Enumerable.Repeat(-1, int.Parse(denseLayout[i+1].ToString())));
        }

        return layout;
    }

    private static void Swap(List<int> list, int idx1, int idx2)
    {
        (list[idx2], list[idx1]) = (list[idx1], list[idx2]);
    }
    
    private static int JumpForwardsUntilBlank(List<int> list, int idx)
    {
        while (idx < list.Count && list[idx] != -1)
            idx++;
        return idx;
    }
    private static int JumpBackwardsWhileNotBlank(List<int> list, int idx)
    {
        while (idx >= 0 && list[idx] == -1)
            idx--;
        return idx;
    }

    /// <summary>
    /// Condenses the data by fitting each right-most number into the left-most empty
    ///   slot, until the data's one long continous block.
    /// </summary>
    /// <param name="origLayout">The compressed data (the input data)</param>
    /// <returns>The defragmented data (contains no blank spaces)</returns>
    private static List<int> DefragString(string origLayout)
    {
        var layout = DecompressString(origLayout);

        // The leftmost pointer is always on a blank slot
        int startIdx = JumpForwardsUntilBlank(layout, 0);
        // The rightmost pointer is always on a non-empty slot
        int endIdx = JumpBackwardsWhileNotBlank(layout, layout.Count - 1);
        // When the "only on blanks" pointer crosses over the "only on valid slots"
        //   pointer, we know that we've filled every blank space.
        while (startIdx < endIdx)
        {
            Swap(layout, startIdx, endIdx);
            startIdx = JumpForwardsUntilBlank(layout, startIdx);
            endIdx = JumpBackwardsWhileNotBlank(layout, endIdx);
        }
        // Crop off the blank spaces on the far-right
        return layout[..startIdx];
    }

    /// <summary>
    /// First, we have to "condense" the data by moving each right-most number into
    ///   every left-most free space, until there are no empty spaces left.
    /// Example:
    ///  ┌────────────┐
    ///  ├┐   ┌┬┬─┬┬┐┌┤
    /// 0..111....22222 => 022111222......
    /// (NOTE: Each number's ID can go above 9, they're single-digits here for visual clarity)
    /// 
    /// After this, calculate the new data's checksum, which if found by multiplying each
    /// number by its index, and summing across every number.
    /// </summary>
    /// <returns>The checksum of the condensed string</returns>
    public string Part1(string[] input)
    {
        return DefragString(input[0])
                .Select((val, idx) => (long)(idx * val))
                .Sum()
                .ToString();
    }

    public string Part2(string[] input)
    {
        throw new NotImplementedException();
    }
}