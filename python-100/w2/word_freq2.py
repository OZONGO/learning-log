text = open(r"E:\AI\workspace\L\learning-log\python-100\w2\sample.txt", encoding="utf-8").read()

words = text.split()
counts = {}
# for i in range(len(words)):
#     words[i] = words[i].strip(".,;!?")
#     words[i] = words[i].lower()
#     counts[words[i]] = counts.get(words[i], 0) + 1

for i,x in enumerate(words):
    x = x.strip(".,;!?")
    x = x.lower()
    counts[x] = counts.get(x, 0) + 1

sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
for word, count in sorted_counts[:10]:
    print(f"{word}: {count}")

    