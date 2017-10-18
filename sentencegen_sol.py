import requests, string, random

''' pip install requests or pip3 install requests '''

hp_text = requests.get("http://www.glozman.com/TextPages/Harry%20Potter%201%20-%20Sorcerer's%20Stone.txt")

''' to print the whole corpus, run "print hp_text.text" '''

all_words = {}
text = hp_text.text
translator = str.maketrans('', '', string.punctuation)
text = text.translate(translator)

hp_words = [word.replace('"', '') for word in text.split()]
total_words_in_book = 0
for line in hp_words:
    for word in line.split():
        word = word.lower()
        total_words_in_book += 1
        if word not in all_words:
            all_words[word] = 1
        else:
            all_words[word] += 1
###
# First find the probability of a given unigram in the corpus; P(w_i)
###
unigram_probs = {}
for word in all_words.keys():
    ''' probabilty = # occurrences/total # words '''
    unigram_probs[word] = (all_words[word]/total_words_in_book)
def unigram(w1):
    return unigram_probs[w1.lower()]

###
# Now find all bigrams in the corpus and order them from most popular
# to least; P(w_i | w_j)
# hint: sorting based on probabilty/frequency
###

bigram_probs = {}

def all_bigrams():
    for i in range(len(hp_words)-1):
        key = (hp_words[i], hp_words[i+1])
        if key in bigram_probs.keys():
            bigram_probs[key] += 1
        else:
            bigram_probs[key] = 1
all_bigrams()
bigram_probs = sorted(bigram_probs.items(), key=lambda pair: -pair[1])

# get 20 most popular bigrams
print(bigram_probs[:20])

###
# Find the probability of a specific bigram in the corpus; P(w_i | w_j)
###

def get_bigram(w1, w2):
    w1 = w1.lower()
    w2 = w2.lower()
    w1_and_w2 = w1 + " " + w2
    count = text.lower().count(w1_and_w2)
    return count/all_words[w1]
# print(get_bigram("sobbed", "Hagrid"))

###
# Sentence prediction/generation
###

# randomly generate the first word of your sentence
unique_words = [key for key in all_words.keys()]
idx = random.randrange(0, len(unique_words), 1)
start_word = unique_words[idx]


# generate a sentence given a word and a length of the sentence
# hint: define a function which chooses the next word in your sentence
#       based on weighted probabilites of bigrams

def get_sentence(word, l=20):
    for i in range(l):
        print(word, " ", end="")
        second_word_options = [e for e in bigram_probs if e[0][0] == word]
        if not second_word_options:
            break
        word = weighted_choice(second_word_options)[1]
    print()

def weighted_choice(second_word_options):
    total = sum(weight for (word, weight) in second_word_options)
    threshold = random.uniform(0, total)
    current_weight = 0
    for (word, weight) in second_word_options:
        if current_weight + weight > threshold:
            return word
        ''' more likely to choose the next word then'''
        current_weight += weight

get_sentence(start_word, 15)

