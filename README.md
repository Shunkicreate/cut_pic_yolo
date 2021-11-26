# cut_pic_yolo

実行するときは下のコマンドを使う．
```
python main.py --separate_x 5 --separate_y 7 --source 'cat'
```
separate_xは横方向(X方向)の分割数．
separate_yは横方向(縦方向)の分割数．
sourceは画像が入っているディレクトリ．なお，ここで示したcatはmain.pyと同じ階層にある．画像が入っているディレクトリとyolo用のテキストデータがが入っているディレクトリは同じにする．分割された画像，テキストデータは指定したディレクトリの中のseparateの中に入る．

