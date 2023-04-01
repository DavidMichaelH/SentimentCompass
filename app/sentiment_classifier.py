import requests
import os
import yaml

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_file = os.path.join(current_dir, "app.yaml")

    with open(yaml_file, "r") as f:
        config = yaml.safe_load(f)

    return config

def get_huggingface_api_details(config):
    api_key = config["env_variables"]["HUGGINGFACE_API_KEY"]
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {api_key}"}
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"

    return headers, api_url

config = load_config()
headers, api_url = get_huggingface_api_details(config)

def truncate_texts(texts, max_length=512):
    return [text[:max_length] for text in texts]

def sentiment_classifier(texts):
    texts = truncate_texts(texts)

    data = {"inputs": texts}
    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()

    results = response.json()
    sentiments = []

    for result in results:
        if result[0]['label'] == 'POSITIVE':
            sentiments.append({"label": "Supportive", "score": result[0]['score']})
        else:
            sentiments.append({"label": "Critical", "score": result[1]['score']})
        
    return sentiments
