import os
import pandas as pd
import numpy as np
import glob
import yake
import pycld2 as cld2
import psycopg2
#from keybert import KeyBERT
from itertools import combinations
from pyvis.network import Network
# import json
import download_comment

def keyword_update_yake(text_summary, numOfKeywords=30):
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.2
    deduplication_algo = 'seqm'
    windowSize = 2
    # numOfKeywords =
    unigram_freq_list = pd.read_csv("./unigram_freq.csv")
    cleaned_text_summary = text_summary
    common_sw = ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ago", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "dont", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gon na", "gonna", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lot", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2",
                 "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "sir", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "thing", "things", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"]
    # remove 500 common words that are most frequent.
    common_words_fromfreq = list(unigram_freq_list[:500]['word'])
    stop_list_special = ['part', 'of', 'for', 'back', 'it', 'good morning', 'to', 'at', 'in', 'the', 'video', 'key', 'simple', 'bitcoin bitcoin', 'with', 'we', 'do', 'time', 'and', 'make', '[ music ]', 'day', 'best', 'work', 'be', 'btw', 'david', 'lol', 'bro',
                         'is', 'are', 'by', 'sex', 'set', 'started', 'meet tomorrow', 'language processing', 'natural language', 'good thing', 'next', 'hello', 'gon na', 'people', 'person', 'human', 'humanbeing', 'Hit', 'Hey', 'hit', 'hey', 'true', 'wow', 'this', 'n\'t']
    stop_list = list(set(common_sw+stop_list_special+common_words_fromfreq))

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold,
                                                dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None, stopwords=stop_list)

    new_keyword_candidates = custom_kw_extractor.extract_keywords(
        cleaned_text_summary)
    new_keyword_candidates.sort(key=lambda x: x[1])
    flatten_list = ' '.join(text_summary)
    n_cad = int(np.log(round(len(flatten_list)))*2)
    new_kw_list = new_keyword_candidates[:n_cad]

    new_kw_list_words = [keyword_tuple[0] for keyword_tuple in new_kw_list]

    return new_kw_list_words


def get_sent_dicts(target_f, yake_keyword_candidates):
    # make node dict
    sent_l = list(target_f['textDisplay'])
    sent_dict = {el: 0 for el in yake_keyword_candidates}

    # make link dict
    yake_pair = list(combinations(yake_keyword_candidates, 2))
    sent_dict_link = {el: 0 for el in yake_pair}

    # make keyword and corresponding videoId list
    keyword_video = {k: [] for k in yake_keyword_candidates}

    # check if keywords in every comment
    for i in range(len(sent_l)):
        sent_concept_list = []
        for item in yake_keyword_candidates:
            tmp = item.lower()
            # j is comment sentence
            j = sent_l[i].lower()
            # if word in this yake keyword not in sentence --> check next keyword
            key_not_in_sent_flag = 0
            for word_chunk in tmp.split():
                # print("word_chunk: ", word_chunk)
                if word_chunk not in j:
                    key_not_in_sent_flag = 1
            # print('key_not_in_sent_flag: ',key_not_in_sent_flag)
            if key_not_in_sent_flag == 1:
                continue
            else:
                vid_id = target_f.iloc[i]['videoId']
                # this keyword appearance +1
                sent_concept_list.append(item)
                sent_dict[item] = sent_dict[item]+1
                # print(sent_dict)
                # if videoId not added to the keyword's videoId list, add
                if str(vid_id) not in keyword_video[item]:
                    keyword_video[item].append(str(vid_id))
                    # print(keyword_video)

        # if >= 2 keywords in sentence, add to link
        if len(sent_concept_list) > 1:
            for j in list(combinations(sent_concept_list, 2)):
                tup1 = (j[0], j[1])
                tup2 = (j[1], j[0])
                if tup1 in sent_dict_link:
                    sent_dict_link[tup1] = sent_dict_link[tup1] + 1
                elif tup2 in sent_dict_link:
                    sent_dict_link[tup2] = sent_dict_link[tup2] + 1

    return sent_dict, sent_dict_link, keyword_video


def get_map_details(target_f):
    yake_keyword_candidates = keyword_update_yake(' '.join(list(target_f['textDisplay'])))
    sent_dict, sent_dict_link, keyword_video = get_sent_dicts(target_f, yake_keyword_candidates)
    return yake_keyword_candidates, sent_dict, sent_dict_link, keyword_video


def get_map():
    ## change them to sql thingy
    # keyword='test'
    os.environ['DB_USERNAME'] = "postgres"
    os.environ['DB_PASSWORD'] = 'eh20010421'
    # Construct connection string
    conn = psycopg2.connect(
        host="database-1.cgrpfuvmepy7.us-east-1.rds.amazonaws.com",
        database="hw3",
        port='5432',
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

    cursor = conn.cursor()
    # Fetch all rows from table
    cursor.execute('''SELECT * From public.comments as c 
                      where c.likecount > 1 ''')
    comments_all = pd.DataFrame(cursor.fetchall(), 
        columns=['commentId', 'videoId', 'textDisplay', 'publishedAt',
        'authorDisplayName', 'authorProfileImageUrl', 'likeCount'])
    cursor.execute('''
        with max_vid as(
            select videoid as vd, max(likecount) as ml
            from public.comments as c
            group by videoid
        )
        SELECT DISTINCT on (videoId)
            commentId, videoId, textDisplay, publishedAt,
            authorDisplayName, authorProfileImageUrl, likeCount 
        From public.comments as c, max_vid
        where c.videoid = max_vid.vd and c.likecount = max_vid.ml
        ''')
    top_comments = pd.DataFrame(cursor.fetchall(), 
        columns=['commentId', 'videoId', 'textDisplay', 'publishedAt',
        'authorDisplayName', 'authorProfileImageUrl', 'likeCount'])
    top_comments.to_csv('./comment_map/top_comments.csv', index=False)
    print("top_comments found")
    cursor.close()
    conn.close()
    yake_keyword_candidates, sent_dict, sent_dict_link, keyword_video = get_map_details(comments_all)
    net = Network('576px', '576ps', notebook=True)
    net.add_nodes(list(sent_dict.keys()), size=[max(i[1]/3, 1) for i in sent_dict.items()])
    for i in sent_dict_link:
        if sent_dict_link[i] > 2:
            net.add_edge(i[0], i[1], width=0.1,length=100/sent_dict_link[i]+20)
    net.barnes_hut(gravity=-1000, spring_length=20)
    net.show('./comment_map/map.html')


if __name__ == '__main__':
    get_map()
