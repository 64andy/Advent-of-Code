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

            foreach (string line in input)
            {
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

        /// <summary>
        /// We must count how often each number in the left list shows up
        /// in the right list, then multiply by said number. This is called
        /// the "similarity score".
        /// e.g. If '3' shows up 5 times in the right list, 3x5=15
        /// </summary>
        /// <returns>The sum of the "similarity score"</returns>
        public string Part2(string[] input)
        {
            // Step 1: Build both lists
            List<int> leftList = [];
            List<int> rightList = [];

            foreach (string line in input)
            {
                string[] nums = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                leftList.Add(int.Parse(nums[0]));
                rightList.Add(int.Parse(nums[1]));
            }

            // Step 2: Count how often each left-list number is in the right-list
            int total = 0;
            var rightListCounts = rightList
                                    .GroupBy(i => i)
                                    .ToDictionary(p => p.Key, p => p.Count());
            foreach (int leftNum in leftList)
            {
                total += leftNum * rightListCounts.GetValueOrDefault(leftNum, 0);
            }

            return total.ToString();
        }
    }
}