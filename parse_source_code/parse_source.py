import bblfsh
import sys
import re
from gensim.models import Doc2Vec
import os
from gensim.models.doc2vec import TaggedDocument

#connect to babelfish client
client = bblfsh.BblfshClient("0.0.0.0:9432")

#walking through all source files of a certain type
def walk(file_type):

    type_list = []
    for root, dirnames, filenames in os.walk("code_samples"):
        for filename in filenames:
            #check file extension here
            if filename.endswith(".%s" % file_type):
                path = os.path.join(root, filename)
                ast = client.parse(path).uast
                ast = str(ast)
                internal_types = re.findall('internal_type: "(.*)"', ast)
                type_list.append(internal_types)

    return type_list

def convert2vec(docs):

    conversion = []
    #convert to tagged document
    for d in docs:
        conversion.append(TaggedDocument(words=d, tags=["test"]))
    model = Doc2Vec(dm=0, vector_size=300, window=5)
    model.build_vocab(conversion)
    model.train(conversion, total_examples=len(docs), epochs=30)
    labels = []
    values = []
    for c in conversion:
        labels.append(c.tags[0])
        values.append(model.infer_vector(c.words, steps=20))

    return labels, values
    

if __name__ == "__main__":

    #usage: py or java
    file_type = str(sys.argv[1])
    type_list = walk(file_type)
    labels, values = convert2vec(type_list)
