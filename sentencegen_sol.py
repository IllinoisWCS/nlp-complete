import requests, string, random

''' pip install requests or pip3 install requests '''

hp_text = requests.get("http://www.glozman.com/TextPages/Harry%20Potter%201%20-%20Sorcerer's%20Stone.txt")

''' to print the whole corpus, run "print hp_text.text" '''

unique_words = {}
text = hp_text.text

# Remove punctation from text
translator = str.maketrans('', '', string.punctuation)
text = text.translate(translator)
# hp_words is a list of each word in the text
# (in order of appearance, duplicates included)
hp_words = [word.replace('"', '') for word in text.split()]
total_words_in_book = len(hp_words)

# Get the number of times of each word in the text appears
for line in hp_words:
    for word in line.split():
        word = word.lower()
        if word not in unique_words:
            unique_words[word] = 1
        else:
            unique_words[word] += 1
###
# First find the probability of a given unigram in the corpus; P(w_i)
###
unigram_probs = {}

def get_all_unigrams():
    for word in unique_words:
        # probabilty = # occurrences/total # words
        unigram_probs[word] = (unique_words[word]/total_words_in_book)

def unigram(w1):
    return unigram_probs[w1.lower()]

get_all_unigrams()
print(unigram("Harry"))

###
# Now find all bigrams in the corpus and order them from most popular
# to least; P(w_i | w_j)
# hint: sorting based on probabilty/frequency
###

bigram_counts = {}

def get_all_bigrams():
    for i in range(len(hp_words)-1):
        key = (hp_words[i].lower(), hp_words[i+1].lower())
        if key in bigram_counts:
            bigram_counts[key] += 1
        else:
            bigram_counts[key] = 1

get_all_bigrams()
bigram_counts_list = sorted(bigram_counts.items(), key=lambda pair: -pair[1])

# Get 20 most popular bigrams
print(bigram_counts_list[:20])

###
# Find the probability of a specific bigram in the corpus; P(w_i | w_j)
###

# Method 1: uses the bigram_counts dictionary
def get_bigram_1(w1, w2):
    w1 = w1.lower()
    w2 = w2.lower()
    w1_and_w2 = (w1, w2)
    return bigram_counts[w1_and_w2]/unique_words[w1]

# Method 2: doesn't use bigram_counts
def get_bigram_2(w1, w2):
    w1 = w1.lower()
    w2 = w2.lower()
    w1_and_w2 = w1 + " " + w2

    # count stores the number of times the substring
    # w1_and_w2 appears in the text
    count = text.lower().count(w1_and_w2)
    return count/unique_words[w1]

# Check equality

print("v1: ", get_bigram_1("sobbed", "hagrid"))
print("v2: ", get_bigram_2("sobbed", "Hagrid"))

###
# Sentence prediction/generation
###

# randomly generate the first word of your sentence
unique_words = [key for key in unique_words.keys()]
idx = random.randrange(0, len(unique_words), 1)
start_word = unique_words[idx]


# Generate a sentence given a word and a length of the sentence
# Hint: define a function which chooses the next word in your sentence
#       based on weighted probabilites of bigrams

def get_sentence(word, l=20):
    for i in range(l):
        print(word, " ", end="")
        second_word_options = [e for e in bigram_counts_list if e[0][0] == word]
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
