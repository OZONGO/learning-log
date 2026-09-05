scores = {
    "Alice": [90, 85, 77],
    "Bob":   [60, 72, 88],
    "Tony": [85, 90, 95]
}

print(scores["Alice"][1])
for name,marks in scores.items():
    print(f"{name}: {(sum(marks)/len(marks)):.2f}")

for name,marks in scores.items():
    marks_above_85 = [m for m in marks if m >= 85]
    print(f"{name}: {marks_above_85}")