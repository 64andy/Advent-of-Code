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

        for (int i = 0; i < denseLayout.Length; i += 2)
        {
            layout.AddRange(Enumerable.Repeat(i / 2, int.Parse(denseLayout[i].ToString())));
            if (i + 1 < denseLayout.Length)
                layout.AddRange(Enumerable.Repeat(-1, int.Parse(denseLayout[i + 1].ToString())));
        }

        return layout;
    }

    private static void Swap<T>(List<T> list, int idx1, int idx2)
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
    private static List<int> DefragString_IndividualNums(string origLayout)
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
        return DefragString_IndividualNums(input[0])
                .Select((val, idx) => (long)(idx * val))
                .Sum()
                .ToString();
    }

    /// <summary>
    /// Swaps multiple consecutive elements within a given list
    /// </summary>
    /// <param name="list">The list to have its elements swapped</param>
    /// <param name="from">Index of one side to be swapped</param>
    /// <param name="to">Index of the other side to be swapped</param>
    /// <param name="size">The number of elements to swap</param>
    /// <exception cref="IndexOutOfRangeException">Thrown if this operation would cause an out-of-bounds write</exception>
    private static void SwapRange<T>(List<T> list, int from, int to, int size)
    {
        if (from + size > list.Count)
            throw new IndexOutOfRangeException($"idx1: {from}+{size} would exceed list's size ({list.Count})");
        if (to + size > list.Count)
            throw new IndexOutOfRangeException($"idx2: {to}+{size} would exceed list's size ({list.Count})");
        for (int i = 0; i < size; i++)
            Swap(list, from + i, to + i);
    }

    /// <summary>
    /// Gets the position & length of the next run of empty spaces from the given index
    /// </summary>
    /// <returns>A 2-tuple pair of (index, length), or null if none exists</returns>
    private static (int, int)? FindProceedingBlankSpace(List<int> list, int idx)
    {
        idx = JumpForwardsUntilBlank(list, idx);
        if (idx >= list.Count) return null;
        var size = 0;
        while (idx+size < list.Count && list[idx+size] == -1)
            size++;
        return (idx, size);
    }

    /// <summary>
    /// Gets the position & length of the next preceeding block from the given position
    /// </summary>
    /// <returns>A 2-tuple pair of (index, length), or null if none exists</returns>
    private static (int, int)? FindPreceedingBlock(List<int> list, int idx)
    {
        idx = JumpBackwardsWhileNotBlank(list, idx);
        if (idx == -1) return null;
        var fileType = list[idx];
        var size = 1;
        while (idx > 0 && list[idx-1] == fileType) {
            idx--;
            size++;
        }
        return (idx, size);
    }

    /// <summary>
    /// Condenses the data by fitting each right-most block into the left-most empty
    ///   space that can fit it, or not moving if none exist.
    /// </summary>
    /// <param name="origLayout">The compressed data (the input data)</param>
    /// <returns>The defragmented data (will likely still contain blank spaces)</returns>
    private static List<int> DefragString_WholeBlocks(string origLayout)
    {
        var layout = DecompressString(origLayout);
        HashSet<int> seen = [];
        // 1. Get the next (preceeding) block of numbers
        int blockPos = layout.Count;
        int blockSize;
        (int, int)? endBlock;
        while ((endBlock = FindPreceedingBlock(layout, blockPos-1)) != null)
        {
            (blockPos, blockSize) = endBlock.Value;
            if (seen.Contains(layout[blockPos])) continue;  // Ignore if seen

            // 2. Find the next block of blank spaces that can fit it
            int emptyPos = 0;
            int emptySize = 0;
            (int, int)? emptyBlock;
            while ((emptyBlock = FindProceedingBlankSpace(layout, emptyPos + emptySize)) != null)
            {
                (emptyPos, emptySize) = emptyBlock.Value;
                if (emptyPos >= blockPos) break;
                if (emptySize >= blockSize) {
                    SwapRange(layout, from:blockPos, to:emptyPos, size:blockSize);
                    break;
                }
            }
        }

        return layout;
    }

    /// <summary>
    /// Now, we condense by moving entire blocks instead of one number at a time.
    /// Each right-most block should be moved into the left-most blank space that can
    ///   fit it, if one exists, otherwise don't move it.
    /// </summary>
    /// <returns>The checksum of the condensed string</returns>
    public string Part2(string[] input)
    {
        return DefragString_WholeBlocks(input[0])
                .Select(val => (val == -1) ? 0 : val)
                .Select((val, idx) => (long)(idx * val))
                .Sum()
                .ToString();
    }
}