namespace AdventOfCode2024.src.Day01
{
    /// <summary>
    /// We are given two of numbers, where each line has two numbers separated by spaces.
    /// e.g.
    /// 1   4
    /// 2   5
    /// 3   6
    /// is two lists: [1,2,3] and [4,5,6]
    /// </summary>    
    public class Day01 : ISolution
    {
        public int GetDay() => 1;

        /// <summary>
        /// We must pair the smallest number in the left list with the smallest in the
        /// right list, then the 2nd smallest in both lists, so on and so forth.
        /// For each pair, add up how far apart they are.
        /// </summary>
        /// <returns>The sum of every pair's distance</returns>
        public string Part1(string[] input)
        {
            // Step 1: Build both lists
            List<int> leftList = [];
            List<int> rightList = [];

            foreach (string line in input) {
                string[] nums = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                leftList.Add(int.Parse(nums[0]));
                rightList.Add(int.Parse(nums[1]));
            }

            // Step 2: Sort and pair each item by position
            var pairs = leftList.Order().Zip(rightList.Order());

            // Step 3: Get the distance of each pair
            int totalDistance = pairs.Select(t => Math.Abs(t.First - t.Second)).Sum();

            return totalDistance.ToString();
        }

        public string Part2(string[] input)
        {
            return "INCOMPLETE";
        }
    }
}