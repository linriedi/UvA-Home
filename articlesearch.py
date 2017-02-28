import re
import math
import operator
import newsextractor
import datetime
from collections import Counter
from difflib import SequenceMatcher

word = re.compile(r'\w+')

class ArticleSearch(object):
    """
    Searches a given list of articles for a search term with some parameters
    """

    def __init__(self, article_list, sources=None):
        """
        Init
        @param article_list List of articles generated by NewsExtractor().build_all()
        """
        self.article_list = article_list.news

    def search(self, search_term, date1=None, date2=None, place=None, sources=None):
        """
        Search function that handles parameters
        @param search_term The string to be searched in tags and titles of the articles
        @param date1 Longest date
        @param date2 Latest date
        @param place Location of news
        @param sources What sources the news will be returned from
        """
        if sources is None:
            sources = newsextractor.NewsExtractor().supported_news_papers

        min_date = datetime.datetime.fromtimestamp(0) if date1 is None else date1
        max_date = datetime.datetime.now() if date2 is None else date2

        search_term_vec = self.text_to_vector(search_term.lower())

        scored_articles = []
        for article in self.article_list:

            if article.published == '' or not (min_date <= article.published <= max_date):
                continue

            if not article.source in sources:
                continue
            if place is not None:
                place_found = False
                for k in article.keywords: # search the full text maybe?
                    if self.place.substring(k.lower()):
                        place_found = True
                        break
                if not place_found:
                    break

            vec2 = self.text_to_vector(article.title.lower())
            # highest_score = self.similar(search_term_vec, vec2) # sum word similarity method
            highest_score = self.get_cosine(search_term_vec, vec2) # cosine similarity method
            for keyword in article.keywords:
                vec2 = self.text_to_vector(keyword)
                # score = self.similar(search_term_vec, vec2) # sum word similarity method
                score = self.get_cosine(search_term_vec, vec2) # cosine similarity method
                if score > highest_score:
                    highest_score = score
            scored_articles.append([article, highest_score])
        return sorted(scored_articles, key=operator.itemgetter(1), reverse=True)

    def get_cosine(self, vec1, vec2):
        """
        Get the similarity between the strings vec1 and vec2.
        @param vec1 string 1
        @param vec2 string 2
        """
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
        else:
            intersection = set(vec1.keys() & vec2.keys())
            numerator = sum([(vec1[x] * vec2[x]) for x in intersection])
            return float(numerator) / denominator

    def text_to_vector(self, text):
        """
        Split string with /w
        @param text String to be split
        """
        global word
        return Counter(word.findall(text)) # cosine similarity method

    def similar(self, word1, word2):
        """
        Check the similarity between two strings, in case of wrong spelling
        @param word1 string1
        @param word2 string2
        """
        word1 = list(word1)
        word2 = list(word2)
        length_word1 = len(word1)
        length_word2 = len(word2)
        if length_word1 == 0 or length_word2 == 0: return 0
        score = 0
        for i in range(length_word2-length_word1):
            for j in range(length_word1):
                temp_score = SequenceMatcher(None, word1[j], word2[i+j]).quick_ratio()
                if temp_score > 0.9:
                    score += temp_score
        return score/(length_word2+length_word1)