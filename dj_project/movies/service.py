import requests
import xml.etree.cElementTree as ET


def get_rating(id_film):
    if id_film == 0:
        imdb_rating = '-'
    else:
        url = f'https://rating.kinopoisk.ru/{id_film}.xml'
        r = requests.get(url)
        rating = {}
        # rating_list = []
        response_xml_as_string = str(r.content)[2:-1]
        responseXml = ET.fromstring(response_xml_as_string)
        for item in responseXml.iterfind('.//'):
            rating[item.tag] = item.text
            # rating_list.append(item.text)
            # print(item.tag, item.text, item.attrib)
        imdb_rating = rating['imdb_rating']
    return imdb_rating



