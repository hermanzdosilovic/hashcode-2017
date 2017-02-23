import random
import sys

R, C, L, H = tuple(int(x) for x in input().split(" "))
pizza = [[" " for i in range(C + 1)] for j in range(R + 1)]
for i in range(1, R + 1):
    pizza[i] = list(" " + input())

slices = []
for s in range(2*L, H + 1):
    for i in range(1, s + 1):
        if s%i == 0:
            slices.append((i, s//i))

number_of_tomatos = [[0 for i in range(C + 1)] for j in range(R + 1)]
for i in range(1, R + 1):
    for j in range(1, C + 1):
        number_of_tomatos[i][j] = (
            number_of_tomatos[i - 1][j] +
            number_of_tomatos[i][j - 1] -
            number_of_tomatos[i - 1][j - 1] +
            int(pizza[i][j] == "T")
        )

number_of_mushrooms = [[0 for i in range(C + 1)] for j in range(R + 1)]
for i in range(1, R + 1):
    for j in range(1, C + 1):
        number_of_mushrooms[i][j] = (
            number_of_mushrooms[i - 1][j] +
            number_of_mushrooms[i][j - 1] -
            number_of_mushrooms[i - 1][j - 1] +
            int(pizza[i][j] == "M")
        )

current_best_area = 0
try:
    f = open(sys.argv[1], "r")
    rectangles = f.read().split("\n")[1:]
    f.close()
    for rec in rectangles:
        if not rec:
            break
        rec = tuple([int(x) for x in rec.split(" ")])
        current_best_area += (rec[2] - rec[0] + 1)*(rec[3] - rec[1] + 1)
except FileNotFoundError:
    pass

print("Your current best area is:", current_best_area)

number_of_iterations = int(sys.argv[2])
while number_of_iterations >= 0:
    number_of_iterations -= 1
    visited = set()
    rectangles = []
    for i in range(1, R + 1):
        for j in range(1, C + 1):
            if (i, j) in visited:
                continue
            
            random.shuffle(slices)
            for s in slices: # s[0] is width, s[1] is height
                if i + s[1] - 1 > R or j + s[0] - 1 > C:
                    continue

                mushrooms = (
                    number_of_mushrooms[i + s[1] - 1][j + s[0] - 1] -
                    number_of_mushrooms[i + s[1] - 1][j - 1] -
                    number_of_mushrooms[i - 1][j + s[0] - 1] +
                    number_of_mushrooms[i - 1][j - 1]
                )

                tomatos = (
                    number_of_tomatos[i + s[1] - 1][j + s[0] - 1] -
                    number_of_tomatos[i + s[1] - 1][j - 1] -
                    number_of_tomatos[i - 1][j + s[0] - 1] +
                    number_of_tomatos[i - 1][j - 1]
                )

                if mushrooms < L or tomatos < L:
                    continue

                valid = True
                for x in range(i, i + s[1]):
                    for y in range(j, j + s[0]):
                        if (x, y) in visited:
                            valid = False
                            break
                    if not valid:
                        break

                if not valid:
                    continue

                rectangles.append((i - 1, j - 1, i + s[1] - 2, j + s[0] - 2))
                for x in range(i, i + s[1]):
                    for y in range(j, j + s[0]):
                        visited |= {(x, y)}

    area = 0
    for rec in rectangles:
        area += (rec[2] - rec[0] + 1)*(rec[3] - rec[1] + 1)

    if area > current_best_area:
        current_best_area = area
        f = open(sys.argv[1], "w")
        print(len(rectangles), file=f)
        for rec in rectangles:
            print(str(rec)[1:-1].replace(",", ""), file=f)
        f.flush()
        f.close()
