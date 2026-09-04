text = "Python is a powerful language. Learn Python daily, and practice Python code. Learning is a habit; daily practice makes progress."
words = text.split()
print(words)
counts = {}
for i in range(len(words)):
    words[i] = words[i].strip(".,;!?")
    words[i] = words[i].lower()
    counts[words[i]] = counts.get(words[i], 0) + 1
sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
for word, count in sorted_counts[:5]:
    print(f"{word}: {count}")