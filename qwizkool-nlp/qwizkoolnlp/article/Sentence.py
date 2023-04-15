import spacy
from qwizkoolnlp.quiz.Question import Question
from qwizkoolnlp.dictionary.QkDictionary import QkDictionary
import random

class Sentence:
    """
    Base Sentence type

    """

    def __init__(self, text, article):
        self.nlp = article.nlp
        self.text = text
        self.article = article
        self.subjects = []
        self.question = None

    # Is this a good sentence for converting to a question?
    def is_candidate_sentence(self):

        # Skip sentences with non english characters
        if not QkDictionary().is_english_chars(self.text):
            return False

        # Skip sentences with first letter not upper case
        if not self.text[0].isupper():
            return False    

        if self.text.split()[0] in ['They', 'Those', 'These', 'This', 'It']:
            return False
        
        # Start simple sentence detection
        # If the first word is a pronoun, it is most likely
        # a continuation sentence. So skip it.
        if self.doc[0].pos_ == 'PRON':
            return False

        # Absence of a verb indicates a non simple sentence
        for token in self.doc:
            if token.pos_ == 'VERB':
                break
        else:
            return False

        return True    


    # Brute force detections based on NOUNs
    def find_subjects_noun(self):
        # Pick the candidates for 'answer' words
        for token in self.doc:
            if token.pos_ == 'PROPN':
                self.subjects.append({'text' : token.text})
                #print ("Subject = " + token.text)

    # Detections based on named entity detection
    def find_subjects_ent(self):
        for ent in self.doc.ents:
            self.subjects.append({'text' : ent.text, 'label':ent.label_})
            #print(ent.text, ent.label_)

    # Remove subjects that aren't desirable
    def clean_subjects(self):
        for subject in self.subjects:
            if (subject['text'].lower() == self.article.title.lower() or \
                    subject['text'].lower() in (name.lower() for name in self.article.title.split())) or \
                    self.article.is_subject_used(subject['text']): # Try to avoid repeating the same answer appearing in different questions
                #print ("Removing subject " + subject['text'])
                self.subjects.remove(subject)
   

    def parse(self):
        #print('Parsing content in [{}]'.format(self.text))
        self.doc = self.nlp(self.text)
        if not self.is_candidate_sentence():
            return

        self.find_subjects_ent()
        self.clean_subjects()

        if self.subjects:   # not empty
            #print('Simple sentence [{}]'.format(self.text))
            #print('subjects:{}'.format(self.subjects))

            # Create a fill in blanks type of question
            # for now, just use one subject randomly from the list
            subject = random.choice(self.subjects)
            question_str = self.text.replace(subject['text'], '______', 1)  # replace only the first occurrence

            # Exclude the title from answer choices
            exclude_list = self.article.title.split()
            ret = self.article.dictionary.get_similar(subject['text'], subject['label'], exclude_list, 3)
            self.question = Question(question_str, ret['answer'], ret['choices'])
            #print(self.question)

    def __str__(self):
        return str(self.text)

    def __repr__(self):
        return "Sentence({})".format(self.text)


