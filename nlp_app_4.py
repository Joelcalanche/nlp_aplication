

# Core Pkgs
import streamlit as st 
import os

# other pkgs

import pandas as pd
# import base64
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import sqlite3



# NLP Pkgs
from textblob import TextBlob 
import spacy
import streamlit as st
import pandas as pd
# import base64
import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import pandas as pd
import sqlite3

import nltk
nltk.download('punkt')


from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# spacy_summarizers packages

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

from heapq import nlargest

# Crea una conexión a la base de datos SQLite
# con = sqlite3.connect(r"C:\Users\calanche\Desktop\projectNLP\nlp_aplication\bbc_db.sqlite")

con = sqlite3.connect("./bbc_db.sqlite")
# Extrae los datos de la consulta directamente a un DataFrame
bbc_df = pd.read_sql_query("SELECT * from bbc_db", con, parse_dates=["timestamps_"])
# bbc_df.tail()
punctuation = punctuation + '\n' + '\n\n'

# # Selecciona sólo datos en el año 2002
# surveys2002 = surveys_df[surveys_df.year == 2002]

# # Escribe los datos del nuevo DataFrame en una nueva tabla en SQLite
# surveys2002.to_sql("surveys2002", con, if_exists="replace")

# # No te olvides de cerrar la conexión
# con.close()

bbc_df.sort_values(by=["timestamps_"], inplace=True, ascending=False)
st.title('NLP_APPLICATION')
df_tmp = bbc_df.copy()
# print(len(df_tmp))


days = df_tmp.timestamps_.dt.day
months = df_tmp.timestamps_.dt.month

print(type(days))
years =df_tmp.timestamps_.dt.year


st.sidebar.header('User Input Features')
# selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))
selected_day = st.sidebar.selectbox('Days', list(days.unique()))
# selected_day_list = list(selected_day)
selected_year = st.sidebar.selectbox('Years', list(years.unique()))
selected_month = st.sidebar.selectbox('Months', list(months.unique()))



# # Filtering data
# r = df_tmp[((df_tmp.timestamps_.dt.year.isin(years)) & (df_tmp.timestamps_.dt.day.isin(days)))]
prueba = [selected_year.tolist()]
print(prueba)
# r = df_tmp[((df_tmp.timestamps_.dt.year.isin([2021])) & (df_tmp.timestamps_.dt.day.isin([24])))]r = df_tmp[((df_tmp.timestamps_.dt.year.isin([selected_year.tolist()])) & (df_tmp.timestamps_.dt.day.isin([selected_day.tolist()])))]
r = df_tmp[((df_tmp.timestamps_.dt.year.isin([selected_year.tolist()])) & (df_tmp.timestamps_.dt.day.isin([selected_day.tolist()])) & (df_tmp.timestamps_.dt.month.isin([selected_month.tolist()])))]
r_1 = r[:20]
print("este es mi experimento",len(df_tmp))
print(len(r_1))
unique_titles = r_1["title"].unique().tolist()
selected_title = st.sidebar.selectbox('titles', unique_titles)
# print(selected_title)
# print(len(selected_title))


# segundo filtro
r_2 =  r_1["text_"][(r_1["title"] == selected_title)]
r_2_str = r_2.tolist()
# print(type(r_2_str))
# print(df_selected_team)
# st.header('Display Player Stats of Selected Team(s)')
# st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
# # print(df_selected_team)
# if r_2.l
if not r_2_str:
    print("Empty")
    st.write("## Sorry no news found for this entry")
else:
    print("Not Empty")
    st.write(r_2)



# Function for Sumy Summarization
def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx,Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result



def spacy_summarizer(text):

    stopwords = list(STOP_WORDS)
    # stopwords
    # NLp model
    nlp = spacy.load('en_core_web_sm')
    # doc
    doc = nlp(text)
    # tokenise sentences
    tokens = [token.text for token in doc]
    print(tokens)

    # We must remove punctuation and stopwords

    # punctuation = punctuation + '\n' + '\n\n'


    # text cleaning

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                # first time the word is apear
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1


        
    # find out max frequency
    max_frequency = max(word_frequencies.values())
    print(max_frequency)
    # then normalize the dictionary
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency

    print(word_frequencies)
    # sentences tokenization
    sentence_tokens = [sent for sent in doc.sents]
    print(sentence_tokens)
    print("longitud de sentence_tokens")
    print(len(sentence_tokens))


    # calcule the sentences score
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]  += word_frequencies[word.text.lower()]




    print("este es sentence_scores")
    print(sentence_scores)
    select_length = int(len(sentence_tokens)* 1/2)
    # print(select_length)

    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
    # combine the sentencs

    print(summary)

    final_summary = [word.text for word in summary]
    summary_join =  " ".join(final_summary)
    print(summary_join)
    print(len(text))

    print(len(summary_join))

    return summary_join

# Function to Analyse Tokens and Lemma
@st.cache
def text_analyzer(my_text):
    #before 'en'------> 'en_core_web_sm'
    nlp = spacy.load("en_core_web_sm")
    docx = nlp(my_text)
    # tokens = [ token.text for token in docx]
    allData = [('"Token":{},\n"Lemma":{}'.format(token.text,token.lemma_))for token in docx ]
    return allData

# Function For Extracting Entities
@st.cache
def entity_analyzer(my_text):
    #before 'en'------> 'en_core_web_sm'
    nlp = spacy.load("en_core_web_sm")
    docx = nlp(my_text)
    tokens = [ token.text for token in docx]
    entities = [(entity.text,entity.label_)for entity in docx.ents]
    allData = ['"Token":{},\n"Entities":{}'.format(tokens,entities)]
    return allData


def main():
    """ NLP Based App with Streamlit """

    # Title
    st.title("NLPiffy with Streamlit to deeplabsearch")
    st.subheader("Natural Language Processing On the Go..")
    st.markdown("""
        #### Description
        + This is a Natural Language Processing(NLP) Based App useful for basic NLP task
        Tokenization,NER,Sentiment,Summarization
        """)
    if not r_2_str:
        st.write("""## wrong entry
        
        No record could be found for the selected year, month and day, try another combination of those suggested, check the database
        
        """)
    else:
        # Tokenization
        if st.checkbox("Show Tokens and Lemma"):
            st.subheader("Tokenize Your Text")

            message = r_2_str
            st.write(message[0])
            if st.button("Analyze"):
                nlp_result = text_analyzer(message[0])
                st.json(nlp_result)

        # Entity Extraction
        elif st.checkbox("Show Named Entities"):
            st.subheader("Analyze Your Text")

            message = r_2_str
            st.write(message[0])
            if st.button("Extract"):
                entity_result = entity_analyzer(message[0])
                st.json(entity_result)

        # Sentiment Analysis
        elif st.checkbox("Show Sentiment Analysis"):
            st.subheader("Analyse Your Text")

            message = r_2_str
            st.write(message[0])
            if st.button("Analyze"):
                blob = TextBlob(message[0])
                result_sentiment = blob.sentiment
                st.success(result_sentiment)

        #Summarization
        elif st.checkbox("Show Text Summarization"):
            st.subheader("Summarize Your Text")

            message = r_2_str
            st.write(message[0])
            summary_options = st.selectbox("Choose Summarizer",['sumy', 'spacy_summarizer'])
            if st.button("Summarize"):
                if summary_options == 'sumy':
                    st.text("Using Sumy Summarizer ..")
                    summary_result = sumy_summarizer(message[0])
                elif summary_options == 'spacy_summarizer':
                	st.text("Using Spacy Summarizer ..")
                	summary_result = spacy_summarizer(message[0])
                # else:
                # 	st.warning("Using Default Summarizer")
                # 	st.text("Using Gensim Summarizer ..")
                # 	summary_result = summarize(rawtext)

            
                st.success(summary_result)



    st.sidebar.subheader("About App")
    st.sidebar.text("NLPiffy App with Streamlit")
    st.sidebar.info("Cudos to the Streamlit Team")
    

    st.sidebar.subheader("By")
    st.sidebar.text("Joel_calanche")
    st.sidebar.text("^_^")

#--------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

## a partir de aqui probamos

# import spacy
# from spacy.lang.en.stop_words import STOP_WORDS
# from string import punctuation

# from heapq import nlargest
# def spacy_summarizer(text):

#     stopwords = list(STOP_WORDS)
#     # stopwords
#     # NLp model
#     nlp = spacy.load('en_core_web_sm')
#     # doc
#     doc = nlp(text)
#     # tokens
#     tokens = [token.text for token in doc]

#     # We must remove punctuation and stopwords

#     punctuation = punctuation + '\n' + '\n\n'


#     # text cleaning

#     word_frequencies = {}
#     for word in doc:
#         if word.text.lower() not in stopwords:
#             if word.text.lower() not in punctuation:
#                 # first time the word is apear
#                 if word.text not in word_frequencies.keys():
#                     word_frequencies[word.text] = 1
#                 else:
#                     word_frequencies[word.text] += 1


        
#     # find out max frequency
#     max_frequency = max(word_frequencies.values())

#     # then normalize the dictionary
#     for word in word_frequencies.keys():
#         word_frequencies[word] = word_frequencies[word]/max_frequency

#     # sentences tokenization
#     sentence_tokens = [sent for sent in doc.sents]
#     print(sentence_tokens)


#     # calcule the sentences score
#     sentence_scores = {}
#     for sent in sentence_tokens:
#         for word in sent:
#             if word.text.lower() in word_frequencies.keys():
#                 if sent not in sentence_scores.keys():
#                     sentence_scores[sent] = word_frequencies[word.text.lower()]
#                 else:
#                     sentence_scores[sent]  += word_frequencies[word.text.lower()]




#     select_length = int(len(sentence_tokens)*0.3)
#     select_length

#     summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
#     # combine the sentencs

#     final_summary = [word.text for word in summary]
#     summary_join =  " ".join(final_summary)

#     print(len(text))

#     print(len(summary_join))

#     return summary_join






if __name__ == '__main__':
    main()