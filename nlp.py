# If you import the complete module, then the program becomes heavy as it contains thousands of lines of codes
import nltk
from nltk.tokenize.regexp import RegexpTokenizer
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk import RegexpParser
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as guru
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from collections import Counter
import pandas as pd


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


def chuncking():
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
    tag_map = defaultdict(lambda: guru.NOUN)
    tag_map['J'] = guru.ADJ
    tag_map['V'] = guru.VERB
    tag_map['R'] = guru.ADV

    text = "guru99 is a totally new kind of learning experience."
    tokens = word_tokenize(text)
    lemma_function = WordNetLemmatizer()
    for token, tag in pos_tag(tokens):
        lemma = lemma_function.lemmatize(token, tag_map[tag[0]])
        print(token, "=>", lemma)


def wordnet_synonym():
    syns = guru.synsets("dog")
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
    counts = Counter(tag for word, tag in tags)
    print(counts)


def frequency_distribution():
    a = "Guru99 is the site where you can find the best tutorials for Software Testing     Tutorial, SAP Course for Beginners. Java Tutorial for Beginners and much more. Please     visit the site guru99.com and much more."
    words = nltk.tokenize.word_tokenize(a)
    fd = nltk.FreqDist(words)
    fd.plot()

frequency_distribution()