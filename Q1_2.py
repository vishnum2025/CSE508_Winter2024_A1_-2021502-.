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


def create_inverted_index(input_dir):
    inverted_index = {}
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):  
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                tokens = preprocess_text(content)
                for token in tokens:
                    if token not in inverted_index:
                        inverted_index[token] = set()
                    inverted_index[token].add(filename)
    return inverted_index


def save_inverted_index(index, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(index, file)


def load_inverted_index(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def execute_operation(docs1, docs2, operation):
    """Execute a binary operation on two sets of documents."""
    if operation == 'AND':
        return docs1.intersection(docs2)
    elif operation == 'OR':
        return docs1.union(docs2)
    elif operation == 'AND NOT':
        return docs1 - docs2
    elif operation == 'OR NOT':
        return docs1 - docs2
    else:
        raise ValueError(f"Unknown operation: {operation}")

def process_query(queries, operations, inverted_index):
    """Process a query with multiple operations."""
    result = set()
    if queries:
        result = inverted_index.get(queries[0], set())
        for i, operation in enumerate(operations):
            if i < len(queries) - 1:  
                next_query_result = inverted_index.get(queries[i + 1], set())
                result = execute_operation(result, next_query_result, operation.strip())
    return result


def main():
    inverted_index_path = 'inverted_index.pkl'
    inverted_index = load_inverted_index(inverted_index_path)
    
    num_queries = int(input("Enter the number of queries: "))
    for i in range(1, num_queries + 1):
        query = input(f"Enter query {i}: ")
        operations_input = input("Enter operations separated by comma for query: ")
        operations = [op.strip() for op in operations_input.split(',')]
        preprocessed_query_tokens = preprocess_text(query)
        formatted_query = preprocessed_query_tokens[0] if preprocessed_query_tokens else ''
        for op, token in zip(operations, preprocessed_query_tokens[1:]):
            formatted_query += f" {op} {token}"
        result = process_query(preprocessed_query_tokens, operations, inverted_index)
        print(f"\nQuery {i}: {formatted_query}")
        print(f"Number of documents retrieved for query {i}: {len(result)}")
        if len(result) > 0:
            print(f"Names of the documents retrieved for query {i}: {', '.join(sorted(result))}")
        else:
            print("No documents retrieved.")

input_dir = '/Users/vishnu/output_1.1'
inverted_index = create_inverted_index(input_dir)
save_inverted_index(inverted_index, 'inverted_index.pkl')
main()
