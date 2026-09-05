scores = {
    "张三": {"语文": 85, "数学": 92, "英语": 78},
    "李四": {"语文": 90, "数学": 88, "英语": 95},
    "王五": {"语文": 85, "数学": 92, "英语": 78},
    "赵六": {"语文": 95, "数学": 90, "英语": 88},
    "孙七": {"语文": 85, "数学": 93, "英语": 95}
}
#语文平均分为86.25，最高分为95
#数学平均分为87.5，最高分为92
#英语平均分为86.5，最高分为95
#张三平均分为85.0，李四平均分为91.0，王五平均分为80.0，赵六平均分为91.0,孙七平均分为91.0

Chinese_score = []
Math_score = []
English_score = []
avg_score = {}
for name,subjects_scores in scores.items():
    Chinese_score.append(subjects_scores["语文"])
    Math_score.append(subjects_scores["数学"])
    English_score.append(subjects_scores["英语"])
    avg = 0
    for subject, score in subjects_scores.items():
        avg += score
    avg_score_float = avg / len(subjects_scores)
    avg_score[name] = avg_score_float

Chinese_avg = sum(Chinese_score) / len(Chinese_score)
Math_avg = sum(Math_score) / len(Math_score)      
English_avg = sum(English_score) / len(English_score)
print(f"语文平均分为{Chinese_avg}，最高分为{max(Chinese_score)}")
print(f"数学平均分为{Math_avg}，最高分为{max(Math_score)}")
print(f"英语平均分为{English_avg}，最高分为{max(English_score)}")
sorted_avg_score = sorted(avg_score.items(), key=lambda item: item[1], reverse=True)
print("学生平均分排序（从高到低）：")
temp = 0
same = 0
for rank,(name,avg) in enumerate(sorted_avg_score, start=1):
    if avg == temp:
        rank = rank - same -1
        #rank -=1
        same += 1
    else:
        same = 0
    print(f"{rank}. {name}平均分为{avg}")
    temp = avg