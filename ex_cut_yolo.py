from os import write



file_text = []
separate_x = 4  # 横方向の分割数
separate_y = 3  # 縦方向の分割数

# 定数の定義
NUM = 0
X = 1
Y = 2
WIDTH = 3
HEIGHT = 4
filename = 'cat'


with open('cat/{}.txt'.format(filename)) as f:
    file_text = f.read().replace('\n', ' ').split(' ')[:-1]
datas = [[float(file_text[5*j+i]) for i in range(5)]
         for j in range(int(len(file_text)/5))]

sum_data = []

new_datas = {i: [] for i in range(separate_x)}
for i in new_datas:
    new_datas[i] = {j: [] for j in range(separate_y)}

print(new_datas)
for data in datas:
    data.append(0)
    for i in range(separate_x):
        data[-1] = i
        devide_coordinate = (i+1)/separate_x
        if(abs(data[X]-devide_coordinate) < data[WIDTH]/2):
            if(abs(data[X]-(i+2)/separate_x) < data[WIDTH]/2 or separate_x-i==1):  # 次もアノテーションを分けれる場合
                new_width1 = (data[WIDTH]/2-data[X] +
                              devide_coordinate)*separate_x
                new_x1 = 1-new_width1/2
                app_data1 = [data[NUM], new_x1, data[Y],
                             new_width1, data[HEIGHT], i]
                sum_data.append(app_data1)
            else:
                new_width1 = (data[WIDTH]/2-data[X] +
                              devide_coordinate)*separate_x
                new_width2 = (data[WIDTH]/2 + data[X] -
                              devide_coordinate)*separate_x
                new_x1 = 1-new_width1/2
                new_x2 = new_width2/2
                app_data1 = [data[NUM], new_x1, data[Y],
                             new_width1, data[HEIGHT], i]
                app_data2 = [data[NUM], new_x2, data[Y],
                             new_width2, data[HEIGHT], i+1]
                sum_data.append(app_data1)
                sum_data.append(app_data2)
        else:
            # for j in range(separate_y):
            #     new_datas[i][j].append(data)
            if(i/separate_x < data[X] and data[X] < (i+1)/separate_x):
                data[X] = (data[X]-i/separate_x)*separate_x
                data[WIDTH] = data[WIDTH]*separate_x
                sum_data.append(data)
                break
# print(new_datas)
for data in sum_data:
    data.append(0)
    for i in range(separate_y):
        data[-1] = i
        devide_coordinate = (i+1)/separate_y
        if(abs(data[Y]-devide_coordinate) < data[HEIGHT]/2):
            if(abs(data[Y]-(i+2)/separate_y) < data[HEIGHT]/2 or (separate_y-i==1)):
                new_height1 = (data[HEIGHT]/2-data[Y] +
                               devide_coordinate)*separate_y
                new_y1 = 1-new_height1/2
                app_data1 = [data[NUM], data[X],
                             new_y1, data[WIDTH], new_height1]
                new_datas[data[-2]][i].append(app_data1)
            else:
                new_height1 = (data[HEIGHT]/2-data[Y] +
                               devide_coordinate)*separate_y
                new_height2 = (data[HEIGHT]/2 + data[Y] -
                               devide_coordinate)*separate_y
                new_y1 = 1-new_height1/2
                new_y2 = new_height2/2
                app_data1 = [data[NUM], data[X],
                             new_y1, data[WIDTH], new_height1]
                app_data2 = [data[NUM], data[X],
                             new_y2, data[WIDTH], new_height2]
                new_datas[data[-2]][i].append(app_data1)
                new_datas[data[-2]][i+1].append(app_data2)
        else:
            if(i/separate_y < data[Y] and data[Y] < (i+1)/separate_y):
                data[Y] = (data[Y]-i/separate_y)*separate_y
                data[HEIGHT] = data[HEIGHT]*separate_y
                new_datas[data[-2]][i].append(data[:-2])
                break
print(new_datas)
for i in new_datas:
    for j in new_datas[i]:
        write_data = ''
        with open('cat/separate/{}_x{}_y{}.txt'.format(filename, (i), j), mode='w') as f:
            for k in new_datas[i][j]:
                for l, m in enumerate(k):
                    if (l == 0):
                        write_data += str(int(m))+" "
                    else:
                        write_data += str(m)+" "
                write_data = write_data[:-1]+"\n"
                if(len(new_datas[i][j]) == 0 and sum(new_datas[i][j]) == 0):
                    write_data = ''

            f.write(write_data)
            print('{}_x{}_y{}.txt\n'.format(filename, (i), j), write_data)

with open('cat/classes.txt', mode='r') as f:
    with open('cat/separate/classes.txt', mode='w') as g:
        text = f.read()
        g.write(text)
