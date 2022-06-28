import sys
from collections import defaultdict
from bubble_sort import bubble_sort


def build_dict(lexicon):
    '''builds a dictionary where the key is a string of sorted letters, and the value is a list of anagrams.'''
    anagram_dict = defaultdict(list) 
    for word in lexicon:
        sorted_c = bubble_sort(list(word))
        sorted_word = ''.join(sorted_c) #create a string of sorted letters
        if sorted_word not in anagram_dict:
            anagram_dict[sorted_word]
        anagram_dict[sorted_word].append(word)
    return anagram_dict
        

def search(anagram_dict, word):
    '''searches for the word in the anagram dictionary and prints the anagrams or otherwise.'''
    word = word.lower()
    sorted_c = bubble_sort(list(word)) #sorts the target word for the search
    sorted_word = ''.join(sorted_c)
    if sorted_word in anagram_dict and anagram_dict[sorted_word] != []:
        anagram_dict[sorted_word].remove(word)
        if anagram_dict[sorted_word]:
            print(anagram_dict[sorted_word])
    
    
def get_lexicon(filename):
    '''builds a list of the lexicon from the input file.'''
    lexicon = []
    with open(filename, encoding='utf8') as f:
        for line in f:
            line = line.strip()
            lexicon.append(line)
    return lexicon
    
            
def main():
    lexicon = get_lexicon('sv-utf8.txt')
    anagram_dict = build_dict(lexicon)
    word = str(sys.argv[1])
    search(anagram_dict, lexicon, word)
                   


if __name__ == "__main__":
    main()