from collections import Counter
import multiprocessing
import itertools
import os
import re
import scipy as sp
import sys
import time
#from tkinter import *
#from tkinter.filedialog import askopenfilename
import warnings

import numpy as np
import pandas as pd
import xlsxwriter

class Ngram(object):

    #English, Spanish, Internet Stopwords
    DEFAULT_STOP_WORDS = {"a","able","about","above","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","after","afterwards","again","against","ah","all","almost","alone","along","already","also","although","always","am","among","amongst","an","and","announce","another","any","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","are","aren","arent","arise","around","as","aside","ask","asking","at","auth","available","away","awfully","b","back","be","became","because","become","becomes","becoming","been","before","beforehand","begin","beginning","beginnings","begins","behind","being","believe","below","beside","besides","between","beyond","biol","both","brief","briefly","but","by","c","ca","came","can","cannot","can't","cause","causes","certain","certainly","co","com","come","comes","contain","containing","contains","could","couldnt","d","date","did","didn't","different","do","does","doesn't","doing","done","don't","down","downwards","due","during","e","each","ed","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","especially","et","et-al","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","except","f","far","few","ff","fifth","first","five","fix","followed","following","follows","for","former","formerly","forth","found","four","from","further","furthermore","g","gave","get","gets","getting","give","given","gives","giving","go","goes","gone","got","gotten","h","had","happens","hardly","has","hasn't","have","haven't","having","he","hed","hence","her","here","hereafter","hereby","herein","heres","hereupon","hers","herself","hes","hi","hid","him","himself","his","hither","home","how","howbeit","however","hundred","i","id","ie","if","i'll","im","immediate","immediately","importance","important","in","inc","indeed","index","information","instead","into","invention","inward","is","isn't","it","itd","it'll","its","itself","i've","j","just","k","keep","kept","keeps","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","line","little","'ll","look","looking","looks","ltd","m","made","mainly","make","makes","many","may","maybe","me","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","more","moreover","most","mostly","mr","mrs","much","mug","must","my","myself","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need","needs","neither","never","nevertheless","new","next","nine","ninety","no","nobody","non","none","nonetheless","noone","nor","normally","nos","not","noted","nothing","now","nowhere","o","obtain","obtained","obviously","of","off","often","oh","ok","okay","old","omitted","on","once","one","ones","only","onto","or","ord","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","owing","own","p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","re","readily","really","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","s","said","same","saw","say","saying","says","sec","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","she","shed","she'll","shes","should","shouldn't","show","showed","shown","showns","shows","significant","significantly","similar","similarly","since","six","slightly","so","some","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","such","sufficiently","suggest","sup","sure","take","t","taken","taking","tell","tends","th","than","thank","thanks","thanx","that","that'll","thats","that've","the","their","theirs","them","themselves","then","thence","there","thereafter","thereby","thered","therefore","therein","there'll","thereof","therere","theres","thereto","thereupon","there've","these","they","theyd","they'll","theyre","they've","think","this","those","thou","though","thoughh","thousand","throug","through","throughout","thru","thus","til","tip","to","together","too","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","under","unfortunately","unless","unlike","unlikely","until","unto","up","upon","ups","us","use","used","useful","usefully","usefulness","uses","using","usually","v","value","various","'ve","very","via","viz","vol","vols","vs","w","want","wants","was","wasnt","way","we","wed","welcome","we'll","went","were","werent","we've","what","whatever","what'll","whats","when","whence","whenever","where","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","which","while","whim","whither","who","whod","whoever","whole","who'll","whom","whomever","whos","whose","why","widely","willing","wish","with","within","without","wont","words","world","would","wouldnt","www","x","y","yes","yet","you","youd","you'll","your","youre","yours","yourself","yourselves","you've","z","zero","él","ésta","éstas","éste","éstos","última","últimas","último","últimos","a","añadió","aún","actualmente","adelante","además","afirmó","agregó","ahí","ahora","al","algún","algo","alguna","algunas","alguno","algunos","alrededor","ambos","ante","anterior","antes","apenas","aproximadamente","aquí","así","aseguró","aunque","ayer","bajo","bien","buen","buena","buenas","bueno","buenos","cómo","cada","casi","cerca","cierto","cinco","comentó","como","con","conocer","consideró","considera","contra","cosas","creo","cual","cuales","cualquier","cuando","cuanto","cuatro","cuenta","da","dado","dan","dar","de","debe","deben","debido","decir","dejó","del","demás","dentro","desde","después","dice","dicen","dicho","dieron","diferente","diferentes","dijeron","dijo","dio","donde","dos","durante","e","ejemplo","el","ella","ellas","ello","ellos","embargo","en","encuentra","entonces","entre","era","eran","es","esa","esas","ese","eso","esos","está","están","esta","estaba","estaban","estamos","estar","estará","estas","este","esto","estos","estoy","estuvo","ex","existe","existen","explicó","expresó","fin","fue","fuera","fueron","gran","grandes","ha","había","habían","haber","habrá","hace","hacen","hacer","hacerlo","hacia","haciendo","han","hasta","hay","haya","he","hecho","hemos","hicieron","hizo","hoy","hubo","igual","incluso","indicó","informó","junto","la","lado","las","le","les","llegó","lleva","llevar","lo","los","luego","lugar","más","manera","manifestó","mayor","me","mediante","mejor","mencionó","menos","mi","mientras","misma","mismas","mismo","mismos","momento","mucha","muchas","mucho","muchos","muy","nada","nadie","ni","ningún","ninguna","ningunas","ninguno","ningunos","no","nos","nosotras","nosotros","nuestra","nuestras","nuestro","nuestros","nueva","nuevas","nuevo","nuevos","nunca","o","ocho","otra","otras","otro","otros","para","parece","parte","partir","pasada","pasado","pero","pesar","poca","pocas","poco","pocos","podemos","podrá","podrán","podría","podrían","poner","por","porque","posible","próximo","próximos","primer","primera","primero","primeros","principalmente","propia","propias","propio","propios","pudo","pueda","puede","pueden","pues","qué","que","quedó","queremos","quién","quien","quienes","quiere","realizó","realizado","realizar","respecto","sí","sólo","se","señaló","sea","sean","según","segunda","segundo","seis","ser","será","serán","sería","si","sido","siempre","siendo","siete","sigue","siguiente","sin","sino","sobre","sola","solamente","solas","solo","solos","son","su","sus","tal","también","tampoco","tan","tanto","tenía","tendrá","tendrán","tenemos","tener","tenga","tengo","tenido","tercera","tiene","tienen","toda","todas","todavía","todo","todos","total","tras","trata","través","tres","tuvo","un","una","unas","uno","unos","usted","va","vamos","van","varias","varios","veces","ver","vez","y","ya","yo", 'full', "http", "https", 'com', 'edu', 'www', 'follow','credit', 'tasty', 'bzfd', 'videos'}
    
    COLUMNS_TO_ANALYZE = ['Category', 'Comments', 'Creator', 'Creator_Country', 
                          'Duration (seconds)', 'ER30', 'ER7', 
                          'Facebook_Comments','Facebook_Likes', 
                          'Facebook_Shares', 'Facebook_Total_Engagements', 
                          'Platform', 'Published_Date', 'Topics', 
                          'Total_Engagements', 'V30', 'V7', 'Video_Title', 
                          'Video_URL', 'Views', 'Likes']

    COLUMNS_TO_AVERAGE = ['Comments', 'Duration (seconds)' , 'ER30', 'ER7', 
                          'Facebook_Comments', 'Facebook_Likes', 
                          'Facebook_Shares', 'Facebook_Total_Engagements', 
                          'Total_Engagements', 'V30', 'V7', 'Views', 'Likes']

    COLUMNS_TO_SUMMARIZE = ['Category', 'Creator', 'Creator_Country', 
                            'Platform', 'Topics']

    CREATOR_COLUMN_TO_FILTER = 'Creator'

    TITLE_COLUMN = 'Video_Title'

    PLATFORM_COLUMN = 'Platform'

    REGEX_PATTERN = re.compile(r'[a-z]{3,}')

    CORES = multiprocessing.cpu_count()

    def __init__(self, df, set_ngram=2, title_cutoff=None, 
                 add_stopwords={}, 
                 filter_creator_names_out=True):
        self.df = df
        self.__ngram = set_ngram
        self.__title_cutoff = title_cutoff
        self.__stop_words = Ngram.DEFAULT_STOP_WORDS.union(add_stopwords)
        self.__filter_creator_names_out = filter_creator_names_out
        self.raw_ngram = self.df_to_ngram()
        self.ngram = self.calc_and_summarize()

    def df_to_ngram(self):
        def ngram_dict():
            ngram_dict = {}
            for column in Ngram.COLUMNS_TO_ANALYZE:
                ngram_dict[column] = {}
            ngram_dict['index'] = {}
            return ngram_dict

        def tuple_to_named_series(tup):
            index = ['index'] + list(df.columns)
            series = pd.Series(tup,index=index)
            return series

        def filter_title_words():
            words = str(row[Ngram.TITLE_COLUMN]).lower().split(' ')
            regex_words_list = []
            pattern = Ngram.REGEX_PATTERN

            for word in words:
                regex_words = re.findall(pattern, word)
                for regex_word in regex_words:
                    regex_words_list.append(regex_word)

            regex_words = set(regex_words_list)
            regex_words = regex_words.difference(self.__stop_words)

            if self.__filter_creator_names_out:
                creators = list(
                                set(
                                    df[Ngram.CREATOR_COLUMN_TO_FILTER].tolist()
                                    )
                                )

                words = [str(creator).split(' ') for creator in creators]
                words = [item for sublist in words 
                                  for item in sublist]
                words_in_creator_names = set(words)
                regex_words = regex_words.difference(words_in_creator_names)

            cleaned_words = list(regex_words)

            if self.__title_cutoff:
                cleaned_words = cleaned_words[0:self.__title_cutoff]

            return cleaned_words

        def get_ngrams(words_list, n=2):
            ngram_iter = itertools.combinations(words_list,n)
            ngram_list = []
            for ngram in ngram_iter: #order bigrams so combination only has one order it will append to dict
                ngram = sorted(ngram)
                ngram = tuple(ngram)
                if n ==1:
                    ngram = ngram[0]
                ngram_list.append(ngram)
            return ngram_list

        def add_ngram_to_dict():
            try:
                ngram_dict[column][ngram].append(row[column])
            except KeyError:
                ngram_dict[column][ngram] = []
                ngram_dict[column][ngram].append(row[column])

        def sort_by_count(df):
            df['word_count'] = df['index'].apply(lambda x: len(x))
            df = df.sort_values(by='word_count', ascending=False)
            return df


        df = self.df.copy()
        df.drop_duplicates([Ngram.TITLE_COLUMN])
        ngram_dict = ngram_dict()

        for tup in df.itertuples():
            row = tuple_to_named_series(tup)
            relevent_words_list = filter_title_words()
            ngram_list = get_ngrams(relevent_words_list, self.__ngram)
            for ngram in ngram_list:
                for column in ngram_dict.keys():
                    if not pd.isnull(row[column]):
                        add_ngram_to_dict()

        ngram_df = pd.DataFrame(ngram_dict)
        ngram_df = sort_by_count(ngram_df)
        return ngram_df


    def calc_and_summarize(self):

        def df_averager(agg_func = sp.nanmean):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                for column in Ngram.COLUMNS_TO_AVERAGE:
                    column_name = 'mean_'+str(column)
                    df[column_name] = df[column].apply(lambda x: agg_func(x))

        def pandaCounter(x):
            if isinstance(x, list):
                return dict(Counter(x))
            else:
                return x
            
        df = self.raw_ngram.copy()
        
        for column in Ngram.COLUMNS_TO_SUMMARIZE:
            df[column] = df[column].apply(pandaCounter)

        df_averager(agg_func=sp.nanmean)
        df_averager(agg_func=sp.nanmedian)
        df = df.drop(Ngram.COLUMNS_TO_AVERAGE, axis=1)

        df = df.join(pd.DataFrame(df[Ngram.PLATFORM_COLUMN].to_dict()).T)

        return df





def printProgress (iteration, total, prefix = '', suffix = '', 
                   decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()




