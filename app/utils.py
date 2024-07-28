import requests
from bs4 import BeautifulSoup
import re
import nltk
from sentence_transformers import SentenceTransformer

def scrape_mental_health_articles(urls):
    articles = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for article in soup.find_all('article'):
            title = article.find('h2')
            content = article.find_all('p')
            
            if title and content:
                content_text = ' '.join([p.text for p in content])
                if re.search(r'\b(mental health|depression|anxiety|therapy)\b', 
                             title.text + ' ' + content_text, re.IGNORECASE):
                    articles.append({
                        'title': title.text.strip(),
                        'content': content_text.strip(),
                        'url': url
                    })
    return articles



def preprocess_articles(articles):
    nltk.download('punkt')
    chunks = []
    for article in articles:
        sentences = nltk.sent_tokenize(article['content'])
        for i in range(0, len(sentences), 3):
            chunk = ' '.join(sentences[i:i+3])
            chunks.append((article['url'], chunk))
    return chunks

def generate_embeddings(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([chunk for _, chunk in chunks])
    return embeddings
