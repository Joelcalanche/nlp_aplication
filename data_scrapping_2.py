import requests
# request allows us to grab/download HTML files
from bs4 import BeautifulSoup

import pprint
# beautyfulsoup allows us to use the  HTML and grab different data
import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker

import json
from datetime import datetime
import datetime
import sqlite3


def run_bbc_etl():



    res = requests.get('https://www.bbc.co.uk/news/science-environment-56837908')
    soup = BeautifulSoup(res.text, 'html.parser')

    # links = soup.select('.gs-c-promo-heading gs-o-faux-block-link__overlay-link')
    # links_divs = soup.find_all('a')

    # for link in links_divs:
    #     link = link.find("href")
    #     print(link)

    # # paragrha
    # print(links_divs[:2])
    # product_links = [] 
    titles_list = soup.find_all("h3")



    paragraph_list = soup.find_all('div', {'class': 'gs-u-mb+ gel-body-copy qa-post-body'})
    # print("evaluando el texto")
    # print(len(paragraph_list))

    content_list = [content.text  for content in paragraph_list]
    # print(content_list)
    # print(content_list[-1])
    # print(len(content_list))

    # for product in product_list:
    #     product_links.append(product.text)

    # print(product_links)
    # print(len(product_links))

    titles_text  = [title.text for title in titles_list]
    # print(product_text[-10:])
    # print(len(product_text))


    # links_list = soup.find_all("a")

    # links_text = [ link.find("https:")  for link in links_list]
    # print(links_text)


    # links_with_text = [a['href'] for a in soup.find_all('a', href=True) if a.text]
    # print(links_with_text[:20])

    links_with_text_ = [a['href'] for a in soup.find_all('a', href=True) if a.text]
    # print(links_with_text_)
    # print(links_with_text[:20])


    # product_text = list(set(product_text))
    # print(product_text)
    # print(len(product_text))


    entradas = soup.find_all('article', {'class': 'qa-post gs-u-pb-alt+ lx-stream-post gs-u-pt-alt+ gs-u-align-left'})
    print(len(entradas))


    entradas_2 = soup.find_all('time', {'class': 'lx-stream-post__meta-time gs-u-align-middle gs-u-display-inline-block gs-u-mr0@m gs-u-mr gel-long-primer'})
    # print(len(entradas_2))



    fecha_list = []
    for idx, entrada in enumerate(entradas_2):
        fecha = entrada.find('span', {'class': 'gs-u-vh qa-visually-hidden-meta'}).getText()
        fecha_list.append(fecha)
    print(fecha_list)

    # print(fecha_list)

    entradas_3 = soup.find_all('div', {'class': 'gs-u-mb+ gel-body-copy qa-post-body'})
    # print("este es la prueba que estoy haciendo")
    # print(len(entradas_3))
    lista_texto = []
    for idx, entrada in enumerate(entradas_3):
        texto_ = entradas[idx].find('p')
        lista_texto.append(texto_)
        
        
        # lista_texto.append(texto_)
    # print(lista_texto)

    # # print(entradas[-3:])
    # #gs-c-promo-body gs-u-mt@xxs gs-u-mt@m gs-c-promo-body--primary gs-u-mt@xs gs-u-mt@s gs-u-mt@m gs-u-mt@xl gel-1/3@m gel-1/2@xl gel-1/1@xxl


    # entradas_2 = soup.find_all('div', {'gs-c-promo-body gs-u-mt@xxs gs-u-mt@m gs-c-promo-body--primary gs-u-mt@xs gs-u-mt@s gs-u-mt@m gs-u-mt@xl gel-1/3@m gel-1/2@xl gel-1/1@xxl'})


    # # print(len(entradas_2))

    # entradas_3 = soup.find_all('div', {'class': 'gs-c-promo-body gs-u-mt@xxs gs-u-mt@m gs-c-promo-body--flex gs-u-mt@xs gs-u-mt0@xs gs-u-mt@m gel-1/2@xs gel-1/1@s'})
    # entradas_3 = list(set(entradas_3))
    # # print(list(set(entradas_3))[:3])

    # entradas_4 = entradas_3 + entradas_2

    # # print(len(entradas_4))

    # Recorremos todas las entradas para extraer el título, autor y fecha
    titles_list = []
    links_list = []
    text_list = []
    Authors_list = []
    dates = []

    for idx, entrada in enumerate(entradas):
        # Con el método "getText()" no nos devuelve el HTML
        title = entrada.h3.find("span").getText()
        titles_list.append(title)
        links_with_text =  entrada.find("a", href=True, text=True)
        links_completo = "https://www.bbc.com" + links_with_text["href"]
        links_list.append(links_completo)

    def create_custom_data_raw(links, titles, texts, dates):
        data_raw = []

        for ix, entrada in enumerate(links):
            data_raw.append({'date': dates[ix], 'title': titles[ix], 'link':links[ix], 'text': texts[ix]})
        print(len(data_raw))
        return  data_raw



    pprint.pprint(create_custom_data_raw(links_list, titles_list, content_list, fecha_list)[-1])


    data = create_custom_data_raw(links_list, titles_list, content_list, fecha_list)


    dates = []
    titles  = []
    links_bbc = []

    texts = []

    for dictionary in data:
        dates.append(dictionary["date"])
        titles.append(dictionary["title"])
        links_bbc.append(dictionary["link"])
        texts.append(dictionary["text"])

    new_data_dict = {
        
        "date_": dates,
        "title": titles,
        "link": links_bbc,
        "text_": texts

    }

    print(new_data_dict)
    df_bbc = pd.DataFrame(new_data_dict, columns=["date_", "title", "link", "text_"])

    df_bbc["timestamps_"] = datetime.datetime.now()


    print(df_bbc.head())
    # print(df_bbc["title"])
    print(df_bbc["link"])

    # Load
    DATABASE_LOCATION = "sqlite:///bbc_db.sqlite"
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('bbc_db.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS bbc_db(
        date_ VARCHAR(200),
        title VARCHAR(200),
        link VARCHAR(200),
        text_  VARCHAR(200),
        timestamps_ VARCHAR(200)
        
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        df_bbc.to_sql("bbc_db", engine, index=False, if_exists='append')
        df_bbc.to_csv("bbc_db", index=False,)



    except:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")













