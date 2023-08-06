import re
import numpy as np
import pandas as pd
from collections import Counter





class ProcessText:
    
    def __init__(self, df, text_column, response_column = None, stop_word_list = None, pos_word_list = None, neg_word_list = None):
        self.df = df
        self.text_column = text_column
        self.response_column = response_column
        self.stop_word_list = stop_word_list
        self.pos_word_list = pos_word_list
        self.neg_word_list = neg_word_list
        
    def __repr__(self):
        df = self.df
        nr = df.shape[0]
        nc = df.shape[1]
        tcol = self.text_column
        rcol = self.response_column
        if self.stop_word_list is not None:
            swl = (", ".join(self.stop_word_list[0:3])) + ", ..."
        else:
            swl = None
        if self.pos_word_list is not None:
            pwl = (", ".join(self.pos_word_list[0:3])) + ", ..."
        else:
            pwl = None
        if self.neg_word_list is not None:
            nwl = (", ".join(self.neg_word_list[0:3])) + ", ..."
        else:
            nwl = None
        ret1 = "|------------------------| INPUT DATA |------------------------|\n"
        ret2 = f"| -- input data of {nr} rows and {nc} columns\n"
        ret3 = f"| -- text column name: {tcol}\n"
        ret4 = f"| -- response column name: {rcol}\n"
        ret5 = f"| -- provided stop words: {swl}\n"
        ret6 = f"| -- provided positive words: {pwl}\n"
        ret7 = f"| -- provided negative words: {nwl}\n"
        ret8 = "|--------------------------------------------------------------|"
        return f"{ret1}{ret2}{ret3}{ret4}{ret5}{ret6}{ret7}{ret8}"
    
    
    def __split_and_clean(self, txt, sub_pattern = "\W+", split_on = " ", drop_len_one = True, force_alt = "NA"):
        try:
            txt_clean = re.sub(sub_pattern, split_on, txt).lower()
        except:
            txt_clean = force_alt
        txt_split = txt_clean.split(split_on)
        txt_split = [t for t in txt_split if t != ""]
        if drop_len_one:
            txt_split = [t for t in txt_split if len(t) != 1]
        return txt_split
    
    def __remove_stopwords(self, txt, stopword_list):
        return [t for t in txt if t not in stopword_list]
    
    
    def listify(self):
        use_stopword_list = self.stop_word_list
        df = self.df
        text_col = self.text_column
        ret_list = []
        text_list = df[text_col].tolist()
        for tl in text_list:
            tmp = self.__split_and_clean(tl)
            if use_stopword_list is not None:
                tmp = self.__remove_stopwords(tmp, use_stopword_list)
            ret_list.append(tmp)
        return ret_list
    
    def sentiment(self):
        pos_word_list = self.pos_word_list
        neg_word_list = self.neg_word_list
        txt_lol = self.listify()
        text_abbr_list = []
        pos_score_list = []
        neg_score_list = []
        pmn_score_list = []
        for tl in txt_lol:
            text_abbr_list.append((", ".join(tl[0:3])) + ", ...")
            pos_score = sum([1 if ttl in pos_word_list else 0 for ttl in tl])
            pos_score_list.append(pos_score)
            neg_score = sum([1 if ttl in neg_word_list else 0 for ttl in tl])
            neg_score_list.append(neg_score)
            pmn_score = pos_score - neg_score
            pmn_score_list.append(pmn_score)
        ret = pd.DataFrame({
            "text_abbr": text_abbr_list,
            "pos_sentiment": pos_score_list,
            "neg_sentiment": neg_score_list,
            "overall_sentiment": pmn_score_list
        })
        return ret
    
    def dictionary(self, rem_dups = True, keep_order = True):
        lol = self.listify()
        if rem_dups:
            flat_list = [item for sublist in lol for item in sublist]
            if keep_order:
                ret = list(dict.fromkeys(flat_list))
            else:
                ret = list(set(flat_list))
        else:
            ret = [item for sublist in lol for item in sublist]
        return ret
    
    def dtm(self, use_dictionary = None, response_var_name = "RESPONSE"):
        if use_dictionary is None:
            raise TypeError("A dictionary must be provided to arg 'use_dictionary'")
        ret_lst = []
        lol = self.listify()
        for l in lol:
            tmp_count = Counter(l)
            res = [tmp_count[word] for word in use_dictionary]
            ret_lst.append(res)
        ret_array = np.array(ret_lst).reshape(len(ret_lst), len(use_dictionary))
        ret_df = pd.DataFrame(ret_array)
        ret_df.columns = use_dictionary
        if self.response_column is not None:
            ret_df[response_var_name] = self.df[self.response_column].tolist()
        return ret_df
