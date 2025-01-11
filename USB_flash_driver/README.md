# USB flash drive	

## sleuthkitを使って解く
TSK, The Sleuth Kitなどとも呼ばれるらしい。
GUI版で使えるようになっているのがAutopsyというらしい。

### ツールの用途
イメージファイル、ファイルシステム周りの調査、デジタルフォレンジックスなどを行う時に利用する。


### インストール
kali linuxコンテナ上で
```
# dockerコンテナの生成
$ docker pull kalilinux/kali-rolling
# 起動したコンテナ内にログイン
# カレントディレクトリをマウントしてdockerコンテナを起動する
$ docker run -itd -v $(pwd):/home --rm kalilinux/kali-rolling
# ログイン
$ docker exec -it $CONTAINER_ID bash



$ apt update
$ apt install sleuthkit -y
```

### イメージファイル内の情報を確認する

- 2つ目の要素がファイルのinodeらしい。
- `-/r` の後に`*`がついているものは、削除されているファイルという意味らしい。
```
┌──(root㉿59d7c9529875)-[/home]
└─# fls drive.img
r/r 4-128-4:	$AttrDef
r/r 8-128-2:	$BadClus
r/r 8-128-1:	$BadClus:$Bad
r/r 6-128-4:	$Bitmap
r/r 7-128-1:	$Boot
d/d 11-144-4:	$Extend
r/r 2-128-1:	$LogFile
r/r 0-128-1:	$MFT
r/r 1-128-1:	$MFTMirr
r/r 9-128-8:	$Secure:$SDS
r/r 9-144-11:	$Secure:$SDH
r/r 9-144-5:	$Secure:$SII
r/r 10-128-1:	$UpCase
r/r 3-128-3:	$Volume
r/r 35-128-1:	Carl Larsson Brita as Iduna.jpg
r/r 37-128-1:	Mona Lisa.jpg
r/r 38-128-1:	The Great Wave off Kanagawa.jpg
-/r * 36-128-1:	Liberty Leading the People.jpg
-/r * 36-128-4:	Liberty Leading the People.jpg:00
-/r * 36-128-5:	Liberty Leading the People.jpg:01
-/r * 36-128-6:	Liberty Leading the People.jpg:02
-/r * 36-128-7:	Liberty Leading the People.jpg:03
-/r * 36-128-8:	Liberty Leading the People.jpg:04
-/r * 36-128-9:	Liberty Leading the People.jpg:05
-/r * 36-128-10:	Liberty Leading the People.jpg:06
V/V 256:	$OrphanFiles
```

### inodeを指定して、イメージファイル内のファイルを表示する

```
┌──(root㉿59d7c9529875)-[/home]
└─#  icat drive.img 36-128-4
FLA
┌──(root㉿59d7c9529875)-[/home]
└─#  icat drive.img 36-128-5
G_q
┌──(root㉿59d7c9529875)-[/home]
└─# icat drive.img 36-128-6
azy
┌──(root㉿59d7c9529875)-[/home]
└─# icat drive.img 36-128-7
etF
┌──(root㉿59d7c9529875)-[/home]
└─# icat drive.img 36-128-7
etF
┌──(root㉿59d7c9529875)-[/home]
└─# icat drive.img 36-128-8
6ic
┌──(root㉿59d7c9529875)-[/home]
└─# icat drive.img 36-128-9
oWC
┌──(root㉿59d7c9529875)-[/home]
└─# icat drive.img 36-128-10
vjN
```

## このツールは何のために
デジタルフォレンジックスを行う時などに使う。
