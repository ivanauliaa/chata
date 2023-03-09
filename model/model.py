import string
import math
import pandas as pd
import numpy as np
from collections.abc import Iterable
from config.env import env
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Model:
  def __init__(self, docs, responses):
    self.stopwords = []
    with open(env.STOPWORDS_PATH) as f:
      for line in f:
        self.stopwords.append(line.strip())

    self.dictionary_df = pd.read_csv(f'{env.DICTIONARY_PATH}')

    self.docs = [self.preprocessing(doc) for doc in docs]
    self.responses = responses

  def preprocessing(self, text):
    # case folding (lowercase)
    text = text.lower()

    # remove punctuation
    text = text.translate(str.maketrans(dict.fromkeys(string.punctuation)))

    # trim unnecessary space
    text = text.strip()

    # tokenize
    tokenized = text.split()

    # slang word conversion
    tokenized = [self.dictionary_df.loc[self.dictionary_df[env.SLANG_WORD_COL] == token, env.FORMAL_WORD_COL].iloc[0] if token in self.dictionary_df[env.SLANG_WORD_COL].values else token for token in tokenized]

    # remove stopwords
    tokenized = [token for token in tokenized if token not in self.stopwords]

    # stem and lemmatize
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    tokenized = [stemmer.stem(token) for token in tokenized]

    return ' '.join(tokenized)

  def predict(self, query):
    query = self.preprocessing(query)

    self.tf_doc = self.compute_normalizedtf(self.docs)
    self.idf_dict = self.compute_idf(self.docs)

    self.query_norm_tf = self.compute_query_tf(query)
    self.idf_dict_qry = self.compute_query_idf(query, self.docs)
    self.tf_idf, self.df = self.compute_tfidf_with_alldocs(self.docs, query)
    self.tfidf_dict_qry = self.compute_query_tfidf(query)

    similarity_docs = list(self.flatten(self.rank_similarity_docs(query, self.docs)))
    max_index = self.get_max_value_index(similarity_docs) 

    if similarity_docs[max_index] < 0.3:
      return 'Tidak dapat memahami permintaan anda'
    else:
      return self.responses[max_index]

  def compute_idf(self, docs):
    idf_dict = {}
    for doc in docs:
        sentence = doc.split()
        for word in sentence:
            idf_dict[word] = self.inverseDocumentFrequency(word, docs)
    return idf_dict

  def compute_normalizedtf(self, docs):
    tf_doc = []
    for txt in docs:
      sentence = txt.split()
      norm_tf= dict.fromkeys(set(sentence), 0)
      for word in sentence:
        norm_tf[word] = self.termFrequency(word, txt)
      tf_doc.append(norm_tf)
      df = pd.DataFrame([norm_tf])
      idx = 0
      new_col = ["Normalized TF"]
      df.insert(loc=idx, column='Document', value=new_col)
    return tf_doc

  def termFrequency(self, term, document):
    normalizeDocument = document.lower().split()
    return normalizeDocument.count(term.lower()) / float(len(normalizeDocument))

  def inverseDocumentFrequency(self, term, allDocuments):
    numDocumentsWithThisTerm = 0
    for doc in range (0, len(allDocuments)):
        if term.lower() in allDocuments[doc].lower().split():
            numDocumentsWithThisTerm = numDocumentsWithThisTerm + 1

    if numDocumentsWithThisTerm > 0:
        return 1.0 + math.log(float(len(allDocuments)) / numDocumentsWithThisTerm)
    else:
        return 1.0

  def compute_tfidf_with_alldocs(self, docs , query):
    tf_idf = []
    index = 0
    query_tokens = query.split()
    df = pd.DataFrame(columns=['doc'] + query_tokens)
    for doc in docs:
        df['doc'] = np.arange(0 , len(docs))
        doc_num = self.tf_doc[index]
        sentence = doc.split()
        for word in sentence:
            for text in query_tokens:
                if(text == word):
                    idx = sentence.index(word)
                    tf_idf_score = doc_num[word] * self.idf_dict[word]
                    tf_idf.append(tf_idf_score)
                    df.iloc[index, df.columns.get_loc(word)] = tf_idf_score
        index += 1
    df.fillna(0 , axis=1, inplace=True)
    return tf_idf , df

  def compute_query_tfidf(self, query):
    tfidf_dict_qry = {}
    sentence = query.split()
    for word in sentence:
        tfidf_dict_qry[word] = self.query_norm_tf[word] * self.idf_dict_qry[word]
    return tfidf_dict_qry

  def cosine_similarity(self, tfidf_dict_qry, df, query, doc_num):
    dot_product = 0
    qry_mod = 0
    doc_mod = 0
    tokens = query.split()

    for keyword in tokens:
        dot_product += tfidf_dict_qry[keyword] * df[keyword][df['doc'] == doc_num]
        #||Query||
        qry_mod += tfidf_dict_qry[keyword] * tfidf_dict_qry[keyword]
        #||Document||
        doc_mod += df[keyword][df['doc'] == doc_num] * df[keyword][df['doc'] == doc_num]
    qry_mod = np.sqrt(qry_mod)
    doc_mod = np.sqrt(doc_mod)
    #implement formula
    denominator = qry_mod * doc_mod
    cos_sim = dot_product/denominator

    if math.isnan(cos_sim):
      cos_sim = pd.Series([0])

    return cos_sim

  def flatten(self, lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
             for x in self.flatten(item):
                yield x
        else:
             yield item

  def rank_similarity_docs(self, query, data):
    cos_sim =[]
    for doc_num in range(0 , len(data)):
        cos_sim.append(self.cosine_similarity(self.tfidf_dict_qry, self.df , query , doc_num).tolist())
    return cos_sim

  def get_max_value_index(self, arr):
    max_index = 0

    for i in range(1, len(arr)):
      max_index = i if arr[i] > arr[max_index] else max_index

    return max_index

  def compute_query_tf(self, query):
    query_norm_tf = {}
    tokens = query.split()
    for word in tokens:
        query_norm_tf[word] = self.termFrequency(word , query)
    return query_norm_tf

  def compute_query_idf(self, query, docs):
    idf_dict_qry = {}
    sentence = query.split()
    for word in sentence:
        idf_dict_qry[word] = self.inverseDocumentFrequency(word, docs)
    return idf_dict_qry
