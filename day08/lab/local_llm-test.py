from sentence_transformers import SentenceTransformer

# Load the model locally
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# Sentences in different languages
sentences = [
    'How to run models locally',
    'Cách chạy mô hình trên máy cục bộ',  # Vietnamese
    'Wie man Modelle lokal ausführt'      # German
]

# Generate embeddings
embeddings = model.encode(sentences)
print(embeddings.shape) # Output: (3, 384)
print(embeddings)