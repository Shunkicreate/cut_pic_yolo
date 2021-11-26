from cut import Cut
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--separate_x", type=int,
                    help="the number of seeparation you want to esparate a jpg file in x direction")
parser.add_argument("--separate_y", type=int,
                    help="the number of seeparation you want to esparate a jpg file in y direction")
parser.add_argument("--source", type=str,
                    help="Name of the directory containing the photos")
args = parser.parse_args()

separate_x = 4  # 横方向の分割数
separate_y = 3  # 縦方向の分割数
dir_name = "cat"  # 画像が入っているディレクトリ

# bugfix: replace == with >=
if args.separate_x:
    separate_x = args.separate_x
    print(separate_x)
if args.separate_y:
    separate_y = args.separate_y
    print(separate_y)
if args.source:
    dir_name = args.source
    print(dir_name)
    


cut = Cut(separate_x=separate_x, separate_y=separate_y, dir_name=dir_name)
file_names = cut.get_path()
for file_name in file_names:
    cut.cut_yolo(file_name = file_name)
    cut.cut_pic(file_name = file_name)
