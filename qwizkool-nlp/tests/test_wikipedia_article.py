import unittest

import qwizkoolnlp
from qwizkoolnlp.article.WikipediaArticle import WikipediaArticle
from qwizkoolnlp.nlp.QkContext import QkContext

class TestOpen(unittest.TestCase):
    def test_wiki_open(self):
        """
        Test that a wiki article can be opened
        """
        qk_ctx = QkContext('small')
        title = "Gorilla"
        wiki_article = WikipediaArticle(title, qk_ctx)
        wiki_article.open()
        self.assertEqual(wiki_article.title, title)

if __name__ == '__main__':
    unittest.main()
