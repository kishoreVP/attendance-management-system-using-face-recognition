import mysql.connector
import pickle
import face_recognition
import cv2
import os

my_con = mysql.connector.connect(host='localhost', user='root', passwd='tiger', database='attendance')
cursor = my_con.cursor()

path = input('enter the folder path or press enter for default folder')
if not (path):
    path = 'images'


def encoder(images, class_info):
    encode_list = []
    file = open('class12_encode.dat', 'ab')
    for img, i in zip(images, range(len(images))):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        encode = face_recognition.face_encodings(img)[0]

        encode_list.append(encode)
        name_ = (class_info[i])
        name_, rolno, adno = name_.split(',')

        data = [adno, encode, name_, img]
        try:
            cursor.execute(f"insert into class12(adm_no,roll_no,name) values({adno},{rolno},'{name_}');")
            pickle.dump(data, file)
        except:  # need to handle if name already exist
            print(f'{adno} already exists ')
    file.close()

    return encode_list


def folder_encoder(path='images'):
    '''
    :param path: enter the folder name if in same director,if not enter the path of the folder
    :return:list of encoding values,list of images,class names
    '''

    images = []  # image path
    class_info = []  # name
    class_names = []
    try:
        ls_dir = os.listdir(path)
    except:
        print('enter a correct path')
        return 1
    for cl in ls_dir:
        cur_img = cv2.imread(f'{path}/{cl}')
        images.append(cur_img)
        filename = (os.path.splitext(cl)[0]).upper()
        class_info.append(filename)
        class_names.append(((filename.split(',')[0]).upper()))

    print('encoding complete')
    return encoder(images, class_info)

folder_encoder(path)
my_con.commit()
my_con.close()
