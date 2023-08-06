# -*- coding: utf-8 -*-
"""
google-ime-skk.py

Google IME SKK Server written in Python
Python 3.6.6, 3.9.10で動作確認済み

  ddskkの仕様
  ▼へんかん と変換をし、キャッシュされている候補を表示しつくした場合はまず辞書サーバを読みにいく
  辞書サーバが使えない場合は、SKK-JISYO.Lなど指定している辞書ファイルを読みにいく

  辞書サーバのプロセスに送る文字列の説明
  辞書サーバ側では、以下の数字が1文字目に入力される場合にレスポンスしなければならない
  0: 辞書サーバを切り離す
  1: 後ろに変換対象文字列が続くので、それを変換した結果を返す
  2: 辞書サーバのバージョンを返す
  3: 辞書サーバのホストアドレスを返す
  4: 辞書サーバに補完リクエスト(server completion)を送る(未対応)

  辞書サーバ側の対応例
  [入力] 0 [出力] 何もしない
  [入力] 1しんそう [出力] 1/真相/深層/新装/神葬/しんそう(半角空白かスラッシュを区切り文字とする)
  [入力] 2 [出力] Google IME SKK written in Python(形式自由)
  [入力] 3 [出力] localhost:127.0.0.1:55100(形式自由)
  [入力] 4 [出力] 何もしない
"""

import os
import argparse
import json
import socket
import urllib.parse
import urllib.request
from socketserver import BaseRequestHandler, ThreadingTCPServer

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, '__version__.py'), mode='r', encoding='utf-8') as f:
    exec(f.read(), about)

VERSION_STRING = about['__title__'] + ' ' + about['__version__']
BUFSIZE = 512


def google_transliterate(text):
    """Send http request to Google CGI API for Japanese Input

    URL: http://www.google.com/transliterate

    引数: "しんそう"
    返り値: "真相/深層/新装/神葬/しんそう"
    """

    query_dict = {
        'langpair': 'ja-Hira|ja',
        'text': text + ','  # 末尾にコンマをつけると勝手に分割されない
    }

    params = urllib.parse.urlencode(query_dict)
    url = 'http://www.google.com/transliterate?' + params

    res = urllib.request.urlopen(url, timeout=5)
    res = res.read().decode().replace("\n", "").replace(",]", "]")

    candidates = '/'.join(json.loads(res)[0][1])

    return candidates


class TCPRequestHandler(BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(BUFSIZE)
            if data:
                data = data.decode('euc-jp')

                end = len(data)
                if ' ' in data:   # 空白文字か改行文字のインデックスを取得
                    end = data.index(' ')
                elif '\n' in data:
                    end = data.index('\n')

                flag = data[0]

                if flag == '1':
                    try:
                        # Google CGI API for Japaneseに投げる
                        candidates = google_transliterate(data[1:end])
                        self.request.sendall(bytes(f'1/{candidates}\n', 'euc-jp'))
                    except Exception as e:
                        print(e)
                        break  # エラーが起きたら接続を閉じる

                elif flag == '2':
                    self.request.sendall(bytes(f'{VERSION_STRING}', 'euc-jp'))

                elif flag == '3':
                    host = socket.gethostname()
                    ip = socket.gethostbyname(host)
                    self.request.sendall(bytes(f'{host}:{ip}', 'euc-jp'))

                else:
                    # 1, 2, 3以外のリクエストが来たら異常なので接続を閉じる
                    break


def start_skk_server(host='127.0.0.1', port=55000, proxy=None):
    """SKK辞書サーバーを立てる"""

    if proxy:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)

    ThreadingTCPServer.allow_reuse_address = True
    with ThreadingTCPServer((host, port), TCPRequestHandler) as server:
        server.serve_forever()


def main():
    """オプション引数を受けとり辞書サーバーを起動"""

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-p', '--port', default=55000, help='Listen port number')
    parser.add_argument('-h', '--host', default='0.0.0.0', help='Listen hostname')
    parser.add_argument('-x', '--proxy', default=None, help='HTTP Proxy Server')
    args = parser.parse_args()

    start_skk_server(args.host, int(args.port), args.proxy)


if __name__ == '__main__':
    main()

"""
Linuxコマンドによるテスト(utf-8のターミナルを想定)
echo "1とあるまじゅつのいんでっくす" | iconv -f UTF-8 -t EUC-JP \
   | nc localhost 55000 | iconv -f EUC-JP -t UTF-8
"""
