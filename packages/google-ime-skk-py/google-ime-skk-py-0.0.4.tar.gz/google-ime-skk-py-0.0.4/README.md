# google-ime-skk-py

Google IME SKK Server written in Python


## インストール

```
$ pip install google-ime-skk-py
```

## 実行

```
$ google-ime-skk-py
```

## オプション

```
 -p, --port 55000                             Listen port number
 -h, --host "0.0.0.0"                         Listen hostname
 -x, --proxy "http://proxy.example.com:8080"  HTTP Proxy Server
```

## Emacsにおけるddskkの設定
`init.el`等に以下を追加

```lisp
;; 辞書サーバが起動していなければ起動する
(setq skk-server-inhibit-startup-server nil)

;; 辞書サーバの起動コマンド(適宜変更)
(setq skk-server-prog "/path/to/google-ime-skk-py")

;; 辞書サーバのポート番号
(setq skk-server-portnum 55000)

;; Proxy(必要な場合)
(setenv "http_proxy" "http://proxy.example.com:8080")
```

## 参考ページ
### RubyによるGoogle IME SKK辞書サーバー
https://github.com/hitode909/google-ime-skk

### ddskk/skk-server.el
https://github.com/skk-dev/ddskk/blob/master/skk-server.el

## Copyright
Copyright (c) 2022 chaploud. See LICENSE.txt for further details.
