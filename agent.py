import json
from tqdm import tqdm
from utils import *


api_name = "GPT-4o"
model_name = "StepMathAgent"
data_path = "./data/stepmath.jsonl"
output_path = "./output/" + api_name + '_' + model_name + ".jsonl"

client, version = get_client(api_name)
prompt_init = get_prompt(model_name)
data = read_jsonl(data_path)


for d in tqdm(data):
    o_d = d
    if d['answers']:
        prompt = prompt_init + '\n\n问题：' + d['question'] + '\n\n参考答案：' + str(d['answers'][0]) + '\n\n回复内容：' + d['model_output']
    else:
        prompt = prompt_init + '\n\n问题：' + d['question'] + '\n\n回复内容：' + d['model_output']
    output = get_output(client, prompt, version)
    # IF AGENT
    o_d['agent_output'] = output
    # IF BASELINE
    # o_d['baseline_output'] = output
    write_jsonl_line(o_d, output_path)