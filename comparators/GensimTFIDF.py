from comparators.Comparator import Comparator
from gensim import corpora, models, similarities


class GensimTFIDF(Comparator):
    STOPWORDS = []
    MODEL = None
    DICTIONARY = None
    NUMBER_OF_TOKENS = 0

    def __init__(self):
        """ Initialize GensimTFIDF model.
        """

        # get stopwords list
        # st = StopWords()
        self.STOPWORDS = super().get_stopwords()

    def train(self, questions_path):
        # get questions
        with open(questions_path, 'r') as ifile:
            questions = ifile.readlines()

        # remove stop words and tokenize
        texts = [[word for word in document.lower().split() if word not in self.STOPWORDS]
                 for document in questions]

        self.DICTIONARY = corpora.Dictionary(texts)
        self.NUMBER_OF_TOKENS = len(self.DICTIONARY)
        corpus = [self.DICTIONARY.doc2bow(text) for text in texts]

        # store to disk
        # corpora.MmCorpus.serialize('/tmp/gensim_tfidf_corpus' + datetime.now().strftime('%H_%M_%S') + '.mm', corpus)
        # dictionary.save('/tmp/gensim_tfidf_dict' + datetime.now().strftime('%H_%M_%S') + '.dict')

        self.MODEL = models.TfidfModel(corpus)

    def must_train(self):
        return True

    def compare(self, question1, question2):
        # get bow vec of questions according to dictionary generated
        question1_vec = self.DICTIONARY.doc2bow(question1.lower().split())
        question2_vec = self.DICTIONARY.doc2bow(question2.lower().split())

        # get questions representation in tfidf space vector
        question1_rep = self.MODEL[question1_vec]
        question2_rep = self.MODEL[question2_vec]
        # print question1_rep, question2_rep

        # WARNING! This new_corpus is already in tfidf space vector
        new_corpus = []
        new_corpus.append(question1_rep), new_corpus.append(question2_rep)
        index = similarities.MatrixSimilarity(new_corpus, num_features=self.NUMBER_OF_TOKENS)

        sims = index[new_corpus]
        # print sims[0][1]

        # transform to dense vec
        # question1_dense_vec = matutils.corpus2dense(question1_rep, num_terms=self.NUMBER_OF_TOKENS)
        # question2_dense_vec = matutils.corpus2dense(question2_rep, num_terms=self.NUMBER_OF_TOKENS)
        # print question1_dense_vec, question2_dense_vec

        # get distance
        # distance = super(GensimTFIDFComparator, self).calculate_distance(question1_dense_vec, question2_dense_vec)
        distance = 1 - sims[0][1]

        return distance
