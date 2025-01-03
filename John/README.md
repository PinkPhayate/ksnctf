# memo
Johnというパスワードクラッキングツールを使えば、すぐに答えにたどり着きそうではあるが、python スクリプトで同じことをできないか、確認してみた。

ついに答えを見つけたかもしれん
https://blog.amedama.jp/entry/unix-crypt-3

## 問題文について
- 問題文のファイルは、`/etc/passwd`ではなく、パスワードが書かれている`/etc/shadow`
- ファイルについて調べると、パスワードがハッシュ化されている2つ目の要素には、文法が決まっている。
  - `$6$`始まりのものはSHA512で暗号化されている、という意味らしい。
https://www.unknownengineer.net/entry/2017/08/16/184537


## opensslコマンドで実行
```
% openssl passwd -6 -salt=rXw/Kruy password
$6$rXw/Kruy$fknmFoVk3U4fO6j8zk7qVlx0VJHADoC/oGGGQhb77iihwy9FQtB4hbGfLhwmEV/XwZnbT5PZufhXkIF1Oocv0.
```
## pythonで実行
```
% python -c "from passlib.hash import sha512_crypt; print(sha512_crypt.hash('password', rounds=5000, salt='rXw/Kruy'))"
$6$rXw/Kruy$fknmFoVk3U4fO6j8zk7qVlx0VJHADoC/oGGGQhb77iihwy9FQtB4hbGfLhwmEV/XwZnbT5PZufhXkIF1Oocv0.
```
## デフォルトで含まれているハッシュ化モジュールでは、ハッシュ値のフォーマットが一致しない
さらにsaltを別の値に変えても、出力される値が一致することが判明。
--> pythonモジュールで使用するハッシュ化関数が古いもの or ハッシュ化に利用する関数を変えないと問題が解けなそうと推測。
```
(john) [hayatetanaka@Hayates-MacBook-Air] ~/Develop/ksnctf/John
% python -c "import crypt; print(crypt.crypt('password','\$6\$rXw/Kruy\$'))"
$6FMi11BJFsAc
(john) [hayatetanaka@Hayates-MacBook-Air] ~/Develop/ksnctf/John
% python -c "import crypt; print(crypt.crypt('password','\$1\$rXw/Kruy\$'))"
$1d2n7Q0.r54s
(john) [hayatetanaka@Hayates-MacBook-Air] ~/Develop/ksnctf/John
% python -c "import crypt; print(crypt.crypt('password','\$6\$aaaaaaaa\$'))"
$6FMi11BJFsAc

```
[hayatetanaka@Hayates-MacBook-Air] ~/Develop/ksnctf/John
% python -c "import crypt; print(crypt.crypt('password','\$6\$rXw/Kruy\$'))"
$6FMi11BJFsAc
[hayatetanaka@Hayates-MacBook-Air] ~/Develop/ksnctf/John
% python -c "import crypt; print(crypt.crypt('password','$6$rXw/Kruy$'))"
/KmmrL8n7ELxw

別のライブラリを入れたら一致した。
% python -c "from passlib.hash import sha512_crypt; print(sha512_crypt.hash('password', rounds=5000, salt='rXw/Kruy'))"
$6$rXw/Kruy$fknmFoVk3U4fO6j8zk7qVlx0VJHADoC/oGGGQhb77iihwy9FQtB4hbGfLhwmEV/XwZnbT5PZufhXkIF1Oocv0.



