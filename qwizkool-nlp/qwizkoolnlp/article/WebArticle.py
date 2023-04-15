from qwizkoolnlp.article.Article import Article
import urllib.request

class WebArticle(Article):
    def __init__(self, name, url, ctx):
        Article.__init__(self, name, ctx)
        self.url = url

    def open(self):
        webUrl = urllib.request.urlopen(self.url)
        print ("result code: " + str(webUrl.getcode()))

        # read the data from the URL and store it
        data = webUrl.read()
        self.set_content(data)
        print(self.content)

        return self.title
