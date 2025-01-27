# import nltk
# nltk.download('punkt_tab')
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer

# from data.english import englishStopWords


# LANGUAGE = "english"
# SENTENCES_COUNT = 10

# def summarizer_from_html():

#     url = "https://en.wikipedia.org/wiki/Automatic_summarization"
#     parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
#     # or for plain text files
#     # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
#     # parser = PlaintextParser.from_string("Check this out.", Tokenizer(LANGUAGE))
#     stemmer = Stemmer(LANGUAGE)

#     summarizer = Summarizer(stemmer)
#     summarizer.stop_words = get_stop_words(LANGUAGE)

#     for sentence in summarizer(parser.document, SENTENCES_COUNT):
#         print(sentence)

#     output:


# LANGUAGE = "english"
LANGUAGE = "norwegian"


def sumy_summarizer(text, maxSentences=10):
    # text = sys.argv[1]
    # maxSentences = int(sys.argv[2])
    # maxSentences = 10

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    # summarizer.stop_words = parse_stop_words(englishStopWords)

    summary = []
    for sentence in summarizer(parser.document, maxSentences):
        # print(sentence, "\n")
        summary.append(str(sentence))

    return summary


# from jpro_language_models.summarizers.sumymodule import sumy_summarizer

if __name__ == "__main__":
    textfilepath = "data/example-data.txt"
    with open(textfilepath, "r") as file:
        # Read the contents of the file
        text = file.read()

    summary = sumy_summarizer(text, maxSentences=10)
    for item in summary:
        print(item)
