from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

import gensim
from nltk.tokenize import RegexpTokenizer


def main():
    sections = []
    tokenizer = RegexpTokenizer(r'\w+')
    with open('../data/laws/uscode/uscode.jsonlines', 'r') as fin:
        for line in fin:
            sections.append(json.loads(line)['section']['text'])
    print(len(sections))
    uscode_documents = 'uscode_sections_as_documents.txt'
    with open(uscode_documents, 'w') as fout:
        for section in sections:
            fout.write(' '.join(tokenizer.tokenize(section)) + '\n')
    documents = gensim.models.doc2vec.TaggedLineDocument(uscode_documents)
    model = gensim.models.doc2vec.Doc2Vec(documents, size=100)
    model.save('uscode_sections_doc2vec.txt')


if __name__ == '__main__':
    main()
