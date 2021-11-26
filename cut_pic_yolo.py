from cut import Cut

separate_x = 4  # 横方向の分割数
separate_y = 3  # 縦方向の分割数
dir_name = "cat"  # 画像が入っているディレクトリ


cut = Cut(separate_x=separate_x, separate_y=separate_y, dir_name=dir_name)
file_names = cut.get_path()
for file_name in file_names:
    cut.cut_yolo(file_name = file_name)
    cut.cut_pic(file_name = file_name)
