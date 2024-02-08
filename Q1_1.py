import os
import string

input_dir = '/Users/vishnu/text_files'
output_dir = '/Users/vishnu/output_1.1'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

stopwords = set([
   "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and",
    "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
    "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
])

def preprocess_text(text, filename="", print_steps=False):
    if print_steps:
        print(f"Processing file: {filename}")
    
    # a. Lowercase the text
    text_lower = text.lower()
    if print_steps:
        print("a. After lowercasing:")
        print(text_lower[:500])
    
    # b. Tokenize and remove punctuation
    text_no_punctuation = text_lower.translate(str.maketrans('', '', string.punctuation))
    tokens = text_no_punctuation.split()
    if print_steps:
        print("\nb. After tokenization and removing punctuation:")
        print(" ".join(tokens[:50]))
    
    # c. Remove stopwords
    tokens_no_stopwords = [word for word in tokens if word not in stopwords]
    if print_steps:
        print("\nc. After removing stopwords:")
        print(" ".join(tokens_no_stopwords[:50]))
    
    # d. (and e.) Remove blank space tokens
    tokens_no_blanks = [token for token in tokens_no_stopwords if token.strip()]
    if print_steps:
        print("\nd. After removing blank space tokens:")
        print(" ".join(tokens_no_blanks[:50]))
    
    return ' '.join(tokens_no_blanks)

files_processed = 0
for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        print_steps = files_processed < 5
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            preprocessed_content = preprocess_text(content, filename=filename, print_steps=print_steps)
            
            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(preprocessed_content)
        
        if print_steps:
            print("\n================================\n")
        
        files_processed += 1
print(f"Preprocessing completed for all files. Total files processed: {files_processed}")