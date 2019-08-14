import html2text
from time import time
from pathlib import Path
from nltk.corpus import stopwords
from alphabet_detector import AlphabetDetector
from nltk import word_tokenize
from nltk.book import FreqDist
from wordcloud import WordCloud, ImageColorGenerator
from matplotlib import pyplot as plt
from collections import OrderedDict
from PIL import Image
import numpy as np


class WordsCloudMaker:
    def __init__(self, **kwargs):
        self.__path_to_html = kwargs['path_to_html']
        self.__path_to_txt = '/'.join(self.__path_to_html.split('.')[:-1]) + '.txt'

        self.__path_to_mask = kwargs['path_to_mask']

        self.__custom_stopwords = kwargs.get('custom_stopwords', ())
        self.__min_word_len = kwargs.get('min_word_len', 3)
        self.__max_words = kwargs.get('max_words', 2000)
        self.__max_font_size = kwargs.get('max_font_size', 20)
        self.__enlargement_factor = kwargs.get('enlargement_factor', 4)


        print('#####################')

    def __html_to_raw_text(self):
        t_start = time()

        file = Path(self.__path_to_txt)

        if file.exists():
            print('Already converted to text!')
            with open(self.__path_to_txt, 'r') as f:
                text_string = f.read()
        else:
            print('Converting html to text...')

            text_maker = html2text.HTML2Text()
            text_maker.ignore_links = True
            text_maker.escape_snob = True
            text_maker.skip_internal_links = True
            text_maker.ignore_images = True
            text_maker.ignore_tables = True
            text_maker.ignore_emphasis = True

            file = open(self.__path_to_html, 'r')
            text_html = file.read()

            text_string = text_maker.handle(text_html)

            with open(self.__path_to_txt, 'w') as f:
                f.write(text_string)

        t_end = time()
        print("TIME = %.2f s" % (t_end - t_start))

        return text_string

    def __freqs_dict(self, raw_text):

        t_start = time()
        print('Making filtered text...')

        stopset = set(stopwords.words('russian'))
        ad = AlphabetDetector()

        tokens = word_tokenize(raw_text)
        tokens_filtered = [w.lower() for w in tokens
                           if w not in stopset
                           and w not in self.__custom_stopwords
                           and w.isalpha()
                           and len(w) >= self.__min_word_len
                           and ad.is_cyrillic(w)]


        freqs_tokenized_text = FreqDist(tokens_filtered)
        freqs_most_common = OrderedDict(freqs_tokenized_text.most_common(self.__max_words))

        res_text = ''
        for item in freqs_most_common.items():
            word = item[0]
            freq = item[1]
            for i in range(freq):
                res_text += word + ' '

        t_end = time()
        print("TIME = %.2f s" % (t_end - t_start))

        return res_text

    def __wordcloud(self, text_string):

        t_start = time()
        print('Plotting word_cloud...')

        mask = np.array(Image.open(self.__path_to_mask))

        wordcloud = WordCloud(height=self.__enlargement_factor*mask.shape[0],
                              width=self.__enlargement_factor*mask.shape[1],
                              mask=mask,
                              max_font_size=self.__max_font_size,
                              max_words=self.__max_words,
                              collocations=False,
                              background_color='white').generate(text_string)

        image_colors = ImageColorGenerator(mask)

        fig_width = 20
        fig_height = int(fig_width * mask.shape[0] / mask.shape[1])

        plt.figure(figsize=(fig_width, fig_height))
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
        plt.axis("off")
        plt.savefig('word_cloud.png', bbox_inches='tight', dpi=200)
        plt.show()

        t_end = time()
        print("TIME = %.2f s" % (t_end - t_start))

    def process(self):
        raw_text = self.__html_to_raw_text()
        res_text = self.__freqs_dict(raw_text)
        self.__wordcloud(res_text)

