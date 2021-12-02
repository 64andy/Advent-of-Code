total_score = 0
group = set()
first_line = True
with open("day6.in", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) > 0:
            if first_line:
                group.update(line)
            else:
                group.intersection_update(line)
            first_line = False
        else:
            total_score += len(group)
            group.clear()
            first_line = True

total_score += len(group)

print(total_score)