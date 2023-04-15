import random
from qwizkoolnlp.dictionary.QkDictionary import QkDictionary
from qwizkoolnlp.utils.QkDateUtils import QkDateUtils

class QkDictionaryNLP(QkDictionary):
    """
    Provide dictionary, thesaurus utilities

    """

    def __init__(self, doc, ctx):
        QkDictionary.__init__(self, [ent.text for ent in doc.ents])
        self.nlp = ctx.nlp
        self.doc = doc

        # Create a dictionary of labels => [entity text list]
        self.label_dict = {}
        for ent in self.doc.ents:
            value = self.label_dict.get(ent.label_, set())
            value.add(ent.text)
            self.label_dict[ent.label_] = value

        print(self.label_dict)

 
    def get_similar(self, word, label, exclude_list, count):
        """
        Get similar words/phrases

        E.g. Given the word 'USA', this function could return [UK, France, Canada]
             Given the word '1993' this function could return [1995, 2020, 1973]

        :param word: input word/phrase for which similar words/phrases to be generated
        :param label: entity label provided by spacy NLP library
        :param exclude_list: exclude these from the generated list
        :param count: number of similar word/phrase to be generated 
        :return: list of {count} simlar words/phrases
        """     
        ret = dict()
        ret['answer'] = ''
        ret['choices'] = []    

        # Process date phrases
        if label == 'DATE':
            ret = QkDateUtils().get_similar_dates(word, count)
            if len(ret['choices']) > 0:
                return ret
        
        ret_list = []
        candidates = list(self.label_dict.get(label, set()))

        # Try continously until we get enough
        num_tries = len(candidates) * 10
        for _ in range(num_tries):
            rnd_idx = random.randrange(len(candidates))
            choice_word = candidates[rnd_idx]

            if not self.is_english_chars(choice_word):
                continue

            # Skip small words    
            if len(choice_word) <=2:
                continue 

            # We don't need one that's same as the input word
            if choice_word.lower() == word.lower():
                continue

            # We don't need anything from the exclude list
            if choice_word.lower() in (name.lower() for name in exclude_list):
                continue    

            # Skip duplicates
            if choice_word.lower() in (name.lower() for name in ret_list):
                continue  

            ret_list.append(choice_word)
            if len(ret_list) >= count:
                break

        ret['answer'] = word
        ret['choices'] = ret_list  
        return ret    

