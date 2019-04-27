import jieba.posseg as pseg
import matplotlib.pyplot as plt
from os import path
import re
import requests
from scipy.misc import imread
from wordcloud import WordCloud

def fetch_sina_news():
    PATTERN = re.compile('<d p=".*?">(.*?)<\/d>')
    BASE_URL = 'http://comment.bilibili.com/83089367.xml'
    with open('31621681.xml', 'w', encoding='utf-8') as f:
        r = requests.get(BASE_URL)
        data = r.text.encode('ISO-8859-1').decode('utf-8')
        p = re.findall(PATTERN, data)
        for s in p:
            f.write(s)
#            print(s)
        
    
def extract_words():
    with open('31621681.xml','r', encoding='utf-8') as f:
        news_subjects = f.readlines()
    
    stop_words = set(line.strip() for line in open('stopwords.txt', encoding='utf-8'))
    
    newslist = []
    for subject in news_subjects:
        if subject.isspace():
            continue
        # segment words line by line
        p = re.compile("n[a-z0-9]{0,2}")    # n, nr, ns, ... are the flags of nouns
        word_list = pseg.cut(subject)     
        for word, flag in word_list:
            if word not in stop_words and p.search(flag) != None:
                newslist.append(word)
    
    content = {}
    for item in newslist:
        content[item] = content.get(item, 0) + 1
    
    d = path.dirname(__file__)
    mask_image = imread(path.join(d, "cxk.jpg"))
    wordcloud = WordCloud(font_path='simhei.ttf', background_color="white", mask=mask_image, max_words=100,scale=4).generate_from_frequencies(content)
    # Display the generated image:
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file('wordcloud.jpg')
    plt.show()
    
if __name__ == "__main__":
    fetch_sina_news()
    extract_words()
