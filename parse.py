from google.appengine.api import urlfetch
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Comment
import hn

class Parse():
    error = 0
    html = ''
	
    def __init__(self,url):
        self.url = url
    	try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                self.html = result.content
                
        except:
            self.error = 1

    def getTitle(self):
        soup = BeautifulSoup(self.html)
        title = soup.findAll('title')
        if(title):
            return title[0].string
        
    def getContent(self):
        return hn.grabContent(self.url,self.html).decode('ascii','ignore')
        
    def getKeyword(self):
        soup = BeautifulSoup(self.getContent())
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
 
        rmlist = [ 'script', 'style', 'img' ]
        for tag in soup.findAll():
            if tag.name.lower() in rmlist:
                tag.extract()
 
        return ''.join(soup.getText())
        
