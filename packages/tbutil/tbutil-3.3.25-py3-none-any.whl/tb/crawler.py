class Crawler():
    def __init__(self,headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }):
        self.urllib=__import__('urllib')
        self.headers=headers
    def __call__(self,url):
        return self.urllib.request.urlopen(self.urllib.request.Request(url,headers=self.headers)).read().decode('utf-8')
if __name__=='__main__':
    print(Crawler()('http://192.168.1.50'))
