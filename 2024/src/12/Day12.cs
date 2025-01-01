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

        for (int i=0; i<input.Length; i++)
        {
            for (int j=0; j<input[i].Length; j++)
            {
                if (seen.Contains(new(i, j))) continue;
                
                IEnumerable<Continuation> regionPlots = GetPlotsOfRegion(input, (i, j));
                seen.UnionWith(regionPlots);
                
                yield return regionPlots;
            }
        }
    }

    /// <summary>
    /// The cost to fence a region is Area * Perimeter:
    /// - Area: The number of plots in a region
    /// - Perimeter: The number of plot edges that don't connect to another node in the same region
    /// </summary>
    /// <param name="input">Puzzle input</param>
    /// <param name="region">The coordinates of each plot in the region</param>
    /// <returns>The cost of the fence</returns>
    private static long CalculateFenceCost(string[] input, IEnumerable<Continuation> region)
    {
        int area = region.Count();
        int perimeter = region
                        .Select(p => GetNeighbours(input, p))
                        .Select(n => n.OfType<Border>().Count())
                        .Sum();

        return area * perimeter; 
    }

    public string Part1(string[] input)
    {
        return GetAllRegions(input)
                .Select(plots => CalculateFenceCost(input, plots))
                .Sum().ToString();
    }

    public string Part2(string[] input)
    {
        throw new NotImplementedException();
    }
}