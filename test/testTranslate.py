import urllib
import urllib2
import re


# curl -A "Mozilla/5.0" 'http://translate.google.com/translate_a/t?client=t&text=I%20am%20Hank.&hl=en&sl=auto&tl=zh-TW&ie=UTF-8&oe=UTF-8&multires=1&otf=2&ssel=0&tsel=0&sc=1'
url = 'http://translate.google.com/translate_a/t?client=t&text=%s&hl=en&sl=auto&tl=zh-TW&ie=UTF-8&oe=UTF-8&multires=1&otf=2&ssel=0&tsel=0&sc=1'
word = "What is your favorite job?"

word = urllib.quote_plus(word)
request = urllib2.Request(url % word)
request.add_header('User-Agent', 'Mozilla/5.0')
opener = urllib2.build_opener()
data = opener.open(request).read()
print data
m = re.search('^\[+"(.+?)",', data)
print m.group(1)