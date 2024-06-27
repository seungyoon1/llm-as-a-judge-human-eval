import json

age = {}
task = {}
language = {}
student_id = {}

with open('./human_data.json', 'r') as file:
    data = json.load(file)

for d in data:
    if d['age'] not in age.keys():
        age[d['age']]=0
    age[d['age']]+=1

    if d['task'] not in task.keys():
        task[d['task']]=0
    task[d['task']]+=1

    if d['language'] not in language.keys():
        language[d['language']]=0
    language[d['language']]+=1

    if d['student_id'] not in student_id.keys():
        student_id[d['student_id']]=0
    student_id[d['student_id']]+=1

print(age)
print()
print()
print(task)
print()
print()
print(language)
print()
print()
print(student_id)