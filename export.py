import sys, re, cgi, urllib, xml.dom.minidom, time
import json
from http.cookiejar import CookieJar
import login_info

def getToken():
    token = False
    html = urllib.request.urlopen("http://www.nicovideo.jp/my/mylist").read().decode('utf-8')
    for line in html.splitlines():
        mo = re.match(r'^\s*NicoAPI\.token = "(?P<token>[\d\w-]+)";\s*',line)
        if mo:
            token = mo.group('token')
            break
    assert token
    return token

def mylist_create(name, is_pubic):
    cmdurl = "http://www.nicovideo.jp/api/mylistgroup/add"
    q = {}
    q['name'] = name.encode("utf8")
    q['description'] = ""
    q['public'] = is_pubic
    q['default_sort'] = 0
    q['icon_id'] = 0
    q['token'] = token
    cmdurl += "?" + urllib.parse.urlencode(q)
    j = json.load(urllib.request.urlopen(cmdurl), encoding='utf8')
    print(name + " " + str(j))
    return j['id']


def get_smids(url):
    smids = []
    html = urllib.request.urlopen(url).read().decode('utf-8')
    for line in html.splitlines():
        mo = re.search(r'data-video-id="(?P<smid>sm\d*)"',line)
        if mo:
            smids.append(mo.group('smid'))
    return smids

def get_playlist_name(url):
    playlist_name = False
    html = urllib.request.urlopen(url).read().decode('utf-8')
    for line in html.splitlines():
        mo = re.search(r'<h1 class="playlist-dtl-title">(?P<name>.*)</h1>',line)
        if mo:
            playlist_name = mo.group('name')
            break
    assert playlist_name
    return playlist_name

def addvideo_tomylist(mid,smids):
    for smid in smids:
        cmdurl = "http://www.nicovideo.jp/api/mylist/add"
        q = {}
        q['group_id'] = mid
        q['item_type'] = 0
        q['item_id'] = smid
        q['description'] = u""
        q['token'] = token
        cmdurl += "?" + urllib.parse.urlencode(q)
        j = json.load(urllib.request.urlopen(cmdurl), encoding='utf8')
        print(smid + " " + str(j))
        time.sleep(0.5)

if __name__ == '__main__':
    #login info
    userid = login_info.userid
    passwd = login_info.passwd

    args = sys.argv
    if len(args) != 2:
        print("invalid arguments")
        exit(-1)
    else:
        playlist_url = args[1]

    #login
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
    urllib.request.install_opener(opener)
    urllib.request.urlopen("https://secure.nicovideo.jp/secure/login",
                urllib.parse.urlencode( {"mail":userid, "password":passwd}).encode('ascii') )
    token = getToken()

    #create and add
    smids = get_smids(playlist_url)
    time.sleep(0.5)
    playlist_name = get_playlist_name(playlist_url)
    mid = mylist_create(playlist_name, 0)
    addvideo_tomylist(mid, smids)

