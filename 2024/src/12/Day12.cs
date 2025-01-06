using System.Collections.Frozen;
using System.Diagnostics;

namespace AdventOfCode2024.src.Day12;

/// <summary>
/// Input: A grid of letters, where neighbouring letters of the same value
///         are part of a "region"
/// </summary>
class Day12 : ISolution
{
    public int GetDay() => 12;

    /// <summary>
    /// Interface for representing a neighbour in a grid.
    /// 
    /// (If C# had Rust's typed enums I wouldn't need this)
    /// </summary>
    private interface INeighbour { }

    /// <summary>
    /// This neighbour isn't part of the current area. Acts like a terminator.
    /// Position is omitted because it isn't relevant (or is OOB)
    /// </summary>
    private record Border : INeighbour { }

    /// <summary>
    /// This neighbour is part of the current area.
    /// </summary>
    private record Continuation(int i, int j) : INeighbour;

    /// <summary>
    /// Looks at the 4 neighbours from the given position, returning whether they're part
    ///   of the same region (<c>Continuation</c>) or not (<c>Border</c>)
    /// </summary>
    /// <param name="input">Puzzle input</param>
    /// <param name="currPos">The node that we search the neighbours of</param>
    /// <returns>A 4-length enumerable stating whether each neighbour is part of the same region</returns>
    private static IEnumerable<INeighbour> GetNeighbours(string[] input, Continuation currPos)
    {
        var (ci, cj) = currPos;
        // Look one space up, down, left, right
        (int, int)[] directions = [(ci - 1, cj), (ci + 1, cj), (ci, cj - 1), (ci, cj + 1)];
        foreach (var (i, j) in directions)
        {
            // In-bounds?
            if (i >= 0 && i < input.Length && j >= 0 && j < input[i].Length
                // Part of the same region?
                && input[i][j] == input[ci][cj])
            {
                yield return new Continuation(i, j);
            }
            else
            {
                yield return new Border();
            }
        }
    }

    /// <summary>
    /// Flood-fill searches <c>input</c>, returning the position of every plot
    /// that's part of the same region
    /// </summary>
    /// <param name="input">Puzzle input</param>
    /// <param name="startPos">The starting point for the flood fill search</param>
    /// <returns>The <c>(i, j)</c> coordinates of each plot in the region that's connected to the given plot</returns>
    private static IEnumerable<Continuation> GetPlotsOfRegion(string[] input, (int i, int j) startPos)
    {
        HashSet<Continuation> visited = [];
        Stack<Continuation> frontier = new();
        frontier.Push(new Continuation(startPos.i, startPos.j));

        while (frontier.TryPop(out var plot))
        {
            if (visited.Contains(plot))
                continue;
            visited.Add(plot);

            foreach (var neighbour in GetNeighbours(input, plot).OfType<Continuation>())
                frontier.Push(neighbour);

            yield return plot;
        }
    }

    /// <summary>
    /// Searches and gets every individual region in the puzzle input
    /// </summary>
    /// <param name="input">Puzzle input</param>
    /// <returns>A 2D enumerable containing each region, which in turn contains each coordinate making up the region</returns>
    private static IEnumerable<IEnumerable<Continuation>> GetAllRegions(string[] input)
    {
        HashSet<Continuation> seen = [];

        for (int i = 0; i < input.Length; i++)
        {
            for (int j = 0; j < input[i].Length; j++)
            {
                if (seen.Contains(new(i, j))) continue;

                IEnumerable<Continuation> regionPlots = GetPlotsOfRegion(input, (i, j));
                seen.UnionWith(regionPlots);

                yield return regionPlots;
            }
        }
    }

    /// <summary>
    /// Calculates the number of fence pieces needed to fully wrap a region.
    /// 
    /// Example:
    /// XXX
    /// X.X
    /// XXX
    /// Each of the 4 sides requires 3 fence pieces, plus the inner holes needs 4
    /// Thus, (3x4 + 4) = 16
    /// </summary>
    /// <param name="input">Puzzle input</param>
    /// <param name="region">The coordinates of each plot in the region</param>
    /// <returns>The number of fence pieces needed</returns>
    private static long CalculateNumFencePieces(string[] input, IEnumerable<Continuation> region)
    {
        return region
                .Select(p => GetNeighbours(input, p))
                .Select(n => n.OfType<Border>().Count())
                .Sum();
    }

    /// <summary>
    /// VERY difficult to explain.
    /// 
    /// Given a row/column in the region, it calculates the amount of continuous faces
    ///   in a given direction, in plots NOT connected to another plot... just look at the example.
    ///   
    /// Example:
    /// .X..
    /// XXXX <- Row in question
    /// 
    /// Looking Up: The 1st & 3rd X have nothing above them, the 2nd does.
    /// = [1, 3, 4]
    ///   Because [3,4] is continuous, there are 2 faces above the row. [[1],[3,4]]
    /// Looking Down: All 4 X's have nothing beneath them.
    ///   Because [1,2,3,4] is continuous, there is 1 face beneath the row [[1,2,3,4]]
    /// </summary>
    /// <param name="line">The row/column we want to check</param>
    /// <param name="region">All plots in the region</param>
    /// <param name="direction"><c>(i, j)</c> direction to look for exposed faces</param>
    /// <returns></returns>
    private static int NumOfRowsExposedContinuousFacesInDirection(IEnumerable<Continuation> line, FrozenSet<Continuation> region, (int i, int j) direction)
    {
                    // Look at plots that aren't connected in a given direction
        return line.Where(c => region.Contains(c with
                    {
                        i = c.i + direction.i,
                        j = c.j + direction.j
                    }))
                    .Select(c => direction.i != 0 ? c.j : c.i)
                    // This only works if it's sorted
                    .Order()
                    // Continuous numbers minus their index will become equal to each other
                    // e.g. [1,2,3,  5,  8,9] => [1,1,1, 2, 4,4]
                    .Select((val, idx) => val - idx)
                    .Distinct()
                    .Count();
    }

    /// <summary>
    /// Calculates the number of faces that make up a region.
    /// A "face" is a group of continuous fences all going the same direction.
    /// 
    /// Example:
    /// XXX
    /// X.X
    /// XXX
    /// 
    /// This box has 4 external faces, and 4 internal faces = 8 total.
    /// </summary>
    private static int CalculateNumFaces(IEnumerable<Continuation> region)
    {
        int totalFaces = 0;
        FrozenSet<Continuation> plotSet = region.ToFrozenSet();
        // To get the "Total number of faces", we look at each row/column
        // For each row, we look at how many exposed continuous faces are above + below
        // For each col, we look left + right
        foreach (var row in region.GroupBy(c => c.i))
        {
            totalFaces += NumOfRowsExposedContinuousFacesInDirection(row, plotSet, (-1, 0));
            totalFaces += NumOfRowsExposedContinuousFacesInDirection(row, plotSet, (+1, 0));
        }
        foreach (var col in region.GroupBy(c => c.j))
        {
            totalFaces += NumOfRowsExposedContinuousFacesInDirection(col, plotSet, (0, -1));
            totalFaces += NumOfRowsExposedContinuousFacesInDirection(col, plotSet, (0, +1));
        }

        return totalFaces;
    }

    /// <summary>
    /// Each region needs to be fenced individually.
    /// Every plot (grid square) needs to be wrapped in at most 4 fences, for each side that doesn't
    ///   connect to the same region. This is the perimeter.
    /// Note: Different regions don't share a fence, perimeter needs to be calculated individually.
    /// 
    /// Example:
    /// XXX
    /// X.X
    /// XXX
    /// The outside needs 3 fences for each of the 4 sides, and the inner hole needs 4 total
    /// Total perimeter: (3*4 + 4) = 16
    /// 
    /// To get the price, we multiple the perimeter by the number of plots (area) 
    /// </summary>
    /// <returns>The sum of every region's fencing cost</returns>
    public string Part1(string[] input)
    {
        return GetAllRegions(input)
                .Select(plots => plots.Count() * CalculateNumFencePieces(input, plots))
                .Sum().ToString();
    }

    /// <summary>
    /// The pricing has changed, instead of "perimeter" we look at the number of faces.
    /// 
    /// If a line of connected fences all go in the same direction, we consider that a single fence.
    /// e.g.
    /// +____+
    /// |XXXX|
    /// |XXXX|
    /// +----+
    /// has 4 faces, instead of the previous part's 12
    /// </summary>
    /// <returns>The sum of every region's fencing cost, with the new face calculation</returns>
    public string Part2(string[] input)
    {
        return GetAllRegions(input)
                .Select(plots => plots.Count() * CalculateNumFaces(plots))
                .Sum().ToString();
    }
}