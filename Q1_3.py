import os
import string
import pickle

stopwords = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and",
    "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
    "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
}



def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stopwords]
    return tokens

def create_positional_index(input_dir):
    positional_index = {}
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                tokens = preprocess_text(content)
                for position, token in enumerate(tokens):
                    if token not in positional_index:
                        positional_index[token] = {}
                    if filename not in positional_index[token]:
                        positional_index[token][filename] = []
                    positional_index[token][filename].append(position)
    return positional_index

def save_positional_index(index, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(index, file)

def load_positional_index(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def process_phrase_query(query, positional_index):
    preprocessed_query = preprocess_text(query)
    if not preprocessed_query:
        return 0, []
    
    initial_docs = positional_index.get(preprocessed_query[0], {})
    
    valid_docs = {}
    for doc, positions in initial_docs.items():
        for pos in positions:
            if all(doc in positional_index.get(term, {}) and pos + offset in positional_index[term][doc]
                   for offset, term in enumerate(preprocessed_query[1:], 1)):
                if doc not in valid_docs:
                    valid_docs[doc] = []
                valid_docs[doc].append(pos)
    
    return len(valid_docs), list(valid_docs.keys())

def main():
    positional_index_path = 'positional_index.pkl'
    positional_index = load_positional_index(positional_index_path)
    
    num_queries = int(input("Enter the number of queries: "))
    for i in range(num_queries):
        query = input(f"Enter phrase query {i+1}: ")
        preprocessed_query_tokens = preprocess_text(query)
        formatted_query = ' '.join(preprocessed_query_tokens)
        print(f"Processed phrase query {i+1}: {formatted_query}")
        
        num_docs, doc_names = process_phrase_query(query, positional_index)
        print(f"Number of documents retrieved for query {i+1} using positional index: {num_docs}")
        if num_docs > 0:
            print(f"Names of documents retrieved for query {i+1} using positional index: {', '.join(doc_names)}")
        else:
            print("No documents retrieved.")


input_dir = '/Users/vishnu/output_1.1'
inverted_index = create_positional_index(input_dir)
save_positional_index(inverted_index, 'positional_index.pkl')


main()
