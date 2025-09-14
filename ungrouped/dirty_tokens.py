import re
import tiktoken
from typing import Dict

enc = tiktoken.get_encoding("o200k_base")
# enc = tiktoken.get_encoding("cl100k_base")

def contains_chinese(text: str) -> bool:
    """
    Check if the input text contains any Chinese characters.
    Returns True if at least one Chinese character is found.
    """
    return re.search(r'[\u4e00-\u9fff]', text) is not None

def dump_long_token(n: int = -1) -> None:
    f"""
    Iterate through all tokens in the vocabulary.
    For each token, decode it and check if it contains Chinese characters.
    Collect tokens containing Chinese characters into a dictionary.
    Sort the tokens by the length of their decoded string (descending).
    Print the top {n} longest tokens containing Chinese characters.
    """
    token_dict: Dict[int, str] = {} 
    for i in range(enc.n_vocab):
        try:
            c = enc.decode([i])  # Decode the token id to string
            if contains_chinese(c):
                token_dict[i] = c  # Store token id and string if it contains Chinese
        except:
            pass  # Ignore decoding errors

    # Sort tokens by string length (descending) and take the top n
    long_tokens = list(sorted(token_dict.items(), key=lambda x: len(x[1]), reverse=True))[:n]
    with open("long_chinese_tokens.txt", "w", encoding="utf-8") as f:
        for i, c in long_tokens:
            f.write(f'{i}: "{c}"\n')
    print('Top tokens written to long_chinese_tokens.txt')

if __name__ == '__main__':
    dump_long_token()
