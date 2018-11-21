import re
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import LabelEncoder
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from keras.models import load_model

DICT_PATH = './extra_prebuilt/corpus.npy'
TFIDF_PATH = './extra_prebuilt/tfidf.pkl'
PREBUILD_MODEL_PATH = './prebuilt_model/mpl.h5'
LABELS_PATH = './extra_prebuilt/classes.npy'

porter = PorterStemmer()
stop = stopwords.words('english')

def text_preprocessor(text):
    text = re.sub('[\W]+', ' ', text.lower())
    tokenized_str = ""
    for word in text.split():
        if word not in stop:
            tokenized_str += " " + porter.stem(word)
    return tokenized_str.strip()

def text2sequence():
    pass

def init():
    # load vocabulary
    vocab = np.load(DICT_PATH).item()
    print('Finish loading vocab...')
    # init CountVectorizer
    count = CountVectorizer(vocabulary=vocab)
    print('Finish loading CountVectorizer...')
    # load tfidf
    tfidf = pickle.load(open(TFIDF_PATH, "rb"))
    print('Finish loading tfidf...')
    # load classes
    encoder = LabelEncoder()
    encoder.classes_ = np.load(LABELS_PATH)
    print('Finish loading classess...')
    # load model
    model = load_model(PREBUILD_MODEL_PATH)
    print('Finish loading model...')

    return count, tfidf, encoder, model

count, tfidf, lb_encoder, model = init()

def predict(txt):
    new_descript = text_preprocessor(txt)
    new_sequences = count.transform([new_descript]).toarray()
    new_tfidf_sequences = tfidf.transform(new_sequences).toarray()
    predicted_indices = model.predict_classes(new_tfidf_sequences)
    return lb_encoder.classes_[predicted_indices]

def predict_multi(list_txt):
    new_descripts = []
    for txt in list_txt:
        new_descripts.append(text_preprocessor(txt))
    new_sequences = count.transform(new_descripts).toarray()
    new_tfidf_sequences = tfidf.transform(new_sequences).toarray()
    predicted_indices = model.predict_classes(new_tfidf_sequences)
    return [lb_encoder.classes_[int(idx)] for idx in predicted_indices]

if __name__ == "__main__":


    txt_list = [ "1. Established since 1999 as a company under FPT Corporation, FPT Software has \nbecome the biggest software outsource service in South East Asia with ...\n2. FPT sought to reach out to the world, like other global companies, and provide \nsoftware outsourcing services. FPT Software was ...\n3. Company Overview. FPT Software Company Limited provides technology \nservices. It offers digital consulting services that include agile factory and \nrenovation ...\n","1. Viettel là Tập đoàn Viễn thông và Công nghệ thông tin lớn nhất Việt Nam, đồng \nthời được đánh giá là một trong những công ty viễn thông có tốc độ phát triển ...\n2. Viettel Group is Vietnam's largest mobile network operator. It is a state-owned ... \nIn 2014, the company announced that they were making UAVs. In 2014, Viettel \nannounced a plan to invest $1 billion in a 3G network in ...\n3. Viettel Group is currently the largest telecommunications group in Vietnam with \n76 million customers. The group consists of more than 20 subsidiary companies ...\n"]


    print("-----------------------------")
    print(txt_list)
    print("-----------------------------")
    print(predict_multi(txt_list))