using System.Text;

namespace AdventOfCode2024.src.Day06;

/// <summary>
/// Our input is a grid, where:
/// - Dots '.' are empty spaces
/// - Hashes '#' are obstacles
/// - The caret '^' is our start position
/// </summary>
class Day06 : ISolution
{
    public int GetDay() => 6;

    private static (int, int) FindStartPos(string[] input)
    {
        for (int i = 0; i < input.Length; i++)
            for (int j = 0; j < input[i].Length; j++)
                if (input[i][j] == '^') return (i, j);
        throw new KeyNotFoundException("'^' not found in input");
    }


    enum Direction
    {
        Up,
        Down,
        Left,
        Right
    }
    static readonly Dictionary<Direction, (int, int)> directionsToDeltas = new() {
        {Direction.Up, (-1, 0)},
        {Direction.Down, (+1, 0)},
        {Direction.Left, (0, -1)},
        {Direction.Right, (0, +1)}
    };

    private static Direction RotateRight(Direction dir)
        => dir switch
        {
            Direction.Up => Direction.Right,
            Direction.Right => Direction.Down,
            Direction.Down => Direction.Left,
            Direction.Left => Direction.Up,
            _ => throw new NotImplementedException("That's not part of the enum you barnacle-head")
        };

    /// <summary>
    /// We start at the '^', and move up until we hit an obstacle.
    /// When this happens, we turn clockwise 90deg (e.g. Up->Right).
    /// We keep moving until we move outside the bounds of the grid.
    /// </summary>
    /// <returns>The number of *distinct* spaces we stepped on,
    ///           including the start pos. If we retread, ignore it.
    /// </returns>
    public string Part1(string[] input)
    {
        var (i, j) = FindStartPos(input);
        var direction = Direction.Up;
        var (di, dj) = directionsToDeltas[direction];
        HashSet<(int, int)> seen = [(i, j)];
        // Loop until we'd move out of bounds
        while (0 <= i + di && i + di < input.Length
                && 0 <= j + dj && j + dj < input[i + di].Length)
        {
            if (input[i + di][j + dj] == '#')
            {
                direction = RotateRight(direction);
                (di, dj) = directionsToDeltas[direction];
            }
            else
            {
                i += di;
                j += dj;
            }
            seen.Add((i, j));
        }

        return seen.Count.ToString();
    }

    /// <summary>
    /// Checks whether following the rules of the given grid gets you
    /// caught in an infinite loop.
    /// </summary>
    private static bool IsCyclic(string[] input)
    {
        var (i, j) = FindStartPos(input);
        var direction = Direction.Up;
        var (di, dj) = directionsToDeltas[direction];
        // We're relying on the default hash impl of tuples
        HashSet<(Direction, (int, int))> seen = [(direction, (i, j))];
        // Loop until we'd move out of bounds
        while (0 <= i + di && i + di < input.Length
                && 0 <= j + dj && j + dj < input[i + di].Length)
        {
            if (input[i + di][j + dj] == '#')
            {
                direction = RotateRight(direction);
                (di, dj) = directionsToDeltas[direction];
            }
            else
            {
                i += di;
                j += dj;
            }
            if (seen.Contains((direction, (i, j))))
            {
                return true;
            }
            else
            {
                seen.Add((direction, (i, j)));
            }
        }

        return false;
    }

    /// <summary>
    /// Generates every version of the given grid with one new obstacle
    /// in every empty spot
    /// </summary>
    /// <param name="input">The grid we're permutating</param>
    private static IEnumerable<string[]> AllPossibleBlockedBoards(string[] input)
    {
        for (int i = 0; i < input.Length; i++)
        {
            for (int j = 0; j < input[i].Length; j++)
            {
                if (input[i][j] == '.')
                {
                    // The immutable string song & dance
                    string[] copy = (string[])input.Clone();
                    var newLine = new StringBuilder(copy[i]);
                    newLine[j] = '#';
                    copy[i] = newLine.ToString();
                    yield return copy;

                }
            }
        }
    }

    /// <summary>
    /// Now we want to know what places to add a single new obstacle that would
    /// cause an infinite loop.
    /// </summary>
    /// <remarks>Warning: This is NOT an efficient solution, it will take ~15s</remarks>
    /// <returns>
    /// The number of obstacles you could put to cause an infinite loop
    /// </returns>
    public string Part2(string[] input)
    {
        return AllPossibleBlockedBoards(input)
                .Where(IsCyclic)
                .Count()
                .ToString();
    }
}