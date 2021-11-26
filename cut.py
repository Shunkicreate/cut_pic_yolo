import os
import cv2


class Cut:
    NUM = 0
    X = 1
    Y = 2
    WIDTH = 3
    HEIGHT = 4

    def __init__(self, separate_x, separate_y, dir_name):
        self.separate_x = separate_x
        self.separate_y = separate_y
        self.dir_name = dir_name

    def get_path(self):
        files = os.listdir(self.dir_name)
        print(files[0][-3:])
        files = [f for f in files if (
            os.path.isfile(os.path.join(self.dir_name, f)))]
        files = [f for f in files if (f[-3:] == 'jpg') or (f[-3:] == 'jpeg')]
        return files

    def cut_yolo(self, file_name):
        file_text = []
        file_name = file_name[:-4]
        with open('{}/{}.txt'.format(self.dir_name,file_name)) as f:
            file_text = f.read().replace('\n', ' ').split(' ')[:-1]
        datas = [[float(file_text[5*j+i]) for i in range(5)]
                 for j in range(int(len(file_text)/5))]

        sum_data = []

        new_datas = {i: [] for i in range(self.separate_x)}
        for i in new_datas:
            new_datas[i] = {j: [] for j in range(self.separate_y)}

        print(new_datas)
        for data in datas:
            data.append(0)
            for i in range(self.separate_x):
                data[-1] = i
                devide_coordinate = (i+1)/self.separate_x
                if(abs(data[self.X]-devide_coordinate) < data[self.WIDTH]/2):
                    # 次もアノテーションを分けれる場合
                    if(abs(data[self.X]-(i+2)/self.separate_x) < data[self.WIDTH]/2 or self.separate_x-i == 1):
                        new_width1 = (data[self.WIDTH]/2-data[self.X] +
                                      devide_coordinate)*self.separate_x
                        new_x1 = 1-new_width1/2
                        app_data1 = [data[self.NUM], new_x1, data[self.Y],
                                     new_width1, data[self.HEIGHT], i]
                        sum_data.append(app_data1)
                    else:
                        new_width1 = (data[self.WIDTH]/2-data[self.X] +
                                      devide_coordinate)*self.separate_x
                        new_width2 = (data[self.WIDTH]/2 + data[self.X] -
                                      devide_coordinate)*self.separate_x
                        new_x1 = 1-new_width1/2
                        new_x2 = new_width2/2
                        app_data1 = [data[self.NUM], new_x1, data[self.Y],
                                     new_width1, data[self.HEIGHT], i]
                        app_data2 = [data[self.NUM], new_x2, data[self.Y],
                                     new_width2, data[self.HEIGHT], i+1]
                        sum_data.append(app_data1)
                        sum_data.append(app_data2)
                else:
                    # for j in range(self.separate_y):
                    #     new_datas[i][j].append(data)
                    if(i/self.separate_x < data[self.X] and data[self.X] < (i+1)/self.separate_x):
                        data[self.X] = (
                            data[self.X]-i/self.separate_x)*self.separate_x
                        data[self.WIDTH] = data[self.WIDTH]*self.separate_x
                        sum_data.append(data)
                        break
        # print(new_datas)
        for data in sum_data:
            data.append(0)
            for i in range(self.separate_y):
                data[-1] = i
                devide_coordinate = (i+1)/self.separate_y
                if(abs(data[self.Y]-devide_coordinate) < data[self.HEIGHT]/2):
                    if(abs(data[self.Y]-(i+2)/self.separate_y) < data[self.HEIGHT]/2 or (self.separate_y-i == 1)):
                        new_height1 = (data[self.HEIGHT]/2-data[self.Y] +
                                       devide_coordinate)*self.separate_y
                        new_y1 = 1-new_height1/2
                        app_data1 = [data[self.NUM], data[self.X],
                                     new_y1, data[self.WIDTH], new_height1]
                        new_datas[data[-2]][i].append(app_data1)
                    else:
                        new_height1 = (data[self.HEIGHT]/2-data[self.Y] +
                                       devide_coordinate)*self.separate_y
                        new_height2 = (data[self.HEIGHT]/2 + data[self.Y] -
                                       devide_coordinate)*self.separate_y
                        new_y1 = 1-new_height1/2
                        new_y2 = new_height2/2
                        app_data1 = [data[self.NUM], data[self.X],
                                     new_y1, data[self.WIDTH], new_height1]
                        app_data2 = [data[self.NUM], data[self.X],
                                     new_y2, data[self.WIDTH], new_height2]
                        new_datas[data[-2]][i].append(app_data1)
                        new_datas[data[-2]][i+1].append(app_data2)
                else:
                    if(i/self.separate_y < data[self.Y] and data[self.Y] < (i+1)/self.separate_y):
                        data[self.Y] = (
                            data[self.Y]-i/self.separate_y)*self.separate_y
                        data[self.HEIGHT] = data[self.HEIGHT]*self.separate_y
                        new_datas[data[-2]][i].append(data[:-2])
                        break
        for i in new_datas:
            for j in new_datas[i]:
                write_data = ''
                with open('{}/separate/{}_x{}_y{}.txt'.format(self.dir_name,file_name, (i), j), mode='w') as f:
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
                    print('{}_x{}_y{}.txt\n'.format(file_name, (i), j), write_data)

        with open('cat/classes.txt', mode='r') as f:
            with open('cat/separate/classes.txt', mode='w') as g:
                text = f.read()
                g.write(text)             
                    

    def cut_pic(self, file_name):
        # 画像の読み込み
        img = cv2.imread(self.dir_name+'/'+file_name, cv2.IMREAD_COLOR)
        h, w = img.shape[:2]
        # 画像の分割処理
        cx = 0
        cy = 0
        for i in range(self.separate_x):
            for j in range(self.separate_y):
                separate_pic = img[cy:cy +
                                   int(h/self.separate_y), cx:cx+int(w/self.separate_x), :]
                cv2.imwrite('{}/separate/{}_x'.format(self.dir_name, file_name[:-4])+str(i) +
                            '_y'+str(j)+'.jpg', separate_pic)
                cy = cy+int(h/self.separate_y)
            cy = 0
            cx = cx+int(w/self.separate_x)
