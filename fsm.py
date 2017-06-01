from transitions.extensions import GraphMachine

import telegram

import urllib

from urllib.request import urlopen

from bs4 import BeautifulSoup


web="http://mojim.com/"

webend=".html?t1"

herf_url="http://mojim.com"

id_web="f"

a_name="aa"

google_web="https://www.google.com.tw/?gfe_rd=cr&ei=fqUuWfioFcrkqAGZg5X4BQ#q="

drama_web="http://tw.dorama.info/cast/cast_search.php?sop=1&find="

per_web="http://dorama.info"

youtube_web="https://www.youtube.com/user/"

wiki_web="https://zh.wikipedia.org/wiki/"


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def article(self, update):
        text = update.message.text
        return text.lower() == '/start'

    def on_enter_article(self, update):
        reply = telegram.ReplyKeyboardRemove()
        update.message.reply_text(text = "Welcome,Please enter your favorite Artist.",
                                  reply_markup=reply)


    def search(self, update):
        global a_name
        a_name = update.message.text
        print(a_name)
        return 1

    def on_enter_search(self, update):
        custom_keyboard = [['Works'],
                           ['Reference'],
                           ['Other']]
        reply = telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text(text = "Which item you want to find?",
                                  reply_markup=reply)

    def on_exit_search(self, update):
        reply = telegram.ReplyKeyboardRemove()
        update.message.reply_text(text="Just another question",
                                  reply_markup=reply)

    def works(self, update):
        text = update.message.text
        return text.lower() == 'works'

    def on_enter_works(self, update):
        custom_keyboard = [['Music'],
                           ['Drama']]
        reply = telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text(text = "What kind of work you want to find?",
                                  reply_markup=reply)

    def on_exit_works(self, update):
        reply = telegram.ReplyKeyboardRemove()
        update.message.reply_text(text = "Start Search!",
                                  reply_markup=reply)
    def other(self, update):
        text = update.message.text
        return text.lower() == 'other'

    def on_enter_other(self, update):
        custom_keyboard = [['YoutubeVEVO'],
                           ['WIKI']]
        reply = telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text(text = "What kind of Infornation you want to find?",
                                  reply_markup=reply)

    def on_exit_other(self, update):
        reply = telegram.ReplyKeyboardRemove()
        update.message.reply_text(text = "Start Search!",
                                  reply_markup=reply)

    def reference(self, update):
        text = update.message.text
        return text.lower() == 'reference'

    def on_enter_reference(self, update):
        custom_keyboard = [['Profile'],
                           ['FB FANS CLUB']]
        reply = telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text(text = "What kind of reference you want to find?",
                                  reply_markup=reply)

    def on_exit_reference(self, update):
        reply = telegram.ReplyKeyboardRemove()
        update.message.reply_text(text = "Start Search!",
                                  reply_markup=reply)

    def profile(self, update):
        text = update.message.text
        return text.lower() == 'profile'

    def on_enter_profile(self, update):
        global a_name
        signal = 0
        for_search = a_name
        a_name = a_name.replace(" ","+")
        res = urllib.request.urlopen((drama_web+a_name))
        soup = BeautifulSoup(res, 'html.parser')
        content = soup.select('.td2_g')
        temp=" "
        output=""
        for x in content:
            temp = x.get_text().lower()
            if temp.find(for_search) != (-1):
                id_web = x.find('a')["href"]
                signal = 1
                break
            else:
               signal = 0
        if signal == 1:
            res2 = urllib.request.urlopen((per_web+id_web))
            soup2 = BeautifulSoup(res2, 'html.parser')
            content2 = soup2.select('.fcol_cnt')
            for x in content2:
                ss = x.get_text()
                ss = ss.replace(" ","")
                output = output+ ss +"\n"
            update.message.reply_text("Here You Are!")
            update.message.reply_text(output)
            self.go_back(update)
        else:
            update.message.reply_text("Don't Match,try again!")
            self.go_back(update)


    def w_music(self, update):
        text = update.message.text
        return text.lower() == 'music'

    def on_enter_w_music(self, update):
        global a_name
        list_name = a_name.split()
        print(len(list_name))
        if len(list_name) != 1:
            a_name=""
            for x in list_name:
                a_name = x + "+" + a_name
        print(a_name)
        res = urllib.request.urlopen((web+a_name+webend))
        soup = BeautifulSoup(res, 'html.parser')
        content = soup.select('.mxsh_ulz')[0]
        content = content.find('a')
        print(content)
        if content == None:
            update.message.reply_text("Doesn't match!Try again")
            self.go_back(update)
        else:
            id_web = content["href"]
            res2 = urllib.request.urlopen((herf_url+id_web))
            soup2 = BeautifulSoup(res2, 'html.parser')
            content2 = soup2.select('.hc1')
            output = " "
            for x in content2:
                output = output + x.get_text() + "\n"
            update.message.reply_text("Here You Are!")
            update.message.reply_text(output)
            self.go_back(update)

    def w_drama(self, update):
        text = update.message.text
        return text.lower() == 'drama'

    def on_enter_w_drama(self, update):
        global a_name
        signal = 0
        for_search = a_name
        a_name = a_name.replace(" ","+")
        res = urllib.request.urlopen((drama_web+a_name))
        soup = BeautifulSoup(res, 'html.parser')
        content = soup.select('.td2_g')
        temp=" "
        for x in content:
            temp = x.get_text().lower()
            if temp.find(for_search) != (-1):
                id_web = x.find('a')["href"]
                signal = 1
                break
            else:
               signal = 0
        if signal == 1:
            res2 = urllib.request.urlopen((per_web+id_web))
            soup2 = BeautifulSoup(res2, 'html.parser')
            content2 = soup2.select('.td2_g')
            temp2=" "
            output=""
            for x in content2:
                temp2 = x.get_text()
                if(temp2.find("＝") != (-1)):
                    output = temp2 + output + "\n"
            update.message.reply_text("Here You Are!")
            update.message.reply_text(output)
            self.go_back(update)
        else:
            update.message.reply_text("Don't Match,try again!")
            self.go_back(update)

    def fb(self, update):
        text = update.message.text
        return text.lower() == 'fb fans club'


    def on_enter_fb(self, update):
        global a_name
        list_name = a_name.split()
        print(len(list_name))
        if len(list_name) != 1:
            a_name=""
            for x in list_name:
                a_name = a_name+x
        update.message.reply_text("https://zh-tw.facebook.com/"+a_name.lower())
        self.go_back(update)

    def youtube(self, update):
        text = update.message.text
        return text.lower() == 'youtubevevo'

    def on_enter_youtube(self, update):
        global a_name
        list_name = a_name.split()
        print(len(list_name))
        if len(list_name) != 1:
            a_name=""
            for x in list_name:
                a_name = a_name+x
        update.message.reply_text(youtube_web+a_name.lower()+"VEVO")
        self.go_back(update)

    def wiki(self, update):
        text = update.message.text
        return text.lower() == 'wiki'

    def on_enter_wiki(self, update):
        global a_name
        list_name = a_name.split()
        print(len(list_name))
        if len(list_name) != 1:
            a_name=""
            for x in list_name:
                a_name = a_name+x
        update.message.reply_text(wiki_web+a_name.lower())
        self.go_back(update)


        
         


