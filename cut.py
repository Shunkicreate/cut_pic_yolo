import os
import cv2


class Cut:
    #datasの中のリストの引数の定義
    NUM = 0
    X = 1
    Y = 2
    WIDTH = 3
    HEIGHT = 4

    def __init__(self, separate_x, separate_y, dir_name):
        self.separate_x = separate_x #x方向の分割数
        self.separate_y = separate_y #y方向の分割数
        self.dir_name = dir_name #写真が入っているディレクトリの名前．

    def get_path(self):  # 画像が入っているディレクトリの取得，画像データの取得．
        files = os.listdir(self.dir_name)
        files = [f for f in files if (
            os.path.isfile(os.path.join(self.dir_name, f)))]
        jpg_files = [f for f in files if (f[-3:] == 'jpg') or (f[-3:] == 'jpeg')]
        text_files = [f for f in files if (f[-3:] == 'txt') and (f != 'classes.txt')]
        self.data_num = len(jpg_files)*self.separate_x*self.separate_y
        if(len(jpg_files) != len(text_files)):
            raise Exception('Error. The amount of images and the amount of annotations are different.')

        return jpg_files  # 拡張子付きの画像データのファイル名のリストを返す．

    def cut_yolo(self, file_name):  # yoloファイルの分割関数．
        file_text = []
        file_name = file_name[:-4]
        with open('{}/{}.txt'.format(self.dir_name, file_name)) as f:  # テキストファイルを開いてその中のアノテーション情報を取る．
            file_text = f.read().replace('\n', ' ').split(' ')[:-1]
        datas = [[float(file_text[5*j+i]) for i in range(5)]  # テキストファイル内の情報を保管するリスト．
                 for j in range(int(len(file_text)/5))]

        sum_data = []  # x方向の分割データをy方向に引き継ぐためのリスト．

        # x，y方向どちらにも分割した最終結果を保持する辞書．
        new_datas = {i: [] for i in range(self.separate_x)}
        for i in new_datas:
            new_datas[i] = {j: [] for j in range(self.separate_y)}

        for data in datas:  # x方向のテキストデータの分割
            data.append(0)  # x方向のどの場所(分割箇所)に入るかの情報を格納するための箱
            for i in range(self.separate_x):
                data[-1] = i
                devide_coordinate = (i+1)/self.separate_x
                if(abs(data[self.X]-devide_coordinate) < data[self.WIDTH]/2):  # アノテーションが分割される場合
                    if(abs(data[self.X]-(i+2)/self.separate_x) < data[self.WIDTH]/2 or self.separate_x-i == 1): # 次のブロックでもアノテーションを分割できる場合
                        new_width1 = (data[self.WIDTH]/2-data[self.X] + 
                                      devide_coordinate)*self.separate_x
                        new_x1 = 1-new_width1/2
                        app_data1 = [data[self.NUM], new_x1, data[self.Y],
                                     new_width1, data[self.HEIGHT], i]
                        sum_data.append(app_data1) 
                    else:  # 次のブロックではアノテーションを分割できない場合
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
                else:  # アノテーションが分割されない場合
                    if(i/self.separate_x < data[self.X] and data[self.X] < (i+1)/self.separate_x): # アノテーションが該当ブロックにいる場合，そのブロックの情報を追加．
                        data[self.X] = (
                            data[self.X]-i/self.separate_x)*self.separate_x
                        data[self.WIDTH] = data[self.WIDTH]*self.separate_x
                        sum_data.append(data)
                        break
                    
        for data in sum_data: #y方向のアノテーションの分割．
            data.append(0) # y方向のどの場所(分割箇所)に入るかの情報を格納するための箱
            for i in range(self.separate_y):
                data[-1] = i
                devide_coordinate = (i+1)/self.separate_y
                if(abs(data[self.Y]-devide_coordinate) < data[self.HEIGHT]/2): # アノテーションが分割される場合
                    if(abs(data[self.Y]-(i+2)/self.separate_y) < data[self.HEIGHT]/2 or (self.separate_y-i == 1)): # 次のブロックでもアノテーションを分割できる場合
                        new_height1 = (data[self.HEIGHT]/2-data[self.Y] +
                                       devide_coordinate)*self.separate_y
                        new_y1 = 1-new_height1/2
                        app_data1 = [data[self.NUM], data[self.X],
                                     new_y1, data[self.WIDTH], new_height1]
                        new_datas[data[-2]][i].append(app_data1)
                    else: # 次のブロックではアノテーションを分割できない場合
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
                else: # アノテーションが分割されない場合
                    if(i/self.separate_y < data[self.Y] and data[self.Y] < (i+1)/self.separate_y): # アノテーションが該当ブロックにいる場合，そのブロックの情報を追加．
                        data[self.Y] = (
                            data[self.Y]-i/self.separate_y)*self.separate_y
                        data[self.HEIGHT] = data[self.HEIGHT]*self.separate_y
                        new_datas[data[-2]][i].append(data[:-2])
                        break
        if not(os.path.exists('{}/separate'.format(self.dir_name))):
            os.makedirs('{}/separate'.format(self.dir_name))
        for i in new_datas:
            for j in new_datas[i]:
                write_data = ''
                with open('{}/separate/{}_x{}_y{}.txt'.format(self.dir_name, file_name, (i), j), mode='w') as f:  # 新しいファイルへの情報の書き込み
                    for k in new_datas[i][j]:
                        for l, m in enumerate(k): #データのフォーマット
                            if (l == 0):
                                write_data += str(int(m))+" "
                            else:
                                write_data += str(m)+" "
                        write_data = write_data[:-1]+"\n"
                        if(len(new_datas[i][j]) == 0 and sum(new_datas[i][j]) == 0):
                            write_data = ''

                    f.write(write_data)
                    # print('{}_x{}_y{}.txt\n'.format(
                    #     file_name, (i), j), write_data)

        with open('{}/classes.txt'.format(self.dir_name), mode='r') as f: #アノテーションのクラス情報のコピー
            with open('{}/separate/classes.txt'.format(self.dir_name), mode='w') as g:
                text = f.read()
                g.write(text)

    def cut_pic(self, file_name): #写真を分割するための関数．
        img = cv2.imread(self.dir_name+'/'+file_name, cv2.IMREAD_COLOR) # 画像の読み込み
        h, w = img.shape[:2]
        cx = 0
        cy = 0
        for i in range(self.separate_x): # 画像の分割処理
            for j in range(self.separate_y):
                separate_pic = img[cy:cy +
                                   int(h/self.separate_y), cx:cx+int(w/self.separate_x), :]
                cv2.imwrite('{}/separate/{}_x'.format(self.dir_name, file_name[:-4])+str(i) + #画像の書き込み．
                            '_y'+str(j)+'.jpg', separate_pic)
                cy = cy+int(h/self.separate_y)
            cy = 0
            cx = cx+int(w/self.separate_x)
