using System.Reflection;
using AdventOfCode2024.src;

namespace AdventOfCode2024;

public class AdventOfCode
{
    /// <summary>
    /// Gets all of the daily AoC solutions from this project
    /// </summary>
    /// <returns>A mapping of every day in this project to its solution class</returns>
    private static Dictionary<int, ISolution> GetAllSolutions()
    {
        return Assembly.GetExecutingAssembly().GetTypes()
                        .Where(t => t.IsClass && !t.IsAbstract && t.IsAssignableTo(typeof(ISolution)))
                        .Select(t =>
                        {
                            object instance = Activator.CreateInstance(t) ?? throw new NullReferenceException("Couldn't initialize " + t.Name);
                            ISolution solution = (ISolution)instance;
                            return solution;
                        })
                        .ToDictionary(
                            t => t.GetDay(),
                            t => t
                        );

    }

    /// <summary>
    /// Asks the user which solution they want to solve via stdin
    /// </summary>
    /// <param name="solutions">The mapping of each day to its corresponding solution</param>
    /// <returns>The day's solution which the user asked for,
    /// or <c>null</c> if the user asked to quit</returns>
    private static ISolution? AskForSolution(Dictionary<int, ISolution> solutions)
    {
        int[] days = solutions.Select(t => t.Key).Order().ToArray();
        Console.WriteLine("Number of solutions: " + days.Length);

        ISolution? output = null;
        do
        {
            Console.Write(string.Format("Please enter the number of the day to solve [{0}-{1} or 'q' to quit]: ", days.First(), days.Last()));
            string sDay = Console.ReadLine() ?? "q";
            if (sDay == "q")
            {
                return null;
            }

            try
            {
                int day = int.Parse(sDay);
                output = solutions[day];
            } catch (FormatException) {
                Console.WriteLine(string.Format("\"{0}\" is not a number", sDay));
            } catch (KeyNotFoundException) {
                Console.WriteLine(string.Format("Day #{0} does not have a solution", sDay));
            }
        } while (output == null);

        return output;
    }

    public static void Main(string[] args)
    {
        var allSolutions = GetAllSolutions();
        ISolution? solution = AskForSolution(allSolutions);

        if (solution == null)
        {
            return;
        }

        Console.WriteLine("Output for Part 1: " + solution.Part1(["UNKNOWN"]));
        Console.WriteLine("Output for Part 2: " + solution.Part2(["UNKNOWN"]));
    }
}