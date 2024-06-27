# Absolute Grading: Outputs score of 1 to 5

import os
import json
from prometheus_eval.litellm import AsyncLiteLLM
from prometheus_eval.vllm import VLLM
from prometheus_eval import PrometheusEval
from prometheus_eval.prompts import ABSOLUTE_PROMPT_WO_REF, SCORE_RUBRIC_TEMPLATE

os.environ['OPENAI_API_KEY'] = "" # FILL IN ME

# model = VLLM(model="prometheus-eval/prometheus-7b-v2.0")
model = AsyncLiteLLM('gpt-4-turbo', requests_per_minute=100)
judge = PrometheusEval(model=model, absolute_grade_template=ABSOLUTE_PROMPT_WO_REF)

with open('./human_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

instructions = []
responses = []

for d in data:
    instructions.append(d['input'])
    responses.append(d['output'])

# Rubric for Grammaticality
grammaticality_rubric = {
  "criteria": "Does the text demonstrate proper grammatical usage, considering it is written by a Korean student?",
  "score1_description": "The text contains frequent grammatical errors, making it difficult to understand.",
  "score2_description": "The text shows occasional grammatical errors, which disrupt the flow and clarity of the text.",
  "score3_description": "The text generally adheres to grammatical rules, though minor errors are present.",
  "score4_description": "The text demonstrates good grammaticality with rare errors that do not affect comprehension.",
  "score5_description": "The text excels in grammatical usage, with clear and correct grammar throughout."
}

# Rubric for Fluency
fluency_rubric = {
  "criteria": "Is the text fluent and easy to read, considering it is written by a Korean student?",
  "score1_description": "The text is disjointed and lacks fluency, making it hard to follow.",
  "score2_description": "The text has limited fluency with frequent awkward phrasing.",
  "score3_description": "The text is moderately fluent, with some awkward phrasing but generally easy to follow.",
  "score4_description": "The text is fluent with smooth transitions and rare awkward phrases.",
  "score5_description": "The text is highly fluent, with natural and smooth expression throughout."
}

# Rubric for Coherence
coherence_rubric = {
  "criteria": "Is the text coherent and logically organized, considering it is written by a Korean student?",
  "score1_description": "The text is incoherent and lacks logical organization, making it difficult to understand.",
  "score2_description": "The text shows some coherence but contains several disjointed ideas and poor organization.",
  "score3_description": "The text is generally coherent with a logical flow, though minor lapses in organization may occur.",
  "score4_description": "The text is coherent and well-organized with clear connections between ideas.",
  "score5_description": "The text is highly coherent, with a strong logical structure and seamless organization."
}

# Rubric for Consistency
consistency_rubric = {
  "criteria": "Is the text consistent in terms of style, tone, and tense, considering it is written by a Korean student?",
  "score1_description": "The text is inconsistent in style, tone, and tense, leading to confusion.",
  "score2_description": "The text shows occasional inconsistencies in style, tone, and tense.",
  "score3_description": "The text is mostly consistent in style, tone, and tense, with minor lapses.",
  "score4_description": "The text is consistent in style, tone, and tense, with rare inconsistencies.",
  "score5_description": "The text is highly consistent in style, tone, and tense throughout."
}

# Rubric for Relevance
relevance_rubric = {
  "criteria": "Is the text relevant to the given instruction or topic, considering it is written by a Korean student?",
  "score1_description": "The text is often irrelevant to the instruction, with significant off-topic content.",
  "score2_description": "The text addresses the instruction but includes some irrelevant content.",
  "score3_description": "The text is mostly relevant to the instruction, with minor deviations.",
  "score4_description": "The text is relevant to the instruction, with rare off-topic content.",
  "score5_description": "The text is highly relevant to the instruction, staying focused and on-topic throughout."
}

rubric_list = [grammaticality_rubric, fluency_rubric, coherence_rubric, consistency_rubric, relevance_rubric]
rubric_name = ["Grammaticality", "Fluency", "Coherence", "Consistency", "Relevance"]


tmp_feedback_results = []
tmp_score_results = []
for rn,rubric_data in zip(rubric_name,rubric_list):
    score_rubric = SCORE_RUBRIC_TEMPLATE.format(**rubric_data)

    feedback_list, score_list = judge.absolute_grade(
        instructions=instructions,
        responses=responses,
        rubric=score_rubric
    )
    tmp_feedback_results.append(feedback_list)
    tmp_score_results.append(score_list)

    print(f"{rn} is done!")
    
results = []
for inst_idx,d in enumerate(data):
    for crit_idx,rn in enumerate(rubric_name):
        d[f"{rn} Feedback"] = tmp_feedback_results[crit_idx][inst_idx]
        d[f"{rn} Score"] = tmp_score_results[crit_idx][inst_idx]
    results.append(d)

        
with open('./evaluation_results.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)