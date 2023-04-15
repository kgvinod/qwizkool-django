import unittest

import qwizkoolnlp
from qwizkoolnlp.quiz.Question import Question

class TestOpen(unittest.TestCase):
    def test_question(self):
        """
        Test that a Question can be created and used
        """
        question_str = 'The genus Gorilla is divided into _____ species:'
        answer = 'two'
        alternates = ['three', 'nine', 'twenty two']
        question = Question(question_str, answer, alternates)
        
        # Total choices should be answer + alternates
        self.assertEqual(question.num_choices(), len(alternates) + 1)

        # There should only be one correct answer
        num_correct_answers = 0
        correct_answer = ''
        for key in range(1, question.num_choices() + 1):
            if question.is_correct_answer(key):
                num_correct_answers += 1
                correct_answer = question.get_choice_from_key(key)

        self.assertEqual(num_correct_answers, 1)
        self.assertEqual(correct_answer, answer)

if __name__ == '__main__':
    unittest.main()
