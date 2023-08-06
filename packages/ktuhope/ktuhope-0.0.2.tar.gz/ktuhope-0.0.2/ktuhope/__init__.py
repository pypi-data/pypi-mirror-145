def matrixOperations():
    # Perform all matrix operation using python using numpy

    txt = "import numpy as np \n"\
        "a = np.array([[1,2,3],[2,4,6]]) \n"\
        "b = np.array([[2,3,4],[5,4,3]]) \n"\
        "print('Addition: ',np.add(a,b)) \n"\
        "print('Sum: ',np.sum(a)) \n"\
        "print('Difference:',np.subtract(a,b)) \n"\
        "print('Multiplied: ',np.multiply(a,b)) \n"\
        "print('Division: ',np.divide(a,b)) \n"\
        "# print('Dot: ',np.dot(a,b)) \n"\
        "print('Matrix size: ',a.size) \n"\
        "print('Transpose: ',a.T)"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt


def svd():
    # Program to perform SVD using python

    txt = "import numpy as np \n"\
        "from scipy.linalg import svd \n" \
        "a = np.array([[1, 2, 3], [2, 4, 6], [2, 3, 4]]) \n"\
        "# number of rows and columns \n"\
        "m, n = 3, 3 \n"\
        "x, y, z = svd(a) \n"\
        "print('Decomposition: ', x) \n"\
        "print('Inverse: ', y) \n"\
        "print('Transpose: ', z) \n"\
        "# Creating array of zeroes with same rows and column \n"\
        "sigma = np.zeros((m, n)) \n"\
        "for i in range(min(m, n)): \n"\
        "   sigma[i, i] = y[i] \n"\
        "a1 = np.dot(x, np.dot(sigma, z)) \n"\
        "print(a1)"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt


def knn():
    # Program to implement k-NN Classification using any
    # standard dataset available in the public domain and
    # find the accuracy of the algorithm using in build function

    txt = "from sklearn.neighbors import KNeighborsClassifier \n"\
        "from sklearn.model_selection import train_test_split \n"\
        "from sklearn.datasets import load_iris \n"\
        "from sklearn.metrics import accuracy_score \n"\
        "irisData = load_iris() \n"\
        "i = irisData.data \n"\
        "j = irisData.target \n"\
        "i_train, i_test, j_train, j_test = train_test_split( \n"\
        "    i, j, test_size=0.7, random_state=30 \n"\
        ") \n"\
        "knn = KNeighborsClassifier(n_neighbors=1) \n"\
        "knn.fit(i_train, j_train)  \n"\
        "print(knn.predict(i_test)) \n"\
        "# finding Accuracy of algorithm \n"\
        "k = knn.predict(i_test) \n"\
        "l = accuracy_score(j_test, k) \n"\
        "print('Accuracy is', l)"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt


def naiveBayes():
    # Program to implement Naïve Bayes Algorithm using any standard dataset available in the public domain and 
    # find the accuracy of the algorithm

    txt = "import pandas as pd \n"\
        "dataset = pd.read_csv('Social_Network_Ads.csv') \n"\
        "x = dataset.iloc[:, [2, 3]].values \n"\
        "y = dataset.iloc[:, -1].values \n"\
        "from sklearn.model_selection import train_test_split \n"\
        "x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=10) \n"\
        "from sklearn.preprocessing import StandardScaler \n"\
        "sc = StandardScaler() \n"\
        "x_train = sc.fit_transform(x_train) \n"\
        "x_test = sc.transform(x_test) \n"\
        "from sklearn.naive_bayes import GaussianNB \n"\
        "gnb = GaussianNB() \n"\
        "gnb.fit(x_train, y_train) \n"\
        "y_pred = gnb.predict(x_test) \n"\
        "print(y_pred) \n"\
        "from sklearn import metrics \n"\
        "print('Accuracy: ', metrics.accuracy_score(y_test, y_pred) * 100)"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt


def chunking():
    # Write a python program for natural program language processing with chunking

    txt = "import nltk \n"\
        "new='The big cat ate the little mouse who was after the fresh cheese'\n"\
        "new_tokens=nltk.word_tokenize(new)\n"\
        "print(new_tokens)\n"\
        "new_tag=nltk.pos_tag(new_tokens)\n"\
        "print(new_tag)\n"\
        "grammer=r'NP: {<DT>?<JJ>*<NN>}'\n"\
        "chunkParser=nltk.RegexpParser(grammer)\n"\
        "chunked=chunkParser.parse(new_tag)\n"\
        "print(chunked)\n"\
        "chunked.draw()\n"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt


def speechtagging():
    # Program for Natural Language Processing which performs speech tagging

    txt = "import nltk \n"\
        "from nltk.corpus import stopwords\n"\
        "from nltk.tokenize import word_tokenize, sent_tokenize\n"\
        "stop_words = set(stopwords.words('english'))\n"\
        "txt = 'Sukanya, Rajib and Naba are my good friends,'\\n"\
        "'Sukanya is getting married next year.'\\n"\
        "'Marriage is a big step in one's life.'\\n"\
        "'It is both exiting and frightening.'\\n" \
        "'But friendship is a sacred bond between people.'\\n"\
        "'It is a special kind of love between us'\\n"\
        "'Many of you must have tried searching for a friend'\\n"\
        "'but never found the right one.'\n"\
        "# sent_tokenize is one of instances of\n"\
        "# PunktSentenceTokenizer from the nltk.tokenize.punkt module\n"\
        "tokenized = sent_tokenize(txt)\n"\
        "for i in tokenized:\n\n"\
        "# words tokenizers is used to find the words\n"\
        "# and punctuation in a string\n"\
        "   wordslist = nltk.word_tokenize(i)\n"\
        "# removing stop words from word list\n"\
        "   wordslist = [w for w in wordslist if not w in stop_words]\n"\
        "# using a Tagger . which is part of speech\n"\
        "# taggger or Pos-tagger \n\n"\
        "   tagged = nltk.pos_tag(wordslist)\n"\
        "   print(tagged)\n\n"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt


def ngrams_buitin():
    # Program for Natural Language Processing which performs n-grams (Using in built functions)

    txt = "import nltk \n"\
        "from nltk.util import ngrams\n"\
        "sample = 'this is a very good book to study'\n"\
        "NGRAMS = ngrams(sequence=nltk.word_tokenize(sample), n=2)\n"\
        "for grams in NGRAMS:\n"\
        "   print(grams)\n\n"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt



def ngrams():
    # Program for Natural Language Processing which performs n-grams

    txt = "def generate(text, WordsToCombine): \n"\
        "words = text.split()\n"\
        "output = []\n"\
        "for i in range(len(words) - WordsToCombine + 1):\n"\
        "   output.append(words[i:i + WordsToCombine])\n"\
        "   return output\n\n"\
        "x = generate(text='this is a very good boook to study', WordsToCombine=3)\n"\
        "print(x)\n"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt



def scraping():
    # Program to implement scrap of any website

    txt = "# program to scrap websites and save quotes from website \n"\
        "import requests \n"\
        "from bs4 import BeautifulSoup \n"\
        "import csv \n"\
        "import lxml \n"\
        "URL = 'http://www.values.com/inspirational-quotes'\n"\
        "r = requests.get(URL)\n"\
        "print(r.content)\n"\
        "soup = BeautifulSoup(r.content, 'lxml')\n"\
        "print(soup.prettify())\n"\
        "# list to store quotes\n"\
        "quotes = []\n"\
        "table = soup.find('div', attrs={'id': 'all_quotes'})\n"\
        "for row in table.findAll('div', attrs={'class': 'col-6 col-lg-3 text-center margin-30px-bottom'}):\n"\
        "   quote = {}\n"\
        "   quote['theme'] = row.h5.text\n"\
        "   quote['url'] = row.a['href']\n"\
        "   quote['img'] = row.img['src']\n"\
        "   quote['lines'] = row.img['alt'].split(' #')[0]\n"\
        "   quote['author'] = row.img['alt'].split(' #')[1]\n"\
        "   quotes.append(quote)\n\n"\
        "filename = 'inspirational_quotes.csv'\n"\
        "with open(filename, 'w', newline='') as f:\n"\
        "w = csv.DictWriter(f, ['theme', 'url', 'img', 'lines', 'author'])\n"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt



def kmeans():
    # Program to implement k-means clustering technique using any 
    # standard dataset available in the public domain.

    txt = "import numpy as np \n"\
        "import pandas as pd \n"\
        "import matplotlib.pyplot as mtp\n"\
        "# importing dataset\n"\
        "dataset = pd.read_csv('Mall_Customers.csv')\n"\
        "x = dataset.iloc[:, [3, 4]].values\n"\
        "print(x)\n"\
        "# finding optimal no of clusters using elbow\n"\
        "from sklearn.cluster import KMeans\n"\
        "wcss_list = []\n"\
        "for i in range(1, 11):\n\n"\
        "kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)\n"\
        "kmeans.fit(x)\n"\
        "wcss_list.append(kmeans.inertia_)\n\n"\
        "mtp.plot(range(1, 11), wcss_list)\n"\
        "mtp.title('The elbow method graph')\n"\
        "mtp.xlabel('number of clusters(k)')\n"\
        "mtp.ylabel('wcss_list')\n"\
        "mtp.show()\n"\
        "# training the kmeans model on a dataset\n"\
        "kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42)\n"\
        "y_predict = kmeans.fit_predict(x)\n"\
        "print(y_predict)\n"\
        "# visualizing clusters\n"\
        "mtp.scatter(x[y_predict == 0, 0], x[y_predict == 0, 1], s=100, c='red', label='cluster1')\n"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt



def linearregression():
    # Program to implement linear and multiple regression techniques 
    # using any standard dataset available in the public domain without Built-in func

    txt = "import numpy as np\n"\
        "import matplotlib.pyplot as plt\n"\
        "def estimate_coef(x, y):\n"\
        "# no of observation\n"\
        "n = np.size(x)\n"\
        "# mean of x and y\n"\
        "m_x = np.mean(x)\n"\
        "m_y = np.mean(y)\n"\
        "# cross deviation and deviation abt x\n"\
        "SS_xy = np.sum(y * x) - n * m_y * m_x\n"\
        "SS_xx = np.sum(x * x) - n * m_x * m_x\n"\
        "# regression coefficient\n"\
        "b_1 = SS_xy / SS_xx\n"\
        "b_0 = m_y - b_1 * m_x\n"\
        "return (b_0, b_1)\n\n"\
        "def ploting(x, y, b):\n"\
        "plt.scatter(x, y, color='m', marker='o', s=30)\n"\
        "# predicting response vector\n"\
        "y_pred = b[0] + b[1] * x\n"\
        "# plotting regression line\n"\
        "plt.plot(x, y_pred, color='g')\n"\
        "plt.xlabel('x')\n"\
        "plt.xlabel('y')\n"\
        "plt.show()\n\n"\
        "def main():\n"\
        "x = np.array([19, 31, 52, 27, 39, 11])\n"\
        "y = np.array([22, 24, 16, 28, 30, 12])\n"\
        "b = estimate_coef(x, y)\n"\
        "print('Estimated coefficients:b_0 = {} \b_1 = {}'.format(b[0], b[1]))\n"\
        "ploting(x, y, b)\n\n"\
        "if __name__ == '__main__':\n"\
        "main()\n\n"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt



def linearregression_builtin():
    # Program to implement linear and multiple regression techniques 
    # using any standard dataset available in the public domain

    txt = "import numpy as np \n"\
        "from sklearn.linear_model import LinearRegression\n"\
        "x = np.array([5, 67, 44, 32, 12, 34]).reshape((-1, 1))\n"\
        "y = np.array([6, 76, 34, 23, 45, 23])\n"\
        "print(x)\n"\
        "print(y)\n"\
        "model = LinearRegression()\n"\
        "model.fit(x, y)\n"\
        "r = model.score(x, y)\n"\
        "print('coefficient of determination :', r)\n"\
        "print('intercept : ', model.intercept_)\n"\
        "print('slope : ', model.coef_)\n"\
        "y_pred = model.predict(x)\n"\
        "print('predicted response : ', y_pred)\n"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt

def webCrawl():
    #  Program to implement a simple web crawler using python

    txt = "import requests"\
        "from bs4 import BeautifulSoup"\
        "url = 'https://www.geeksforgeeks.org'"\
        "r = requests.get(url)"\
        "soup = BeautifulSoup(r.text, 'html.parser')"\
        "print(soup.prettify())"\
        "for row in soup.find_all('a'):"\
            "data = row.get['href']"\
            "f = open('abc.py', 'a')"\
            "print(data)"\
            "f.write(data)"\
            "f.write('\n')"\
            "f.close()"
    f = open("res.py", "w")
    f.write(txt)
    f.close()
    return txt


def info():
    # Use it for educational purpose only
    
    txt = "This is a sample func to try the whole package"
    return txt

