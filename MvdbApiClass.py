import requests
import json
import sys

if __name__=='__main__':
    import MvdbApiClass
    help(MvdbApiClass)

class MvdbApi():
    api_host = "https://api.themoviedb.org/3/"
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = '.'
    special_vars = json.load(open("%s/login/MvdbLoginInfo.txt" % base_path))
    api_key = special_vars['apikey']
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

    def SearchMovies(self,string,year=""):
        self.errmsg = ""
        url = "search/movie"
        full_url = self.api_host + url
        params = {
                'api_key': self.api_key,
                'query' : string}
        if year:
            params['year'] = year
        r = requests.get(url=full_url, params=params, headers=self.headers)
        if r.status_code != 200:
            self.errmsg = "Bad response code"
            return False
        r_json = r.json()
        return r_json

    def GetGenres(self):
        self.errmsg = ""
        url = "genre/movie/list"
        full_url = self.api_host + url
        params = {
                'api_key': self.api_key}

        r = requests.get(url=full_url, params=params, headers=self.headers)
        if r.status_code != 200:
            self.errmsg = "Bad response code"
            return False
        r_json = r.json()
        genre_dict = {}
        genres = r_json['genres']
        for genre in genres:
            genre_dict[genre['name']] = genre['id']
        return genre_dict