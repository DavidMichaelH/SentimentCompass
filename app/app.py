from flask import Flask, render_template, request
from fetch_comments import get_video_comments
from sentiment_classifier import sentiment_classifier
import numpy as np
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

def extract_video_id(url):
    parsed_url = urlparse(url)
    
    if "youtube.com" in parsed_url.netloc or "youtu.be" in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get("v")
        
        if video_id:
            return video_id[0]
    return None

def analyze_sentiments(comments):
    sentiments = sentiment_classifier(comments) 
            
    stats = {
        'total': len(comments),
        'positive': sum(1 for sentiment in sentiments if sentiment['label'] == 'Supportive'),
        'negative': sum(1 for sentiment in sentiments if sentiment['label'] == 'Critical'),
        'score': np.mean([sentiment['score'] for sentiment in sentiments]),
        'positive_percentage': 0,
        'negative_percentage': 0
    }
    
    if stats['total'] > 0:
        stats['positive_percentage'] = 100 * stats['positive'] / stats['total']
        stats['negative_percentage'] = 100 * stats['negative'] / stats['total']

    return sentiments, stats

@app.route('/', methods=['GET', 'POST'])
def index():
    comments = []
    sentiments = []
    stats = {
        'total': 0,
        'positive': 0,
        'negative': 0,
        'score': 0,
        'positive_percentage': 0,
        'negative_percentage': 0
    }

    if request.method == 'POST':
        video_url = request.form.get('video_url')
        video_id = extract_video_id(video_url)
        
        if video_id:
            comments = get_video_comments(video_id)
            sentiments, stats = analyze_sentiments(comments)

    return render_template('index.html', comments=zip(comments, sentiments), stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
