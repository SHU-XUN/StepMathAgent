import json
import re
from tqdm import tqdm
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from utils import *


data_path = "./output/**.jsonl"
data = read_jsonl(data_path)

model_scores = []
gold_scores = []
new_data = []

for d in data:
    o_d = d
    text = d['agent_output']
    pattern = re.compile(r'{(?:[^{}]|(?R))*}', re.DOTALL)
    matches = pattern.findall(text)
    if matches:
        json_str = matches[-1]
        json_str = json_str.replace('\\', '\\\\')
        try:
            parsed_json = json.loads(json_str)
        except json.JSONDecodeError as e:
            try:
                json_str = json_str.replace('\n', '')
                parsed_json = json.loads(json_str)
            except json.JSONDecodeError as e:
                parsed_json = json.loads(text)
        model_scores.append(parsed_json['最终得分'])
    gold_scores.append(d['gold_score'])
    o_d['agent_step'] = parsed_json
    o_d['agent_score'] = int(parsed_json['最终得分'])
    o_d['agent_chain'] = parsed_json['错误链']
    new_data.append(o_d)


print('gold scores:', sum(gold_scores)/len(gold_scores))
print('model scores:', sum(model_scores)/len(model_scores))


def overlap_rate(y_true, y_pred):
    total = len(y_true)
    correct_matches = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    return correct_matches / total


correlation, _ = pearsonr(gold_scores, model_scores)
print(f"Corr: {correlation}")
mse = mean_squared_error(gold_scores, model_scores)
print(f"MSE: {mse}")
overlap = overlap_rate(gold_scores, model_scores)
print(f"OR: {overlap}")
