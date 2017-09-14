from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import urllib2
from bs4 import BeautifulSoup


class FrequencySummarizer(object):
    """
    This class includes three methods:
        1. constructor
        2. function to calculate the frequency of words and store as a dictionary
        3. function to list out the top n sentences to represent the article
           by indentifying the sentences where most freq words reside
    """
    def __init__(self, min_cut=0.1, max_cut=0.9):
        """
        this member method, constructor, to initialize some
        thresholds to cut off two extremes, low frequency &
        high frequency words
        """
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('english') + list(punctuation))

    def _compute_frequencies(self, word_sent):
        freq = defaultdict(int)
        # to avoid KeyError arising, use defaultdict instead
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        m = float(max(freq.values()))
        print freq
        # normalization the frequency: 0 ~ 1
        for w in freq.keys():
            freq[w] = freq[w] / m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                del freq[w]
        return freq

    def summarize(self, text, n):
        sents = sent_tokenize(text)
        assert n <= len(sents)

        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)

        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = nlargest(n, ranking, key=ranking.get)
        return [sents[j] for j in sents_idx]

#########################################################

def get_only_text_washington_post_url(url):
    """
    This function takes in a URL only from WashingtonPost as an argument,
    and returns only the text parts of the article
    """
    page = urllib2.urlopen(url).read().decode('utf8')
    # download the URL
    soup = BeautifulSoup(page,'lxml')
    text = ' '.join(map(lambda p: p.text, soup.find_all('article')))
    soup2 = BeautifulSoup(text,'lxml')
    if soup2.find_all('p')!=[]:
        text = ' '.join(map(lambda p: p.text, soup2.find_all('p')))
    return soup.title.text, text

def main():
    Url = "https://www.washingtonpost.com/news/innovations/wp/2017/09/11/as-hurricane-irma-bore-down-tesla-gave-some-florida-drivers-more-battery-juice-heres-why-thats-a-big-deal/?utm_term=.4fab356d1e82"
    textOfUrl = get_only_text_washington_post_url(Url)
    sents = sent_tokenize(textOfUrl[1])
    word_sent = [word_tokenize(s.lower()) for s in sents]
    fs = FrequencySummarizer()
    freq_dict = fs._compute_frequencies(word_sent)
    summary = fs.summarize(textOfUrl[1],3)
    print textOfUrl, '\n'
    print freq_dict, '\n'
    print summary

if __name__ == '__main__':
    main()
