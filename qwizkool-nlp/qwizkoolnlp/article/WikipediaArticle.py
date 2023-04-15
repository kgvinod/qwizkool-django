from qwizkoolnlp.article.Article import Article
import wikipedia
import re

class WikipediaArticle(Article):

    def open(self):
        # Specify the title of the Wikipedia page
        print ('Collecting information about ' + self.title)
        wiki = wikipedia.page(title=self.title)
        
        # Extract the plain text content of the page
        text = wiki.content
        
        # Clean text
        text = re.sub(r'==.*?==+', '', text)
        text = text.replace('\n', '')
        self.set_content(text)
        #print(self.content)

        return wiki.title
