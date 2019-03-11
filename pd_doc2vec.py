import re
from scipy import sparse
import gensim
from tqdm import tqdm
from gensim.models.doc2vec import TaggedDocument
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from nltk.tokenize import TweetTokenizer

class doc2vec:

                
    def tokenization(self, document):
        return re.findall(self.w, document)
                   # tokenized_words = self.tknzr.tokenize(datapoint[X].lower())

    def __init__(self, df, X, Y, build=False):
        self.w = re.compile("\w+", re.I)
        if 'basestring' not in globals():
            basestring = str
        self.tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
        # Hyperparameters : https://arxiv.org/pdf/1607.05368.pdf
        self.vector_size = 300
        self.window_size = 15
        self.min_count = 2
        self.sampling_threshold = 1e-4
        self.negative_size = 5
        self.train_epoch = 50
        self.dm = 0
        self.worker_count = 7


        labeled_sentences = []
        df_tags = []

        if isinstance(Y, basestring):
            df_tags.append(Y)
        elif isinstance(Y, list):
            df_tags = Y
        elif not isinstance(Y, list):
            raise TypeError
        self.df = df
#         print(self.df)
        self.x = X
        self.y = Y
        self.df_tags = df_tags
        self.testseries = df[df_tags[0]].unique()
        self.testseries_name = df_tags[0]
        if build == True:
            for index, datapoint in df.iterrows():
                tokenized_words = self.tokenization(datapoint[X])
                labeled_sentences.append(TaggedDocument(words=tokenized_words, tags=[datapoint[i] for i in df_tags]))
            model = gensim.models.doc2vec.Doc2Vec(vector_size=self.vector_size,
                                                  window_size=self.window_size,
                                                  min_count=self.min_count,
                                                  sampling_threshold=self.sampling_threshold,
                                                  negative_size=self.negative_size,
                                                  train_epoch=self.train_epoch,
                                                  dm=self.dm,
                                                  worker_count=self.worker_count)
            model.build_vocab(labeled_sentences)
            model.train(labeled_sentences, total_examples=model.corpus_count, epochs=model.epochs)
            self.model = model


    def score(self, verbose=False):

        df = self.df
        X = self.x
        Y =self.y
        self.verbose = verbose
        if 'basestring' not in globals():
            basestring = str

        labeled_sentences = []
        df_tags = []

        if isinstance(Y, basestring):
            df_tags.append(Y)
        elif isinstance(Y, list):
            df_tags = Y
        elif not isinstance(Y, list):
            raise TypeError
       
    
    
        for col in self.df_tags:
            print(col)
            total_accuracy = 0
            total_label_accuracy = []




            for i in df[col].unique():
                total_label_accuracy.append(0)
            iterations = 1
            for i in (range(iterations)):

                train, test = train_test_split(self.df, shuffle=True, test_size=0.05)

                for index, datapoint in train.iterrows():
                    tokenized_words = self.tokenization(datapoint[X])
                    

                    labeled_sentences.append(TaggedDocument(words=tokenized_words, tags=[datapoint[i] for i in df_tags]))

                model = gensim.models.doc2vec.Doc2Vec(vector_size=self.vector_size,
                                                      window_size=self.window_size,
                                                      min_count=self.min_count,
                                                      sampling_threshold=self.sampling_threshold,
                                                      negative_size=self.negative_size,
                                                      train_epoch=self.train_epoch,
                                                      dm=self.dm,
                                                      worker_count=self.worker_count)

                model.build_vocab(labeled_sentences)
                model.train(labeled_sentences, total_examples=model.corpus_count, epochs=model.epochs)
                self.model = model

                test['results'] = self.predict(test[X])
                labelaccuracy = f1_score(test[self.testseries_name], test['results'], average=None)
                total_label_accuracy= [x + y for x, y in zip(total_label_accuracy, labelaccuracy)]
                accuracy = accuracy_score(test[self.testseries_name], test['results'])
                total_accuracy = total_accuracy + accuracy

            print("Accuracy Score: ", total_accuracy/iterations)

            total_label_accuracy = [i/iterations for i in total_label_accuracy]
            print("Label Score: ", total_label_accuracy)

        return [total_label_accuracy, accuracy]


    def predict_taggedtext(self,
                           document):  # takes in a taged document and infers vector and returns whether it is releveant or not (1 or 0)
        inferred_vector = document
        inferred_vector = self.model.infer_vector(inferred_vector)
        sims = self.model.docvecs.most_similar([inferred_vector], topn=len(self.model.docvecs))
        return sims

    def predict_text(self, document):  # takes in a string and infers vector and returns vectors and distance
        tokenized_words = self.tokenization(document)

        inferred_vector = TaggedDocument(words=tokenized_words, tags=["inferred_vector"])[0]
        inferred_vector = self.model.infer_vector(inferred_vector)
        sims = self.model.docvecs.most_similar([inferred_vector], topn=len(self.model.docvecs))
        tags = []
        for col in self.df_tags:
            tags.append([rec for rec in sims if rec[0] in set(self.df[col].unique())][0][0])
        return tags
    
    def predict_sims(self, document):  # takes in a string and infers vector and returns vectors and distance
        tokenized_words = self.tokenization(document)


        inferred_vector = TaggedDocument(words=tokenized_words, tags=["inferred_vector"])[0]
        inferred_vector = self.model.infer_vector(inferred_vector)
        sims = self.model.docvecs.most_similar([inferred_vector], topn=len(self.model.docvecs))
        return sims
    
    def get_vector(self, document):  # takes in a string and infers vector and returns vectors and distance
        tokenized_words = self.tokenization(document)


        inferred_vector = TaggedDocument(words=tokenized_words, tags=["inferred_vector"])[0]
        inferred_vector = self.model.infer_vector(inferred_vector)
        return sparse.csr_matrix(inferred_vector).toarray()

    def predict_text_main(self, document, col=None):  # takes in a string and infers vector and returns vectors and distance
        if col == None:
            col = self.df_tags[0]
        tokenized_words = self.tokenization(document)


        inferred_vector = TaggedDocument(words=tokenized_words, tags=["inferred_vector"])[0]
        inferred_vector = self.model.infer_vector(inferred_vector)
        sims = self.model.docvecs.most_similar([inferred_vector], topn=len(self.model.docvecs))
#         print([rec for rec in sims if rec[0] in set(self.df[self.df_tags[0]].unique())])
        return [rec for rec in sims if rec[0] in set(self.df[col].unique())][0][0]



    def label_sentences(self, df, X, Y):
        # trick for py2/3 compatibility
        if 'basestring' not in globals():
            basestring = str

        labeled_sentences = []
        df_tags = []

        if isinstance(Y, basestring):
            df_tags.append(Y)
        elif isinstance(Y, list):
            df_tags = Y
        elif not isinstance(Y, list):
            raise TypeError
        self.df = df
        self.x = X
        self.y = Y

        for index, datapoint in df.iterrows():
            tokenized_words = self.tokenization(document)


            labeled_sentences.append(TaggedDocument(words=tokenized_words, tags=[datapoint[i] for i in df_tags]))
        return labeled_sentences

    def predict(self, X):  # Takes a series of text and returns a series of predictions
        if self.verbose:
            from tqdm import tqdm
            tqdm.pandas()
            return X.progress_apply(self.predict_text_main)
        else:
            return X.apply(self.predict_text_main)



