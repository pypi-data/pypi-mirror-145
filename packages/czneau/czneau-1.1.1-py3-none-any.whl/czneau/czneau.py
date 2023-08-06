'''
提供CCN类
'''

from rich.console import Console
from collections import UserDict
from typing import overload
from rich import traceback
from rich import print
import requests
import random
import time
import json

traceback.install()

##
userAgentList = [
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
"Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36",
"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
"Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
"Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
"Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
"Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
"Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
"Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
"Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
"Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
]


class CrawlData(UserDict):
    def __init__(self) -> None:
        super().__init__()

    def __len__(self) -> int:
        return super().__len__()

    @overload
    def __getitem__(self, key: int) -> dict: ...
    @overload
    def __getitem__(self, key: str) -> dict: ...
    def __getitem__(self, key) -> dict:
        return super().__getitem__(key)
    
    @overload
    def __setitem__(self, key: int, item: dict) -> None: ...
    @overload
    def __setitem__(self, key: str, item: dict) -> None: ...
    @overload
    def __setitem__(self, key: tuple, item: dict) -> None: ...
    def __setitem__(self, key, item) -> None:
        return super().__setitem__(key, item)
    
    @overload
    def __delitem__(self, key: int): ...
    @overload
    def __delitem__(self, key: str): ...
    def __delitem__(self, key):
        return super().__delitem__(key)

    def __iter__(self):
        return super().__iter__()

    def __repr__(self):
        return f'{type(self).__name__}({repr(self.data)})'

    def loadData(self, file: str) -> bool:
        r'''加载json文件'''
        try:
            print('[purple]<load start>[/purple]')
            console = Console()
            with console.status('[bold red]Start loading...') as status:
                with open(file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            print('[cyan]<load finish>[/cyan]')
        except: return False
        else: return True
    
    def saveData(self, file: str) -> bool:
        r'''保存json文件'''
        try:
            print('[purple]<save start>[/purple]')
            console = Console()
            with console.status(f'[bold red]Start saveing...', spinner_style='blue') as status:
                time.sleep(3)
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f)
            print('[cyan]<save finish>[/cyan]')
        except: return False
        else: return True


##
class CrawlStatus:
    _urlComment = 'http://czneau.com/api/comments'
    _urlNew = 'http://czneau.com/api/posts'
    _urlHot = 'http://czneau.com/api/hot'
    _referer = 'http://czneau.com/'
    _userAgent = userAgentList

    def __init__(self) -> None:
        self._pageSize = 0 # this must less than 30
        self._fromId = ''
        self._postId = ''
        self._url = ''
        self._proxies = None
        pass
    
    @property
    def urlComment(self) -> str:
        return CrawlStatus._urlComment
    @urlComment.setter
    def urlComment(self, url: str) -> bool:
        try: CrawlStatus._urlComment = url
        except: return False
        else: return True
    @property
    def urlNew(self) -> str:
        return CrawlStatus._urlNew
    @urlNew.setter
    def urlNew(self, url: str) -> bool:
        try: CrawlStatus._urlNew = url
        except: return False
        else: return True
    @property
    def urlHot(self) -> str:
        return CrawlStatus._urlHot
    @urlHot.setter
    def urlHot(self, url: str) -> bool:
        try: CrawlStatus._urlHot = url
        except: return False
        else: return True
    @property
    def referer(self) -> str:
        r'''防盗链'''
        return CrawlStatus._referer
    @referer.setter
    def referer(self, value: str) -> bool:
        try: CrawlStatus._referer = value
        except: return False
        else: return True
    @property
    def userAgent(self) -> list:
        r'''User-Agent of headers'''
        return CrawlStatus._userAgent
    @userAgent.setter
    def userAgent(self, agents) -> bool:
        try: CrawlStatus._userAgent = [agents] if type(agents) == str else agents
        except: return False
        else: return True

    @property
    def pageSize(self) -> str:
        r'''大小介于[1,30), 默认29'''
        return self._pageSize
    @pageSize.setter
    def pageSize(self, value) -> bool:
        if value <= 0 or value >=30:
            print('The size of page must in interval [1, 30)')
            return False
        try: self._pageSize = value if type(value) == str else f'{value}'
        except: return False
        else: return True
    @property
    def fromID(self) -> str:
        return self._fromId
    @fromID.setter
    def fromID(self, value) -> bool:
        try: self._fromId = value if type(value) == str else f'{value}'
        except: return False
        else: return True
    @property
    def postID(self) -> str:
        return self._postId
    @postID.setter
    def postID(self, value) -> bool:
        try: self._postId = value if type(value) == str else f'{value}'
        except: return False
        else: return True
    @property
    def url(self) -> str:
        return self._url
    @url.setter
    def url(self, value: str) -> bool:
        try: self._url = value
        except: return False
        else: return True
    @property
    def proxies(self):
        return self._proxies
    @proxies.setter
    def proxies(self, value: dict) -> bool:
        try: self._proxies = value
        except: return False
        else: return True


##
class CrawlCzNeau(CrawlStatus, CrawlData):
    _indentSize = 2

    @property
    def indentSize(self) -> int:
        return CrawlCzNeau._indentSize
    @indentSize.setter
    def indentSize(self, value: int) -> bool:
        try: CrawlCzNeau._indentSize = value
        except: return False
        else: return True

    def __init__(self) -> None:
        self.level = 0
        CrawlStatus.__init__(self)
        CrawlData.__init__(self)
    
    def _getJsonData(self, url, level=0) -> list:
        r'''获取json'''
        levelIndentSize = ' ' * self._indentSize * level
        headers = {
            'User-Agent': random.choice(self.userAgent),
            'Referer': self.referer,
        }
        params = {
            'pageSize': random.randint(15, 29) if self.pageSize == 0 else self.pageSize,
            'fromId': self.fromID,
            'postId': self.postID
        }
        proxies = self.proxies
        jsonData = {}
        try:
            resp = requests.get(url=url, headers=headers, params=params, proxies=proxies)
            resp.close()
            if resp.status_code != 200:
                print(f'\n{levelIndentSize}Response Status Code: [red]{resp.status_code}[/red]')
                return []
            jsonData = resp.json()
        except requests.exceptions.ProxyError:
            print('\n{levelIndentSize}An [red bold]ProxyError[/red bold] Raised As Expected.\n大概率 [blue]ip[/blue] 被封了. 要等段时间或加代理.')
            exit(-1)
        return jsonData['data']
    
    def _crawlMain(self, url: str, crawlTimes: int, sleepTime: int, level: int) -> int:
        r'''爬虫主循环'''
        levelIndentSize = ' ' * self._indentSize * level
        dataList = []
        for _i in range(crawlTimes):
            console = Console()
            with console.status(f'[bold yellow]Crawling Times:{_i}...', spinner='line', spinner_style='red') as status:
                sleepT = random.random() * 3 if sleepTime == None else sleepTime
                dataList = self._getJsonData(url, level+1)
                if len(dataList) == 0: break
                for dt in dataList:
                    self.data[dt['id']] = dt
                    self.fromID = dt['id']
                time.sleep(sleepT)
            print(f'{levelIndentSize}[yellow]{_i}: Crawl finish. Sleep {sleepT} second. Crawl {len(dataList)} dates.[/yellow]')
        return len(dataList)

    def crawlNew(self, crawlTimes=1, sleepTime=None, level=0) -> int:
        r'''爬取最新评论'''
        levelIndentSize = ' ' * self._indentSize * level
        print(f'{levelIndentSize}[purple]<function crwalNew() In>[/purple]')
        if self.url != self.urlNew:
            self.url = self.urlNew
            self.fromID = ''
        result = self._crawlMain(self.url, crawlTimes, sleepTime, level+1)
        print(f'{levelIndentSize}[cyan]<function crwalNew() Out>[/cyan]')
        return result

    def crawlHot(self, crawlTimes=1, sleepTime=None, level=0) -> int:
        r'''爬取热评'''
        levelIndentSize = ' ' * self._indentSize * level
        print(f'{levelIndentSize}[purple]<function crwalHot() In>[/purple]')
        if self.url != self.urlHot:
            self.url = self.urlHot
            self.fromID = ''
        result = self._crawlMain(self.url, crawlTimes, sleepTime, level+1)
        print(f'{levelIndentSize}[cyan]<function crwalHot() Out>[/cyan]')
        return result
    
    def crawlComment(self, sleepTime=None, level=0) -> None:
        r'''爬取评论的回复'''
        levelIndentSize = ' ' * self._indentSize * level
        print(f'{levelIndentSize}[purple]<function crwalComment() In>[/purple]')
        tempList = []
        for dt in self.data.values():
            if dt['commentCount'] == 0: continue
            dt_id = dt['id']
            levelIndentSize = ' ' * self._indentSize * (level+1)
            print(f'{levelIndentSize}[yellow]爬取 id 为 {dt_id} 评论的回复[/yellow]')
            tempCCN = CrawlCzNeau()
            tempCCN.postID = dt['id']
            temp = 1
            while temp != 0:
                temp = tempCCN._crawlMain(self.urlComment, 1, sleepTime, level+2)
            tempList.append((dt['id'], tempCCN.data.values(), ))
        for commentD in tempList:
            self.data[commentD[0]]['commentList'] = list(commentD[1])
        print(f'{levelIndentSize}[cyan]<function crwalComment() Out>[/cyan]')


## nickname of class
CCN = CrawlCzNeau
