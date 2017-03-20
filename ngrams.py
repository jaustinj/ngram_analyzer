from collections import Counter
import itertools
import os
import re
import sys
import time
from tkinter import *
from tkinter.filedialog import askopenfilename
import warnings

import numpy as np
import pandas as pd
import scipy as sp
import xlsxwriter

def get_filename():
    '''Call opens Tk() gui to allow user to select a file
    '''
    filename = askopenfilename()
    return filename

def get_user_number(input_sentance, n=4):
    '''Prompts users with a message to select a number between a range.

    @params:
    imput_sentance  -required  :  ex:'please select number of words to include in ngram (1-3): '
    n               -required  :  ex:'n=3, only accepts user input of number between 1-3'
    '''
    number = None
    while number not in list(range(0,n+1)):
        number = input(input_sentance)
        try:
            number = int(number)
        except ValueError:
            continue
    return number

def get_user_stopwords():
    '''Asks users for a list of words, seperated by commas, that will be taken out of analysis 
    as stopwords'''
    user_input = input("List any words you don't want included, seperated by commas and no spaces (press enter when finished):  ")
    if user_input:
        user_input = user_input.split(',')
        return user_input
    else:
        return []

def initialize_stopwords_list(user_stopwords = []):
    '''returns a custom list of common English, Spanish, and Internet Stop Words'''
    if type(user_stopwords) is not type([]):
        raise ValueError('User Stopwords should be a list')

    english_stop_words = ["a","able","about","above","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","after","afterwards","again","against","ah","all","almost","alone","along","already","also","although","always","am","among","amongst","an","and","announce","another","any","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","are","aren","arent","arise","around","as","aside","ask","asking","at","auth","available","away","awfully","b","back","be","became","because","become","becomes","becoming","been","before","beforehand","begin","beginning","beginnings","begins","behind","being","believe","below","beside","besides","between","beyond","biol","both","brief","briefly","but","by","c","ca","came","can","cannot","can't","cause","causes","certain","certainly","co","com","come","comes","contain","containing","contains","could","couldnt","d","date","did","didn't","different","do","does","doesn't","doing","done","don't","down","downwards","due","during","e","each","ed","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","especially","et","et-al","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","except","f","far","few","ff","fifth","first","five","fix","followed","following","follows","for","former","formerly","forth","found","four","from","further","furthermore","g","gave","get","gets","getting","give","given","gives","giving","go","goes","gone","got","gotten","h","had","happens","hardly","has","hasn't","have","haven't","having","he","hed","hence","her","here","hereafter","hereby","herein","heres","hereupon","hers","herself","hes","hi","hid","him","himself","his","hither","home","how","howbeit","however","hundred","i","id","ie","if","i'll","im","immediate","immediately","importance","important","in","inc","indeed","index","information","instead","into","invention","inward","is","isn't","it","itd","it'll","its","itself","i've","j","just","k","keep","kept","keeps","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","line","little","'ll","look","looking","looks","ltd","m","made","mainly","make","makes","many","may","maybe","me","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","more","moreover","most","mostly","mr","mrs","much","mug","must","my","myself","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need","needs","neither","never","nevertheless","new","next","nine","ninety","no","nobody","non","none","nonetheless","noone","nor","normally","nos","not","noted","nothing","now","nowhere","o","obtain","obtained","obviously","of","off","often","oh","ok","okay","old","omitted","on","once","one","ones","only","onto","or","ord","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","owing","own","p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","re","readily","really","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","s","said","same","saw","say","saying","says","sec","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","she","shed","she'll","shes","should","shouldn't","show","showed","shown","showns","shows","significant","significantly","similar","similarly","since","six","slightly","so","some","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","such","sufficiently","suggest","sup","sure","take","t","taken","taking","tell","tends","th","than","thank","thanks","thanx","that","that'll","thats","that've","the","their","theirs","them","themselves","then","thence","there","thereafter","thereby","thered","therefore","therein","there'll","thereof","therere","theres","thereto","thereupon","there've","these","they","theyd","they'll","theyre","they've","think","this","those","thou","though","thoughh","thousand","throug","through","throughout","thru","thus","til","tip","to","together","too","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","under","unfortunately","unless","unlike","unlikely","until","unto","up","upon","ups","us","use","used","useful","usefully","usefulness","uses","using","usually","v","value","various","'ve","very","via","viz","vol","vols","vs","w","want","wants","was","wasnt","way","we","wed","welcome","we'll","went","were","werent","we've","what","whatever","what'll","whats","when","whence","whenever","where","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","which","while","whim","whither","who","whod","whoever","whole","who'll","whom","whomever","whos","whose","why","widely","willing","wish","with","within","without","wont","words","world","would","wouldnt","www","x","y","yes","yet","you","youd","you'll","your","youre","yours","yourself","yourselves","you've","z","zero"]
    spanish_stop_words = ["él","ésta","éstas","éste","éstos","última","últimas","último","últimos","a","añadió","aún","actualmente","adelante","además","afirmó","agregó","ahí","ahora","al","algún","algo","alguna","algunas","alguno","algunos","alrededor","ambos","ante","anterior","antes","apenas","aproximadamente","aquí","así","aseguró","aunque","ayer","bajo","bien","buen","buena","buenas","bueno","buenos","cómo","cada","casi","cerca","cierto","cinco","comentó","como","con","conocer","consideró","considera","contra","cosas","creo","cual","cuales","cualquier","cuando","cuanto","cuatro","cuenta","da","dado","dan","dar","de","debe","deben","debido","decir","dejó","del","demás","dentro","desde","después","dice","dicen","dicho","dieron","diferente","diferentes","dijeron","dijo","dio","donde","dos","durante","e","ejemplo","el","ella","ellas","ello","ellos","embargo","en","encuentra","entonces","entre","era","eran","es","esa","esas","ese","eso","esos","está","están","esta","estaba","estaban","estamos","estar","estará","estas","este","esto","estos","estoy","estuvo","ex","existe","existen","explicó","expresó","fin","fue","fuera","fueron","gran","grandes","ha","había","habían","haber","habrá","hace","hacen","hacer","hacerlo","hacia","haciendo","han","hasta","hay","haya","he","hecho","hemos","hicieron","hizo","hoy","hubo","igual","incluso","indicó","informó","junto","la","lado","las","le","les","llegó","lleva","llevar","lo","los","luego","lugar","más","manera","manifestó","mayor","me","mediante","mejor","mencionó","menos","mi","mientras","misma","mismas","mismo","mismos","momento","mucha","muchas","mucho","muchos","muy","nada","nadie","ni","ningún","ninguna","ningunas","ninguno","ningunos","no","nos","nosotras","nosotros","nuestra","nuestras","nuestro","nuestros","nueva","nuevas","nuevo","nuevos","nunca","o","ocho","otra","otras","otro","otros","para","parece","parte","partir","pasada","pasado","pero","pesar","poca","pocas","poco","pocos","podemos","podrá","podrán","podría","podrían","poner","por","porque","posible","próximo","próximos","primer","primera","primero","primeros","principalmente","propia","propias","propio","propios","pudo","pueda","puede","pueden","pues","qué","que","quedó","queremos","quién","quien","quienes","quiere","realizó","realizado","realizar","respecto","sí","sólo","se","señaló","sea","sean","según","segunda","segundo","seis","ser","será","serán","sería","si","sido","siempre","siendo","siete","sigue","siguiente","sin","sino","sobre","sola","solamente","solas","solo","solos","son","su","sus","tal","también","tampoco","tan","tanto","tenía","tendrá","tendrán","tenemos","tener","tenga","tengo","tenido","tercera","tiene","tienen","toda","todas","todavía","todo","todos","total","tras","trata","través","tres","tuvo","un","una","unas","uno","unos","usted","va","vamos","van","varias","varios","veces","ver","vez","y","ya","yo"]
    internet_stop_words = ['episode','followme','unilad', 'video', 'videos', 'comment', 'like', 'ladbible', 'theladbible', 'download', 'app', 'lmao', 'free', 'link', 'bio', 'tag', 'full', "http", "https", 'com', 'edu', 'www', 'follow','credit', 'tasty', 'bzfd', 'videos']

    stop_words = english_stop_words + spanish_stop_words + internet_stop_words + user_stopwords
    return stop_words

def create_ngram_df(df, title_column, creator_column, n, stopwords, sentance_cutoff = None, columns_to_include=None):
    '''returns a pandas.DataFrame object with a words/ngrams index and aggregated columns

    @params:
    df                  -required   :  A VI export converted to Pandas.DataFrame object
    title_column        -required   :  Name of the df column with video titles (currently: 'Video_Title')
    creator_column      -required   :  Name of column with creator name (currently: "Creator") for removing creator names from words before analysis
    n                   -required   :  The number of words for ngram 
    stopwords           -required   :  List of stopwords to remove before analysis
    sentance_cutoff     -optional   :  Allows truncating sentence to specific number of words, default set to no trucation (highly recommended for ngrams > 2)
    columns_to_include  -optional   :  Allows user to only aggregate certain columns, default is to aggregate all columns

    sample output:
    Word/ngram      Count        Views         Titles
    chocolate       3            [10,20,40]    ['how to make chocolate', 'top 10 christmas chocolate ideas', 'chocolate fondue']
    '''

    df.drop_duplicates([title_column])
    ngram_dict = initialize_ngram_dict(df, columns_to_include = columns_to_include)
    counter = 0
    printProgress(counter, len(df), prefix = 'Progress: ', suffix = 'Complete', barLength = 50)

    for row in df.itertuples():
        row = tuple_to_series(df, row) #allows reference, similar to named tuple, but compatible
        words = filter_title_words(df, row, title_column, stopwords, sentance_cutoff = sentance_cutoff, filter_creator_names = True, creator_column = creator_column)
        ngrams = get_ngrams(words, n)
        for ngram in ngrams:
            for column in ngram_dict.keys():
                if not pd.isnull(row[column]):
                    add_ngram_to_dict(row, ngram, ngram_dict, column)
        counter += 1
        printProgress(counter, len(df), prefix = 'Progress: ', suffix = 'Complete', barLength = 50)

    ngram_df = pd.DataFrame(ngram_dict)
    ngram_df = sort_by_count(ngram_df)
    return ngram_df

def initialize_ngram_dict(df, columns_to_include = None):
    '''Creates a dictionary to append ngram aggregations.  Creates a dictionary with one
    key for every column to aggregate, default to to aggregate all columns in input df

    @params:
    df                   -required   :  input df of type pandas.DataFrame
    columns_to_include   -optional   :  list of columns to aggregate, defaults to all

    sample input:
    df
    Video_Title       youtube_channel_id        Views      Total_Engagements

    sample output:
    dict
    {'Video_Title': {}
     'youtube_channel_id': {}
     'Views': {}
     'Total_Engagments': {}
     }
     '''
    ngram_dict = {}
    if not columns_to_include:
        columns_to_include = df.columns
    for column in columns_to_include:
        ngram_dict[column] = {}
    ngram_dict['index'] = {} #create an index column to keep track of unique videos
    return ngram_dict

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
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

def tuple_to_series(df, row):
    '''change tuple to pd.Series to allow for lookup by attribute'''
    index = ['index'] + list(df.columns)
    row = pd.Series(row, index = index) 
    return row

def filter_title_words(df, row, title_column, stopwords, sentance_cutoff=None, filter_creator_names = True, creator_column = None):
    '''Placed in df.iterrows loop - Takes title words from each row, uses regex to return only alphanum, then filters stopwords 
    and creator names from results.  Also truncates list to sentance cutoff length if given

    @params:
    df                      -required  : The Pandas.DataFrame
    row                     -required  : Row of Pandas.DataFrame from iterrows loop
    title_column            -required  : The name of the Row Series containing title words
    stopwords               -required  : A list of stopwords to filter out of results
    sentance_cutoff         -optional  : Allows to filter list of words to a max limit (to speed up computation)
    filter_creator_names    -optional  : Option to filter out creator names from results as found in creator column of row-level Series
    creator_column          -optional  : The name of the Series containing creator names

    Sample Input/Output:
    'This is the coolest title in!the!WORLD!@*!&@*!DEFINITELY!)!'  => ['coolest', 'title', 'world']
    '''
    if not creator_column:
        filter_creator_names = False

    words = str(row[title_column]).lower().split(' ')
    regex_words_list = []
    pattern = re.compile(r'\w{3,}')
    for word in words:
        regex_words = re.findall(pattern, word)
        for regex_word in regex_words:
            regex_words_list.append(regex_word)

    if sentance_cutoff:
        regex_words_list = regex_words_list[0:sentance_cutoff]
    regex_words_set = set(regex_words_list) #eliminate duplicates
    stop_words = set(stopwords)
    regex_words_set = regex_words_set.difference(stop_words) #eliminate stop_words
    if filter_creator_names:
        words_in_creator_names = get_words_in_creator_names(df, creator_column)
        regex_words_set = regex_words_set.difference(words_in_creator_names)
    regex_words_list = list(regex_words_set)
    return regex_words_list

def get_words_in_creator_names(df, creator_column):
    '''Filters out creator names from words --> see filter_title_words()
    '''
    creators = list(set(df[creator_column].tolist()))
    words_in_creator_names = [str(creator).split(' ') for creator in creators]
    words_in_creator_names = [item for sublist in words_in_creator_names for item in sublist]
    words_in_creator_names = set(words_in_creator_names)
    return words_in_creator_names

def get_ngrams(words_list, n=2):
    '''Given a list of words, returns all combinations of ngrams without replacement, in alphabetical order

    @params:
    words_list     -required  :  a list of words
    n              -required  :  number of words to choose for combination

    Sample Input/Output:
    ['Small', 'Word', 'List'] => [('List', 'Small'),('List','Word'),('Small','Word')]
    '''
    ngram_iter = itertools.combinations(words_list,n)
    ngram_list = []
    for ngram in ngram_iter: #order bigrams so combination only has one order it will append to dict
        ngram = sorted(ngram)
        ngram = tuple(ngram)
        if n ==1:
            ngram = ngram[0]
        ngram_list.append(ngram)
    return ngram_list

def add_ngram_to_dict(row, ngram, ngram_dict, column_key):
    '''Adds Column value to dictionary with key = current_ngram
    
    '''
    try:
        ngram_dict[column_key][ngram].append(row[column_key])
    except KeyError:
        ngram_dict[column_key][ngram] = []
        ngram_dict[column_key][ngram].append(row[column_key])

def sort_by_count(df):
    '''returns Df, sorted by Word Count descending


    '''
    df.head()
    df['word_count'] = df['index'].apply(lambda x: len(x))
    df = df.sort_values(by='word_count', ascending=False)
    return df

def df_means(df,*args): 
    column_number = len(args)
    counter = 0
    printProgress(counter, column_number, prefix = 'Progress: ', suffix = 'Complete', barLength = 50)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        for arg in args:
            column_name = 'mean_'+str(arg)
            df[column_name] = df[arg].apply(lambda x: sp.nanmean(x))
            counter += 1
            printProgress(counter, column_number, prefix = 'Progress: ', suffix = 'Complete', barLength = 50)
    return df

def df_medians(df,*args): 
    column_number = len(args)
    counter = 0
    printProgress(counter, column_number, prefix = 'Progress: ', suffix = 'Complete', barLength = 50)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        for arg in args:
            column_name = 'median_'+str(arg)
            df[column_name] = df[arg].apply(lambda x: sp.nanmedian(x))
            counter += 1
            printProgress(counter, column_number, prefix = 'Progress: ', suffix = 'Complete', barLength = 50)
    return df

def save_file(filename):
    path_to_desktop = os.path.expanduser('~') + '/Desktop/' + filename + '.xlsx'
    writer = pd.ExcelWriter(path_to_desktop, engine='xlsxwriter')
    df.to_excel(writer, 'Word Count', encoding='UTF-8')
    writer.save()

def pandaCounter(x):
    if type(x) is type([]):
        count = dict(Counter(x))
        return count
        #total = sum(count.values())
        #percentages = {k: v / total for k, v in count.items()}
        #return percentages
    else:
        return x

def summarize_columns(df, *args, **kwargs):
    for column in args:
        df[column] = df[column].apply(nancounter)
        return df


if __name__ == '__main__':
    
    outfile = input("Select a Filename:   ") #to save file later
    if not outfile: outfile = 'output' 

    #get user set options
    ngram = get_user_number('Please select how many words in ngram (1-3)?:  ', n=4)
    sentance_cutoff = get_user_number('Please select title word limit (1-1000)?:  ', n=1000)
    stopwords = initialize_stopwords_list(user_stopwords = get_user_stopwords())
    df = pd.read_csv(get_filename(), skiprows=1)
    
    #define which columns to work on from export
    columns_to_include = ['Category', 'Comments', 'Creator', 'Creator_Country', 'Duration (seconds)', 'ER30', 'ER7', 'Facebook_Comments', 'Facebook_Likes', 'Facebook_Shares', 'Facebook_Total_Engagements', 'Platform', 'Published_Date', 'Topics', 'Total_Engagements', 'V30', 'V7', 'Video_Title', 'Video_URL', 'Views', 'Likes']
    columns_to_do_stats_on = ['Comments', 'Duration (seconds)' , 'ER30', 'ER7', 'Facebook_Comments', 'Facebook_Likes', 'Facebook_Shares', 'Facebook_Total_Engagements', 'Total_Engagements', 'V30', 'V7', 'Views', 'Likes']
    #columns_to_do_stats_on = df.select_dtypes(include=['float64']).columns.tolist() #list of columns with 'float64' type
    columns_to_summarize = ['Category', 'Creator', 'Creator_Country', 'Platform', 'Topics']

    print('\n(Part 1/6): Reading selected csv...')


    start_time = time.time()
    print('\n(Part 2/6): Converting to word-index table...')
    ngram_df = create_ngram_df(df, title_column = 'Video_Title', creator_column = 'Creator', n = ngram, stopwords = stopwords, sentance_cutoff = sentance_cutoff, columns_to_include=columns_to_include)


    print('\n(Part 3/6): Computing metric means...')
    #take the means of aggregated values for each indicated column
    df = df_means(ngram_df, *columns_to_do_stats_on)
    #take the medians of aggregated values for each indicated column
    print('\n(Part 4/6): Computing metric medians...')
    df = df_medians(df, *columns_to_do_stats_on)
    
    #drop some less interesting data to make opening excel faster
    print('\n(Part 5/6): Doing some extra analysis...')
    df = df.drop(columns_to_do_stats_on, axis=1)
    df['Unique_Creator_Count'] = df['Creator'].apply(lambda x: len(x))
    for column in columns_to_summarize:
        df[column] = df[column].apply(pandaCounter)
    df = df.join(pd.DataFrame(df['Platform'].to_dict()).T)
    df = df[df['word_count'] > 1]
    df = df.reset_index()

    print('\n(Part 6/6): Saving file to Desktop...')
    save_file(outfile)
    print('\nCOMPLETE')

    seconds = (time.time() - start_time)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    print("Time to Completion: --- %dh:%02dm:%02ds ---\n" % (h, m, s))


