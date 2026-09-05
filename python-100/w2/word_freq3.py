from collections import Counter
text = open(r"E:\AI\workspace\L\learning-log\python-100\w2\sample.txt", encoding="utf-8").read()

words = text.split()

words2 = words
counts2 = {}
words2 = [words[x].strip(",.!?;:\"'") for x in range(len(words))]
words2 = [words2[y].lower() for y in range(len(words2))]
words2 = [counts2 for counts2 in words2 if not counts2.isdigit()]
counts2 = Counter(words2)



sorted_counts2 = sorted(counts2.items(), key=lambda item: item[1], reverse=True)
for word, count in sorted_counts2[:10]:
    print(f"{word}: {count}")

print(counts2.get("3"))