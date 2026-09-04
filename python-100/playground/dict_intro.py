scores = {"python": 90, "bs": 85}
scores["english"] = 88
scores["math"] = 92
print (scores["python"])
print(f"{scores.get("abc")}")
for k, v in scores.items():
    print(f"{k}:{v}")
#scores[["python", "bs"]] = 1