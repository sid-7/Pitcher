import nltk, re, heapq, string
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from rake_nltk import Metric, Rake

MAX_TAGS = 5
MAX_SENTENCE = 5

def summarizer(text):
    article_text = text
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    sentence_list = sent_tokenize(article_text)
    if(len(sentence_list)<MAX_SENTENCE):
        return '. '.join(sentence_list)
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = '. '.join(summary_sentences)
    return summary


def extract_tags(text):
    result = string.punctuation + "’"
    stop_words = set(stopwords.words('english'))
    r = Rake(language='english')
    r = Rake(stopwords = stop_words, punctuations = result)
    r = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO)
    r = Rake(ranking_metric=Metric.WORD_DEGREE)
    r = Rake(ranking_metric=Metric.WORD_FREQUENCY)
    r = Rake(min_length=1, max_length=3)
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()[:MAX_TAGS]
