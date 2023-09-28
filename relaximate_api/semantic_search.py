import numpy as np
from tqdm.auto import tqdm
from sklearn.neighbors import NearestNeighbors
import tensorflow as tf
# import tensorflow_hub as hub


class SemanticSearch:
    
    def __init__(self):
        # self.use = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')
        self.use = tf.saved_model.load("/Users/gauravkesharwani/Desktop/RelaxiMate/universal-sentence-encoder_4")
        self.fitted = False
    
    
    def fit(self, data, batch=1000, n_neighbors=5):
        self.data = data
        self.embeddings = self.get_text_embedding(data, batch=batch)
        print(len(self.embeddings))
        n_neighbors = min(n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        self.fitted = True
    
    
    def __call__(self, text, return_data=True):
        inp_emb = self.use([text])
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]
        
        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors
    
    
    def get_text_embedding(self, texts, batch=1000):
        embeddings = []
        for i in tqdm(range(0, len(texts), batch)):
            text_batch = texts[i:(i+batch)]
            emb_batch = self.use(text_batch)
            embeddings.append(emb_batch)
        embeddings = np.vstack(embeddings)
        return embeddings