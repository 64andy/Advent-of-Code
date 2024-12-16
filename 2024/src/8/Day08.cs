using System.Collections.Frozen;

namespace AdventOfCode2024.src.Day08;

/// <summary>
/// The input is a grid of characters, containing "antenna" groups
/// where:
/// - dots '.' are empty spaces
/// - any other character is an antenna
/// Example:
/// ............
/// ........0...
/// .....0......
/// .......0....
/// ....0.......
/// ......A.....
/// ............
/// ............
/// ........A...
/// .........A..
/// ............
/// ............
/// </summary>
class Day08 : ISolution
{
    public int GetDay() => 8;

    // Only used because tuples call their fields Item1/2
    private readonly record struct Coord(int i, int j);

    /// <summary>
    /// Searches the grid to find every antenna's position
    /// </summary>
    /// <param name="input">The grid of antenna</param>
    /// <returns>A mapping from every antenna group to their positions</returns>
    private static Dictionary<char, List<Coord>> GetAntennaPos(string[] input)
    {
        Dictionary<char, List<Coord>> antennaPos = [];
        char ch;
        for (int i = 0; i < input.Length; i++)
            for (int j = 0; j < input[i].Length; j++)
                if ((ch = input[i][j]) != '.')
                    if (antennaPos.TryGetValue(ch, out var coords))
                        coords.Add(new Coord(i, j));
                    else
                        antennaPos.Add(ch, [new Coord(i, j)]);

        return antennaPos;
    }

    /// <summary>
    /// Generates every antinode's position from the given antennas,
    ///   where antinode are found by taking the distance between each
    ///   antenna pair, then going an equal distance away from each antenna
    /// 
    /// Examples: (Where 'A' are antenna, '#' are antinodes)
    /// ...# | .#.. | #.........
    /// ..A. | .A.. | ...A......
    /// .A.. | .A.. | ......A...
    /// #... | .#.. | .........#
    /// 
    /// NOTE: This won't check if an antinode's outside the grid,
    /// you have to check that
    /// </summary>
    /// <param name="antennas">The antennas of a 'single' group</param>
    /// <returns>Yields every antinode for every antenna pair</returns>
    private static IEnumerable<Coord> FindAntinodes(List<Coord> antennas)
    {
        // An itertools.combinations loop
        for (int i = 0; i < antennas.Count; i++)
        {
            for (int j = i + 1; j < antennas.Count; j++)
            {
                var a = antennas[i];
                var b = antennas[j];
                var (di, dj) = (a.i - b.i, a.j - b.j);
                yield return new(a.i + di, a.j + dj);
                yield return new(b.i - di, b.j - dj);
            }
        }
    }

    /// <summary>
    /// For each pair of antenna from the same group, we must find their antinodes.
    ///   These are found by taking their direction & distance, then moving 180deg
    ///   the other way for both of the two nodes.
    /// Antinodes must also be within the bounds of the grid
    /// </summary>
    /// <returns>The number of unique antinode positions</returns>
    public string Part1(string[] input)
    => GetAntennaPos(input)
        .Select(kv => kv.Value)
        .SelectMany(FindAntinodes)
        .Where(anti => anti.i >= 0 && anti.i < input.Length
                    && anti.j >= 0 && anti.j < input[anti.i].Length)
        .ToFrozenSet()
        .Count.ToString();

    public string Part2(string[] input)
    {
        return "UNIMPLEMENTED";
    }
}