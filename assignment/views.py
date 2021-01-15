from django.shortcuts import render

import requests
from bs4 import BeautifulSoup


def index(request):
  return render(request,'index.html')

# Defining function to fetch the blog of given user tag input
def scrapper(text):
    url = 'https://medium.com/hackernoon/tagged/' +text
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    content = soup.find_all('div', class_="streamItem streamItem--postPreview js-streamItem")
    dic = []
    for property in content:
        Title = property.find('h3').text
        CreatedBy = property.find(
            class_='ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken').text
        date = property.find(
            class_='ui-caption u-fontSize12 u-baseColor--textNormal u-textColorNormal js-postMetaInlineSupplemental').text.split(
            ",")
        reading = property.find('span', class_='readingTime').get('title')
        link = property.find('a', class_='button button--smaller button--chromeless u-baseColor--buttonNormal').get(
            'href')

        blog = link.split("?")
        r = requests.get(link)
        hello = BeautifulSoup(r.content, 'html.parser')
        tags = hello.find_all('a', class_='b')
        Details = date[0] + " , " + reading
        Content = str(blog[0])
        res = property.find(class_="buttonSet u-floatRight").find('a',class_='button button--chromeless u-baseColor--buttonNormal')
        response = str(res).split("---------")[1:2]

        if len(response) != 0:
            count = response[0]
        else:
            count = 0

        tag_list = []
        for tag in tags:
            tag_list.append(tag.text)
        Tags = tag_list

        scrap = {
            'CreatedBy': CreatedBy,
            'Title': Title,
            'Details': Details,
            'Content': Content,
            'Tags': Tags,
            'link': link,
            'Response':count

        }
        dic.append(scrap)
    return dic

#Getting user input and processed it and return blogs of that input
def analyze(request):
    djtext = request.POST.get('text', 'default')
    dec = scrapper(djtext)

    return render(request, 'analyze.html', {'dec':dec})










