using System.Text;
using System.Text.RegularExpressions;
using AdventOfCode2024.src;

partial class Day14 : ISolution
{
    public int GetDay() => 14;

    [GeneratedRegex(@"p=([-]?\d+),([-]?\d+) v=([-]?\d+),([-]?\d+)")]
    private static partial Regex INPUT_REGEX();

    private record Robot((int x, int y) StartPos, (int x, int y) Velocity);

    private static IEnumerable<Robot> ParseInput(string[] input)
    {
        foreach (string line in input)
        {
            int[] nums = INPUT_REGEX()
                        .Match(line)
                        .Groups.Values
                        .Skip(1)
                        .Select(g => int.Parse(g.Value))
                        .ToArray();
            yield return new((nums[0], nums[1]), (nums[2], nums[3]));
        }
    }
    
    private static int Mod(int a, int m)
    {
        int output = a % m;
        if (output < 0) output += m;
        return output;
    }

    private static (int x, int y) MoveRobotAndWrap(Robot robot, int steps, int width, int height)
    {
        return (
            x: Mod(robot.StartPos.x + (steps*robot.Velocity.x), width),
            y: Mod(robot.StartPos.y + (steps*robot.Velocity.y), height)
        );
    }

    enum Quadrant {TopLeft, TopRight, BottomLeft, BottomRight, None}
    private static Quadrant GetQuadrant((int x, int y) pos, int width, int height)
    {
        if (pos.x == width / 2 || pos.y == height / 2)
            return Quadrant.None;
        else if (pos.x < width / 2 && pos.y < height / 2)
            return Quadrant.TopLeft;
        else if (pos.x < width / 2 && pos.y > height / 2)
            return Quadrant.BottomLeft;
        else if (pos.x > width / 2 && pos.y < height / 2)
            return Quadrant.TopRight;
        else
            return Quadrant.BottomRight;
    }

    public string Part1(string[] input)
    {
        const int NUM_STEPS = 100;
        const int WIDTH = 101;
        const int HEIGHT = 103;
        var robots = ParseInput(input).Select(r => MoveRobotAndWrap(r, NUM_STEPS, WIDTH, HEIGHT));
        var quadrants = robots.Select(pos => GetQuadrant(pos, WIDTH, HEIGHT)).Where(q => q != Quadrant.None);
        var count = quadrants.GroupBy(x => x)
                .Select(g => (g.Key, g.Count()));
        return count.Select(t => t.Item2).Aggregate((a,b) => a*b).ToString();

    }

    private static void PrintPositions(IEnumerable<(int x, int y)> positions, int width, int height)
    {
        StringBuilder[] grid = new StringBuilder[height];
        for (int i=0; i < height; i++)
            grid[i] = new StringBuilder(string.Concat(Enumerable.Repeat('.', width)));
        
        foreach (var (x, y) in positions)
        {
            grid[y][x] = '█';
        }

        foreach (var line in grid)
        {
            Console.WriteLine(line);
        }
    }

    private static bool IsMaybeATree(IEnumerable<(int x, int y)> positions)
    {
        var columns = positions.GroupBy(pos => pos.x, pos => pos.y).Select(g => g.Order());
        foreach (var height in columns)
        {
            var heightDeltas = height.Select((pos, idx) => pos - idx);
            if (heightDeltas.GroupBy(x => x).Select(g => g.Count()).Any(count => count >= 30))
            {
                return true;
            }
        }

        return false;
    }

    public string Part2(string[] input)
    {
        const int WIDTH = 101;
        const int HEIGHT = 103;
        var robots = ParseInput(input);

        for (int i=0; i < WIDTH*HEIGHT; i++) {
            if (i % 500 == 0) Console.WriteLine($"{i}s");
            var positions = robots.Select(r => MoveRobotAndWrap(r, i, WIDTH, HEIGHT)).Distinct();
            if (IsMaybeATree(positions))
            {
                PrintPositions(positions, WIDTH, HEIGHT);
                return i.ToString();
                // Console.WriteLine($"{i}s: Press 'q' to quit, anything else to continue");
                // if (Console.ReadKey().Key == ConsoleKey.Q) break;
            }
        }

        return "Couldn't find it";

    }
}