import sublime
import sublime_plugin
import urllib
import urllib2
import re

url = 'http://translate.google.com/translate_a/t?client=t&text=%s&hl=en&sl=auto&tl=%s&ie=UTF-8&oe=UTF-8&multires=1&otf=2&ssel=0&tsel=0&sc=1'

class TranslateCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        settings = sublime.load_settings('Translate.sublime-settings')
        targetLang = settings.get('target_language');

        region = self.view.sel()[0]
        self.symbol = self.get_symbol(region).lower()
        self.result = translate(self.symbol, targetLang)

        view = sublime.active_window().new_file()

        edit = view.begin_edit()
        view.insert(edit, 0, self.result.decode('UTF-8'))
        view.end_edit(edit)

    def get_symbol(self, region):
        if region.begin() != region.end():
            return self.view.substr(region)

        point  = region.begin()
        region = self.view.word(point)
        symbol = self.view.substr(region)

        point  = point - region.begin()
        end = region.end() - region.begin() + 1
        pos = symbol[:point].rfind('_')
        begin = 0 if pos == -1 else pos + 1
        pos = symbol[point:].find('_')
        end = end if pos == -1 else pos + point

        return symbol[begin:end]

def translate(word, tl):
    word = urllib.quote_plus(word)
    request = urllib2.Request(url % (word, tl))

    request.add_header('User-Agent', 'Mozilla/5.0')
    opener = urllib2.build_opener()
    data = opener.open(request).read()

    m = re.search('^\[+"(.+?)",', data)
    return m.group(1)