# 이후 Elastic Search로 Refac

import helloflask.tedfunctions as f
from pprint import pprint
class ElasticSearch():

    talkcnt = 0    
    engtalk = []
    diffs = []
    kortalk = []
    shows=[]
    def __init__ (self):

        # 전체 Talk의 수 구하기
        conn = f.get_conn()
        cur = conn.cursor()
        
        sqltalkcnt = ''' select (@rownum := @rownum + 1) r
                        from Talk t, (select @rownum := 0) rn
                        order by r desc
                        limit 1; '''

        sqlisdiff = 'select talk_id from Talk where diff = 0'
        
        cur.execute(sqltalkcnt)
        self.talkcnt = cur.fetchall()[0][0]

        cur = conn.cursor()
        cur.execute(sqlisdiff)
        self.diffs = cur.fetchall()

    def engtoKor(self, search):
        self.engtalk = []
        engsentences = []
        # foresentence = []
        # lastsentence = []
        for t in range(1, 10):
            if (t,) in self.diffs:
                continue
            # 검색
            s = ''
            s = search[0]
            # print("search>>>>>>>", search)
            sqlEngSearch = '''select engcue from English 
                        where eng regexp '([{}{}]{})'
                        and talk_id = {}'''.format(s.lower(), s.upper(), search[1:], t)

            conn = f.get_conn()
            cur = conn.cursor()
            cur.execute(sqlEngSearch)
            rows = cur.fetchall()
            cur.close()

            # print("rows>>>>>>>>>", rows)

            # 검색어가 없는 경우
            if len(rows) == 0:
                continue
            # 검색어가 있는 경우
            else:
                for row in rows:
                    cue = row[0]
                    self.engtalk.append((t, cue))
                    sentence = ''
                    sqleng = 'select eng from English where engcue between {} and {} and talk_id = {}'.format(cue-2, cue+2, t)
                    # print(sqlss)
                    cur = conn.cursor()
                    cur.execute(sqleng)
                    rows2 = cur.fetchall()
                    cur.close()
                    # print(rows2)
                    foresentence = ' '
                    lastsentence = ' '
                    for idx, r in enumerate(rows2):
                        if idx == 0:
                            foresentence = r
                        elif idx == len(r) - 1:
                            lastsentence = r
                        else:
                            sentence += (r[0]+' ')
                    # print(sentence)
                    sentences = {'foresentence' : foresentence, 'sentence':sentence, 'lastsentence' : lastsentence}
                    engsentences.append(sentences)
        # print("engsentences>>>>>>", engsentences)

        return engsentences        

    def engtoKorequiv(self, search):
        engsentences = self.engtoKor(search)
        tshows = []
        lang = 'English'
        n=1

        for e, engt in enumerate(self.engtalk):
            strs = ''
            cue = engt[1]
            tid = engt[0]

            # 만일 첫 문장인 경우
            if cue == 1:
                sqlKorSearch = '''select kor from Korean 
                    where korcue between {} and {}
                    and talk_id = {}'''.format(cue, cue+3, tid)

            # 첫 문장이 아닌 경우
            else:     
                sqlKorSearch = '''select kor from Korean 
                    where korcue between {} and {}
                    and talk_id = {}'''.format(cue-2, cue+2, tid)

            conn = f.get_conn()
            cur = conn.cursor()
            cur.execute(sqlKorSearch)
            enrows = cur.fetchall() # tuple
            cur.close()
            
            a=[]
            for english in enrows:
                a.append(english[0]) # eng
            

            # 세 개의 문장을 하나의 string으로 만들기
            foreresult = ' '
            lastresult = ' '
            for idx, i in enumerate(a):
                if idx == 0:
                    foreresult = i
                elif idx == len(a) -1 :
                    lastresult = i
                else:
                    strs += i + ' '
            show = {'number' : n, 'tid' : tid, 'cue':cue, 'engsentences':engsentences[e]['sentence'], 'foreresult':foreresult, 'lastresult':lastresult, 'result':strs, 'lang': lang,
                    'foresentence':engsentences[e]['foresentence'][0], 'lastsentence':engsentences[e]['lastsentence'][0]}
            # print(show)
            # return

             # tags 가져오기
             
            tagSearch = ''' select t.title, t.tags, s.name from Talk t inner join TalkSpeaker ts on                     t.talk_id = ts.talk_id
	        inner join Speaker s on ts.speaker_id= s.speaker_id where t.talk_id={}'''.format(tid)
            cur = conn.cursor()
            cur.execute(tagSearch)
            tagrows = cur.fetchall()
            cur.close()
            print("tt>>", tagrows)

            show['tags'] = tagrows[0][1].split(',')
            show['title'] = tagrows[0][0]
            show['speaker'] = tagrows[0][2]
            tshows.append(show)
            tshows = sorted(tshows, key = lambda t:t['number'], reverse=True)
            n+=1
        print(tshows)

        return tshows

    def kortoEng(self, search):
        self.kortalk = []
        korsentences = []
        # int(self.talkcnt)+1
        for t in range(1, 10):
            if (t,) in self.diffs:
                continue

            # 검색
            sqlKorSearch = '''select korcue from Korean 
                        where kor like '%{}%'
                        and talk_id = {}'''.format(search, t)
            conn = f.get_conn()
            cur = conn.cursor()
            cur.execute(sqlKorSearch)
            rows = cur.fetchall()
            cur.close()

            # 검색어가 없는 경우
            if len(rows) == 0:
                continue
            # 검색어가 있는 경우
            else:
                for row in rows:
                    cue = row[0]
                    self.kortalk.append((t, cue))
                    sentence = ''
                    sqlkor = 'select kor from Korean where korcue between {} and {} and talk_id = {}'.format(cue-2, cue+2, t)
                    # print(sqlss)
                    cur = conn.cursor()
                    cur.execute(sqlkor)
                    rows2 = cur.fetchall()
                    cur.close()
                    # print(rows2)
                    foresentence = ' '
                    lastsentence = ' '

                    for idx, r in enumerate(rows2):
                        if idx == 0:
                            foresentence = r
                        elif idx == len(rows2) - 1:
                            lastsentence = r
                        else:
                            sentence += (r[0]+' ')
                        
                    # print(sentence)
                    sentences = {'foresentence' : foresentence, 'sentence':sentence, 'lastsentence' : lastsentence}
                    korsentences.append(sentences)
        # print("korsentences>>>>>>", korsentences)
        return korsentences

    def kortoEngequiv(self, search):
        lang = 'Korean'
        korsentences = self.kortoEng(search)
        tshows = []
        n=1

        # print("kkkkkkkkkkk>", self.kortalk)
        for k, kort in enumerate(self.kortalk):
            strs = ''
            cue = kort[1]
            tid = kort[0]

            # 만일 첫 문장인 경우
            if cue == 1:
                sqlEngSearch = '''select eng from English 
                    where engcue between {} and {}
                    and talk_id = {}'''.format(cue, cue+3, tid)

            # 첫 문장이 아닌 경우
            else:     
                sqlEngSearch = '''select eng from English 
                    where engcue between {} and {}
                    and talk_id = {}'''.format(cue-2, cue+2, tid)

            conn = f.get_conn()
            cur = conn.cursor()
            cur.execute(sqlEngSearch)
            enrows = cur.fetchall()
            # print(sqlEngSearch) # tuple
            cur.close()
            # print("en>>>>", enrows)
            
           
            
            a=[]
            for english in enrows:
                a.append(english[0]) # eng
            # print("aaaaaaaaaaa> ", a)

            # 세 개의 문장을 하나의 string으로 만들기
            foreresult = ' '
            lastresult = ' '
            # print("aaaaaaaaaaaaaa>", len(a))

            for idx, i in enumerate(a):
                if idx == 0:
                    foreresult = i
                elif idx == len(a) - 1:
                    lastresult = i
                else:
                    strs += i + ' '
            # print("ffffffff>", foreresult)
            # print("lllll>", lastresult)
            # print("sssssssssss>", strs)

            show = {'number' : n, 'tid' : tid, 'cue':cue, 'korsentences':korsentences[k]['sentence'], 'foreresult':foreresult, 'lastresult':lastresult, 'result':strs, 'lang': lang, 'foresentence':korsentences[k]['foresentence'][0], 'lastsentence':korsentences[k]['lastsentence'][0]}
            # print("show>>>>>", show)
            # # 세 개의 문장을 하나의 string으로 만들기
            # for i in a:
            #     strs += i + ' '
            # show = {'number' : n, 'tid' : tid, 'cue':cue, 'korsentences':korsentences[k], 'result':strs, 'isShowTags': False, 'lang':lang}

             # tags 가져오기
            tagSearch = ''' select t.title, t.tags, s.name from Talk t inner join TalkSpeaker ts on                     t.talk_id = ts.talk_id
	        inner join Speaker s on ts.speaker_id= s.speaker_id where t.talk_id={}'''.format(tid)
            cur = conn.cursor()
            cur.execute(tagSearch)
            tagrows = cur.fetchall()
            cur.close()
            # print("tt>>", tagrows)

            # for m in tagrows:
            #     tag = m[0]
            #     print("t>>>", tag)
                
            #     # 같은 talk_id를 갖고 있는 경우 tag들의 중복 append 방지
            #     if tag in tags:
            #         continue
            #     else:
            #         tags.append(tag)

            # show['tags'] = tags
            show['tags'] = tagrows[0][1].split(',')
            show['title'] = tagrows[0][0]
            show['speaker'] = tagrows[0][2]

            # self.shows[n] = show
            tshows.append(show)
            n+=1
        # print(tshows)
        # print(n)
        return tshows
                