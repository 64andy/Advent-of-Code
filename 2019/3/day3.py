# RIGHT_MOVEMENT = 3

# n_trees = 0
# with open("day3.in", "r") as file:
#     for i, row in enumerate(file):
#         row = row[:-1]      # Remove the trailing newline
#         offset = (i * RIGHT_MOVEMENT) % len(row)
#         if row[offset] == '#':
#             n_trees += 1

# print(i, n_trees)



slopes = [ (1,1), (3,1), (5,1), (7,1), (1,2) ]  # move (right, down) each loop
print(slopes)
trees_met = [0 for _ in range(len(slopes))]
with open("day3.in") as file:
    for i, row in enumerate(file):
        row = row[:-1]  # Remove the trailing newline
        for slope_num, (right, down) in enumerate(slopes):
            if (i % down) == 0:     # Stupid 1-right 2-down condition
                #i //= down         # 
                offset = ((i // down) * right) % len(row)
                if row[offset] == '#':
                    trees_met[slope_num] += 1
        print(trees_met)

product = 1
for t in trees_met:
    product *= t

print(i, trees_met, product)