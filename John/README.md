# memo
Johnというパスワードクラッキングツールを使えば答えにたどり着きそうではあるが、python スクリプトで同じことをできないか、確認してみた。


## 問題文について
- 問題文のファイルは、`/etc/passwd`ではなく、パスワードが書かれている`/etc/shadow`
- ファイルについて調べると、パスワードがハッシュ化されている2つ目の要素には、文法が決まっている。
  - `$6$`始まりのものはSHA512で暗号化されている、という意味らしい。
  - このフォーマットのことを、「Modular Crypt Format」といい、ハッシュ化に使った暗号化アルゴリズムやソルト、ハッシュ値などをまとめて1箇所にまとめられる方法。
  - Linuxのパスワードを保持するファイル(`/etc/shadow`)ではよく見るフォーマットである。


### 参考
- https://www.unknownengineer.net/entry/2017/08/16/184537
- https://blog.amedama.jp/entry/unix-crypt-3

## MacOS上のpythonモジュールがModular Crypt Formatに対応していない件
デフォルトで利用できる、crypt やhashlibのpythonモジュールで出力されるハッシュ値はlinuxのパスワードを解析するのに適していないことがわかった。  
正確にいうと、デフォルトのモジュールが使うハッシュ化関数(`crypt(3)`)がこのフォーマットに対応していない模様。

```
$ python -c "import crypt; print(crypt.crypt('password','\$6\$rXw/Kruy\$'))"
$6FMi11BJFsAc

# マニュアルにはソルトの先頭2文字しか使っていないと書いてあり、ソルトが異なるのにハッシュ値が一致してしまうことを確認。
$ python -c "import crypt; print(crypt.crypt('password','\$6\$aaaaaaaa\$'))"
$6FMi11BJFsAc

# マニュアル確認コマンド
$ man 3 crypt

$ python -c "import crypt; print(crypt.crypt('password','\$1\$rXw/Kruy\$'))"
$1d2n7Q0.r54s

```

そのため、別のモジュールをインストールする必要があった。
```
$ python -c "from passlib.hash import sha512_crypt; print(sha512_crypt.hash('password', rounds=5000, salt='rXw/Kruy'))"
$6$rXw/Kruy$fknmFoVk3U4fO6j8zk7qVlx0VJHADoC/oGGGQhb77iihwy9FQtB4hbGfLhwmEV/XwZnbT5PZufhXkIF1Oocv0.
```

## 補足: MacOSはuserのパスワードをどう管理しているか
1つのファイルにまとまっているのではなくユーザごとにplistファイルが作られていた。  
`/var/db/dslocal/nodes/Default/users/$USER.plist`

### ファイルの内容はsudoで確認できる
`ShadowHashData`という項目の中にパスワードのハッシュ値が書いてありそうで、ハッシュ値からパスワードを推測した例もあった。  
https://embracethered.com/blog/posts/2022/grabbing-and-cracking-macos-hashes/
```
% sudo plutil -p /var/db/dslocal/nodes/Default/users/$USER.plist
```