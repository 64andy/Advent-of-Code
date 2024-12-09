namespace AdventOfCode2024.src.Day06;

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

    public string Part1(string[] input)
    {
        var (i, j) = FindStartPos(input);
        var direction = Direction.Up;
        var (di, dj) = directionsToDeltas[direction];
        HashSet<(int, int)> seen = [(i,j)];
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

    public string Part2(string[] input)
    {
        return "UNIMPLEMENTED";
    }
}