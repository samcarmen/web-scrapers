# If you import the complete module, then the program becomes heavy as it contains thousands of lines of codes
import json
import nltk
from nltk.tokenize.regexp import RegexpTokenizer
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk import RegexpParser, wordnet
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from collections import Counter
import pandas as pd
from nltk.corpus import stopwords
from textblob import Word
import matplotlib


def tokenization():
    tokenizer = RegexpTokenizer(r'\w+')
    filterdText = tokenizer.tokenize('Hello Guru99, You have build a very good site and I love visiting your site.')
    print(filterdText)

    text = "God is Great! I won a lottery."
    print(word_tokenize(text))
    print(sent_tokenize(text))


def pos_tag():
    text = "learn php from guru99 and make study easy".split()
    print("After Split:", text)

    tokens_tag = pos_tag(text)
    print("After Token:", tokens_tag)

    patterns = """mychunk:{<NN.?>*<VBD.?>*<JJ.?>*<CC>?}"""
    chunker = RegexpParser(patterns)
    print("After Regex:", chunker)

    output = chunker.parse(tokens_tag)
    print("After Chunking", output)


def chunking():
    text = "learn php from guru99"
    tokens = nltk.word_tokenize(text)
    print(tokens)
    tag = nltk.pos_tag(tokens)
    print(tag)
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    cp  =nltk.RegexpParser(grammar)
    result = cp.parse(tag)
    print(result)
    result.draw()


def create_dataframe():
    lst = ['Geeks', 'For', 'Geeks', 'is',
          'portal', 'for', 'Geeks']

    # Calling DataFrame constructor on list
    df = pd.DataFrame(lst)
    print(df)


def stemming():
    sentence = "Hello Guru99, You have to build a very good site and I love visiting your site."
    words = word_tokenize(sentence)
    ps = PorterStemmer()
    for w in words:
        rootWord = ps.stem(w)
        print(rootWord)


def lemmatization():
    tag_map = defaultdict(lambda: wordnet.NOUN)
    tag_map['J'] = wordnet.ADJ
    tag_map['V'] = wordnet.VERB
    tag_map['R'] = wordnet.ADV

    text = "guru99 is a totally new kind of learning experience."
    tokens = word_tokenize(text)
    lemma_function = WordNetLemmatizer()
    for token, tag in pos_tag(tokens):
        lemma = lemma_function.lemmatize(token, tag_map[tag[0]])
        print(token, "=>", lemma)


def wordnet_synonym():
    syns = wordnet.synsets("dog")
    print(syns)


def wordnet_lexical():
    from nltk.corpus import wordnet
    synonyms = []
    antonyms = []

    for syn in wordnet.synsets("active"):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    print(set(synonyms))
    print(set(antonyms))


def tagging_sentence():
    text = "Hello Guru99, You have to build a very good site, and I love visiting your   site."
    sentence = nltk.sent_tokenize(text)
    for sent in sentence:
        print(nltk.pos_tag(nltk.word_tokenize(sent)))


def count_pos():
    text = " Guru99 is one of the best sites to learn WEB, SAP, Ethical Hacking and much more online."
    lower_case = text.lower()
    tokens = nltk.word_tokenize(lower_case)
    tags = nltk.pos_tag(tokens)
    counts = Counter(tag for word, tag in tags)  # Calculate the pos_tag of each token
    print(counts)


def frequency_distribution():
    a = "Guru99 is the site where you can find the best tutorials for Software Testing     " \
        "Tutorial, SAP Course for Beginners. Java Tutorial for Beginners and much more. Please" \
        "     visit the site guru99.com and much more."
    words = nltk.tokenize.word_tokenize(a)
    fd = nltk.FreqDist(words)
    fd.plot()


def bigram():
    text = "Guru99 is a totally new kind of learning experience."
    Tokens = nltk.word_tokenize(text)
    bigram = list(nltk.bigrams(Tokens))
    print("Bigrams: ", bigram)
    trigram = list(nltk.trigrams(Tokens))
    print("Trigrams: ", trigram)


def synonym_antonym():
    syn = wordnet.synsets("Teaching")
    print("Word and Type: ", syn[0].name())
    print("Synonym of teaching is: ", syn[0].lemmas()[0].name())
    print("The meaning of teaching is: ", syn[0].definition())
    print("Example of teaching: ", syn[0].examples())

    synonym = []
    for syn in wordnet.synsets("travel"):
        for lm in syn.lemmas():
            synonym.append(lm.name())
    print("Synonyms for travel are: ", synonym)

    antonym = []
    for syn in wordnet.synsets("increase"):
        for lm in syn.lemmas():
            if lm.antonyms():
                antonym.append(lm.antonyms()[0].name())
    print("Antonyms for increase are: ", antonym)


def implement_gensim():
    data = [{"tag": "welcome",
"patterns": ["Hi", "How are you", "Is any one to talk?", "Hello", "hi are you available"],
"responses": ["Hello, thanks for contacting us", "Good to see you here"," Hi there, how may I assist you?"]

        },
{"tag": "goodbye",
"patterns": ["Bye", "See you later", "Goodbye", "I will come back soon"],
"responses": ["See you later, thanks for visiting", "have a great day ahead", "Wish you Come back again soon."]
        },

{"tag": "thankful",
"patterns": ["Thanks for helping me", "Thank your guidance", "That's helpful and kind from you"],
"responses": ["Happy to help!", "Any time!", "My pleasure", "It is my duty to help you"]
        },
        {"tag": "hoursopening",
"patterns": ["What hours are you open?", "Tell your opening time?", "When are you open?", "Just your timing please"],
"responses": ["We're open every day 8am-7pm", "Our office hours are 8am-7pm every day", "We open office at 8 am and close at 7 pm"]
        },

{"tag": "payments",
"patterns": ["Can I pay using credit card?", " Can I pay using Mastercard?", " Can I pay using cash only?" ],
"responses": ["We accept VISA, Mastercard and credit card", "We accept credit card, debit cards and cash. Please don’t worry"]
        }
   ]

    data = json.load(data)
    df = pd.DataFrame(data)
    df['patterns'] = df['patterns'].apply(', '.join)

    stop = stopwords.words('english')
    df['patterns'] = df['patterns'].apply(lambda x: ' '.join(x.lower() for x in x.split()))
    df['patterns']= df['patterns'].apply(lambda x: ' '.join(x for x in x.split() if x not in string.punctuation)
    df['patterns'] = df['patterns'].str.replace('[^\w\s]', '')
    df['patterns'] = df['patterns'].apply(lambda x: ' '.join(x for x in x.split() if not x.isdigit()))
    df['patterns'] = df['patterns'].apply(lambda x: ' '.join(x for x in x.split() if not x in stop))
    df['patterns'] = df['patterns'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
synonym_antonym()
