import spacy
from qwizkoolnlp.article.Sentence import Sentence
from qwizkoolnlp.dictionary.QkDictionary import QkDictionary
from qwizkoolnlp.dictionary.QkDictionaryNLP import QkDictionaryNLP

class Article:
    """
    Base Article type

    """

    def __init__(self, title, ctx):
        self.title = title
        self.content = ''
        self.sentences = []
        self.ctx = ctx
        self.nlp = ctx.nlp

    def set_content(self, content):
        self.content = content

    def parse(self):
        print('Parsing content about ' + self.title)
        self.doc = self.nlp(self.content)
        self.dictionary = QkDictionaryNLP(self.doc, self.ctx)

        for count, sent in enumerate(self.doc.sents, start=1):
            print('Generating sentences: ' + str(count), end='\r')
            self.sentences.append(Sentence(sent.text, self))              
        print()

        #print ('Lines of information collected = {}'.format(str(len(self.sentences))))

        for count, sentence in enumerate(self.sentences, start=1):
            print('Parsing Sentence: ' + str(count), end='\r')
            sentence.parse()    
        print()

        print ('\n' + self.title + ': [ {} ]'.format(self.sentences[0]))

    def get_all_nouns(self):
        nouns = []
        for token in self.doc:
            if token.pos_ == 'PROPN':
                nouns.append(token.text)           
        return nouns    

    def get_all_ents(self):
        ents = []
        for ent in self.doc.ents:
            ents.append(ent.text)
        return ents 

    def is_subject_used(self, subject):
        for sentence in self.sentences:
            if sentence.question is not None:
                if sentence.question.answer.lower() == subject.lower():
                    return True
        return False        

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return "Article({})".format(self.title)


