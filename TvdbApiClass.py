import requests
import json
import sys
if __name__=='__main__':
    import TvdbApiClass
    help(TvdbApiClass)

class TvdbApi():
    api_host = "https://api.thetvdb.com/"
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = '.'
    special_vars = json.load(open("%s/login/TvdbLoginInfo.txt" % base_path))
    api_key = special_vars['apikey']
    user_key = special_vars['userkey']
    user_name = special_vars['username']
    headers = {'Content-type': 'application/json'}

    def __init__(self,debug=False):
        if debug:
            print("DBG> api_host = %s" % self.api_host)
            print("DBG> api_key = %s" % self.api_key)
            print("DBG> user_key = %s" % self.user_key)
            print("DBG> user_name = %s" % self.user_name)
            print("DBG> headers = %s" % self.headers)
    def Close(self):
        return True

    def Login(self,debug=False):
        self.errmsg = ""
        url = "login"
        full_url = self.api_host + url
        data = {
                'apikey': self.api_key,
                'userkey': self.user_key,
                'username': self.user_name}
        payload = json.dumps(data)
        try:
            r = requests.post(url=full_url, data=payload, headers=self.headers, timeout=2)
        except:
            self.errmsg = "Could not connect in 2 seconds"
            return False
        if r.status_code != 200:
            self.errmsg = "Bad response code"
            return False
        r_json = r.json()
        self.token = r_json['token']
        self.headers['Authorization'] = "Bearer %s" % self.token
        return True

    def Refresh(self,debug=False):
        self.errmsg = ""
        url = "refresh_token"
        full_url = self.api_host + url
        if debug:
            print(self.headers)
        r = requests.get(url=full_url, headers=self.headers)
        if debug:
            print(r.text)
            print(r.status_code)
        if r.status_code != 200:
            self.errmsg = "Bad response code"
            return False
        r_json = r.json()
        self.token = r_json['token']
        self.headers['Authorization'] = "Bearer %s" % self.token
        return True

    def SearchSeries(self,name,debug=False):
        self.errmsg = ""
        url = "search/series"
        full_url = self.api_host + url
        params = {'name': name}
        r = requests.get(url=full_url, params=params, headers=self.headers)
        if r.status_code != 200:
            self.errmsg = "Bad response code"
            return False
        r_json = r.json()
        return r_json

    def GetEpisodes(self,show_id,debug=False):
        self.errmsg = ""
        url = "series/%s/episodes" % show_id
        full_url = self.api_host + url
        r = requests.get(url=full_url, headers=self.headers)
        if r.status_code != 200:
            self.errmsg = "Bad response code"
            return False
        r_json = r.json()
        return r_json

    def SearchEpisodes(self,show_id,season_num,episode_num,debug=False):
        self.errmsg = ""
        url = "series/%s/episodes/query" % show_id
        full_url = self.api_host + url
        params = {'airedSeason': season_num,
                  'airedEpisode': episode_num}
        r = requests.get(url=full_url, params=params, headers=self.headers)
        if r.status_code != 200:
            self.errmsg = "Bad response code"
            return False
        r_json = r.json()
        return r_json









