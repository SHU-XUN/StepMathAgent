import json
from openai import OpenAI


def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            data.append(json.loads(line))
    return data


def write_jsonl(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def write_jsonl_line(data, file_path):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_client(model_name):
    api = read_json('./config/api.json')
    client = OpenAI(
        api_key=api[model_name]['api_key'],
        base_url=api[model_name]['base_url']
    )
    return client, api[model_name]['version']


def get_prompt(model):
    prompts = read_json('./config/prompts.json')
    return prompts[model]


def get_output(client, prompt, model):
    chat_completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return chat_completion.choices[0].message['content']
