import requests
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pandas as pd
import nltk
from utils import scrape_mental_health_articles, preprocess_articles, generate_embeddings

class RAG:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/distilgpt2"
        self.headers = {"Authorization": "Bearer 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"}
        self.index, self.chunks = self.setup_vector_db()

    def setup_vector_db(self):
        urls = [
            "https://www.psychologytoday.com/us",
            "https://www.nami.org/Blogs",
            "https://www.mentalhealth.gov/blog"
        ]
        articles = scrape_mental_health_articles(urls)
        chunks = preprocess_articles(articles)
        embeddings = generate_embeddings(chunks)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        return index, chunks

    
    
    async def process_user_query(self, query):
        # Encode the query
        query_embedding = SentenceTransformer('all-MiniLM-L6-v2').encode([query])
        
        # Search the FAISS index
        k = 3
        distances, indices = self.index.search(query_embedding, k)
        
        # Get relevant chunks
        context = "\n".join([self.chunks[i][1] for i in indices[0]])
        
        # Construct the prompt for the LLM
        prompt = f"""User query: {query}
        Based on the following relevant information, provide a helpful response and suggest which articles might be most useful:
        {context}
        """
        
        # Make a request to the LLM API
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": prompt})
        
        try:
            response_json = response.json()
            
            if 'error' in response_json:
                raise ValueError(f"Error from API: {response_json['error']}")
            
            # Extract the generated text from the response
            if isinstance(response_json, list) and len(response_json) > 0:
                response_text = response_json[0].get("generated_text", "")
            else:
                response_text = ""
            
            # Remove the prompt text from the response if it still contains it
            response_text = response_text.replace(prompt.strip(), "").strip()
            
        except (KeyError, IndexError, ValueError) as e:
            print(f"Error processing response: {e}")
            print(f"Response content: {response.content}")
            return "There was an error processing your request. Please try again later."
        
        # Create a list of relevant articles
        article_urls = [self.chunks[i][0] for i in indices[0]]
        
        # Format the response
        formatted_response = {
            "response": response_text,
            "relevant_articles": article_urls
        }
        
        return formatted_response




class Classification:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = self.train_classification_model()

    def train_classification_model(self):
        df = pd.read_csv(self.data_path)
        X = df['Tweet']
        y = df['Suicide']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        vectorizer = SentenceTransformer('all-MiniLM-L6-v2')
        X_train_emb = vectorizer.encode(X_train.tolist())
        X_test_emb = vectorizer.encode(X_test.tolist())

        clf = LogisticRegression()
        clf.fit(X_train_emb, y_train)

        y_pred = clf.predict(X_test_emb)
        print(classification_report(y_test, y_pred))

        return clf

    async def classify_text(self, text):
        vectorizer = SentenceTransformer('all-MiniLM-L6-v2')
        text_emb = vectorizer.encode([text])
        prediction = self.model.predict(text_emb)
        return prediction[0]
