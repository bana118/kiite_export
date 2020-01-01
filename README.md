# kiite_export
kiiteのプレイリストをニコニコ動画のマイリストにコピーするプログラムです。kiiteで作成したマイリストを[nicobox](https://site.nicovideo.jp/nicobox/lp/index.html)アプリを用いてスマートフォンで再生できます。

## 使用方法
1. login_info.py.exampleを以下のように自身のniconicoアカウントのメールアドレス、パスワードに書き換える  
```
email = "youremail@example.com"
passwd = "yourpassword"
```  
  
2. login_info.py.exampleをlogin_info.pyへリネーム  

3. pythonでexport.pyをkiiteのプレイリストのurlを引数に入れて実行

```
> python export.py playlist_url
```

## 注意点
- ニコニコ動画の上限(一般: 100, プレミアム: 25000)を越えてマイリストに曲は追加できないです。
- pythonのバージョンは3.7.4で動作確認しました。
