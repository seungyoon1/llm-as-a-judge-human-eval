import json

topic = {}
rubric_name = ["Grammaticality", "Fluency", "Coherence", "Consistency", "Relevance"]
topic_analysis_result = {}

age = {}
age_result = {}

with open('./evaluation_results.json', 'r') as file:
    data = json.load(file)

for d in data:
    if d['task'] not in topic.keys():
        topic[d['task']] ={}
        topic_analysis_result[d['task']] = {}
    if d['age'] not in age.keys():
        age[d['age']]={}
        age_result[d['age']] = {}
    for rn in rubric_name:
        if rn not in topic[d['task']].keys():
            topic[d['task']][rn] = []
        topic[d['task']][rn].append(d[f"{rn} Score"])

        
        if rn not in age[d['age']].keys():
            age[d['age']][rn] = []
        age[d['age']][rn].append(d[f"{rn} Score"])

for task_name in topic.keys():
    for rn in rubric_name:
        topic_analysis_result[task_name][rn] = sum(topic[task_name][rn]) / len(topic[task_name][rn])

for age_inst in age.keys():
    for rn in rubric_name:
        age_result[age_inst][rn] = sum(age[age_inst][rn]) / len(age[age_inst][rn])
    

for task_name in topic.keys():
    print(task_name)
    for rn in rubric_name:
        print(f"{rn} Score: {topic_analysis_result[task_name][rn]}")

print()
print()
print()

for age_inst in age.keys():
    print(f"Age: {str(age_inst)}")
    for rn in rubric_name:
        print(f"{rn} Score: {age_result[age_inst][rn]}")