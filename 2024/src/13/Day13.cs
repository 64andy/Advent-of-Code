using System.Text.RegularExpressions;

namespace AdventOfCode2024.src.Day13;

/// <summary>
/// Input: An information list for various crane game machines, plus a "goal", separated by a blank line.
/// Each machine has two buttons, A and B, which moves the cranes in a given direction.
/// 
/// The first two lines specify how far the buttons move the crane, the third line is where
///   you must end up after pressing these buttons.
/// 
/// Example:
/// Button A: X+94, Y+34
/// Button B: X+22, Y+67
/// Prize: X=8400, Y=5400
/// 
/// Button A: X+26, Y+66
/// Button B: X+67, Y+21
/// Prize: X=12748, Y=12176
/// </summary>
partial class Day13 : ISolution
{
    public int GetDay() => 13;

    [GeneratedRegex(
        @"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    )]
    private static partial Regex MACHINE_INFO_REGEX();

    record Game((long X, long Y) A, (long X, long Y) B, (long X, long Y) Prize);

    private static IEnumerable<Game> ParseGame(string[] input)
    {
        return MACHINE_INFO_REGEX().Matches(string.Join('\n', input))
                .Select(m => m.Groups.Values.Skip(1))   // First group is the whole string (we don't want)
                .Select(m => m.Select(n => long.Parse(n.Value)).ToArray())
                .Select(n => new Game((n[0], n[1]), (n[2], n[3]), (n[4], n[5])));

    }

    /// <summary>
    /// Tries to guess how many button presses are needed, using simultaneous equations.
    /// 
    /// </summary>
    /// <returns></returns>
    private static (long APresses, long BPresses)? TrySolveButtonPresses(Game game)
    {
        /*
        I've forgotten my simultaneous equations so:
        https://thirdspacelearning.com/gcse-maths/algebra/simultaneous-equations/
        
        Solve by elimination:
        * 3a + 2b = 8
        * 2a + 5b = -2
        
        PART 1:
        To find `b` we must eliminate `a`, we do this by multiplying each equation by
          the other one's `a` value
        * Multiplied by 2 -> 6a + 4b = 16
        * Multiplied by 3 -> 6a + 15b = -6
        Because `a` is the same, we can subtract the two equations and get `b`
        * a(6-6) + b(4-15) = (16 - -6)
        = 0 + b(-11) = 22
        b = 22 / -11
        b = -2

        PART 2:
        Now we know b = -2, we can just fill in the equation to solve
        * 3a + 2(-2) = 8
        * 3a + -4 = 8
        * 3a = 8 - -4
        * 3a = 12
        * a = 12/3
        * a = 4
        */
        // PART 1: Eliminate A to get B
        long A_lhs = game.A.X * game.B.Y - game.A.Y * game.B.X;
        long A_rhs = game.Prize.X * game.B.Y - game.Prize.Y * game.B.X;
        // Our number of presses must be a whole number, we can't "half-press" like SM64
        if (A_rhs % A_lhs != 0) return null;
        long A = A_rhs / A_lhs;

        // PART 2: Now B's known, solve for A
        long B_rhs = game.Prize.X - (A * game.A.X);
        if (B_rhs % game.B.X != 0) return null;
        long B = B_rhs / game.B.X;

        // Final sanity check: We can't have negative button presses
        if (A < 0 || B < 0) return null;
        return (A, B);
    }

    public string Part1(string[] input)
    {
        return ParseGame(input)
                .Select(TrySolveButtonPresses)
                .OfType<(long APresses, long BPresses)>()
                .Select(p => p.APresses * 3 + p.BPresses)
                .Sum().ToString();
    }

    public string Part2(string[] input)
    {
        return ParseGame(input)
                .Select(g => g with {Prize = (g.Prize.X + 10_000_000_000_000, g.Prize.Y + 10_000_000_000_000)})
                .Select(TrySolveButtonPresses)
                .OfType<(long APresses, long BPresses)>()
                .Select(p => p.APresses * 3 + p.BPresses)
                .Sum().ToString();
    }
}