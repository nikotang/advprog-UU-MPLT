from collections import defaultdict
from nltk.tokenize import word_tokenize
from random import sample

ENG_ALPHA = 'abcdefghijklmnopqrstuvwxyzé'
    

def get_lines(filename): 
    '''returns a list of items from each line in the lexicon or the corpus.'''
    items = []
    with open(filename, encoding='unicode-escape') as f: #I could not find an encoding to decode 'É'
        for line in f:
            line = line.strip()
            if '\x83' in line: #to decode 'É'
                line = line.replace('\x83', 'é')
            items.append(line)
    return items


class AutoCorrect:
    

    def __init__(self, word_list=get_lines('usenglish.txt'), alpha=ENG_ALPHA): 
        self.word_list = word_list
        self.alpha = alpha


    def insertion(self, word):
        #return a list of suggestions to alternative spellings for words with edit distance 1
        alternatives = []
        for i in range(len(word)+1):
            for letter in self.alpha:
                possible_word = word[:i] + letter + word[i:]
                if possible_word in self.word_list:
                    alternatives.append(possible_word)
        return alternatives

    
    def deletion(self, word):
        alternatives = []
        for i in range(len(word)):
            possible_word = word[:i] + word[i+1:]
            if possible_word in self.word_list:
                alternatives.append(possible_word)
        return alternatives

        
    def substitution(self, word):
        alternatives = []
        for i in range(len(word)):
            for letter in self.alpha:
                possible_word = word[:i] + letter + word[i+1:]
                if possible_word in self.word_list:
                    alternatives.append(possible_word)
        return alternatives

        
    def swapping(self, word):
        alternatives = []
        letters = list(word)
        for i in range(len(letters)-1):
            letters[i], letters[i+1] = letters[i+1], letters[i]
            possible_word = ''.join(letters)
            if possible_word in self.word_list:
                alternatives.append(possible_word)
        return alternatives

        
    def call_operation(self, word):
        #call the operation methods, put the elements of the lists in a set, and return that set.
        all_alternatives = set()
        all_alternatives.update(self.insertion(word))
        print(all_alternatives)
        all_alternatives.update(self.deletion(word))
        print(all_alternatives)
        all_alternatives.update(self.substitution(word))
        print(all_alternatives)
        all_alternatives.update(self.swapping(word))
        print(all_alternatives)
        return all_alternatives


    
def tokenize(sents):
    return [word_tokenize(sent) for sent in sents]
        
        
def populate_dict(tokenized_sents):
    bigram_frequency = defaultdict(int)
    for sent in tokenized_sents:
        for i in range(len(sent)-1): #last punctuation
            bigram_frequency[(sent[i].lower(), sent[i+1].lower())] += 1
    return bigram_frequency


def fetch_next(bigrams, input_word):
    suggestions = {}
    for (word, next_word), count in bigrams.items():
        if word == input_word:
            if len(suggestions) < 3:
                suggestions[count] = next_word
            elif count > min(suggestions): #only with a non-empty dictionry
                suggestions.pop(min(suggestions)) #remove the less frequent option 
                suggestions[count] = next_word
    return list(suggestions.values())
                

def main():
    a = AutoCorrect()
    #tie everything together, run until interrupted
    tokenized_sents = tokenize(get_lines('UNv1.0.testset.en'))
    bigrams = populate_dict(tokenized_sents)
    while True:
        word = input('Type a word: ')
        if word not in get_lines('usenglish.txt'): 
            suggestions = a.call_operation(word)
            if len(suggestions) > 3:
                print(sample(suggestions, 3))
            else:
                print(suggestions)
        else:
            print(fetch_next(bigrams, word))


if __name__ == "__main__":
    main()
    