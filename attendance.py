# importing the necessary modules
import pickle
import cv2
import numpy as np
import face_recognition
import mysql.connector
import datetime


def col_add():
    my_con1 = mysql.connector.connect(host='localhost', user='root', passwd='tiger', database='attendance')
    cursor = my_con1.cursor()
    date1 = (str(datetime.date.today())).replace('-', '_')
    command = f'alter table class12 add {date1} char(4);'
    try:
        cursor.execute(command)
    except:  # expect duplicate coulmn error
        pass


def take_attendace():
    my_con = mysql.connector.connect(host='localhost', user='root', passwd='tiger', database='attendance')

    cursor = my_con.cursor()

    date = str(datetime.date.today()).replace('-', '_')
    col_add()

    encodelistknown = []
    class_names = []
    try:
        with open('class12_encode.dat', 'rb') as f:
            try:
                while True:
                    data = pickle.load(f)
                    encodelistknown.append(data[1])
                    class_names.append(data[2])
            except:
                pass
    except:
        print('no encodings found')
        return 1

    cap = cv2.VideoCapture(0)
    state = 'P'
    done_names = []
    while True:  # key != 27 escape key
        success, img = cap.read()

        imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
        faces_cur_frame = face_recognition.face_locations(imgs)
        encodes_current_frame = face_recognition.face_encodings(imgs, faces_cur_frame)

        for encodeface, faceloc in zip(encodes_current_frame, faces_cur_frame):
            matches = face_recognition.compare_faces(encodelistknown, encodeface)
            facedis = face_recognition.face_distance(encodelistknown, encodeface)

            # print(facedis)
            matchindex = np.argmin(facedis)
            if matches[matchindex]:
                name = class_names[matchindex]
                # print(name)
                if name not in done_names:
                    if datetime.datetime.now().time() < datetime.time(11):
                        state = 'P'
                    else:
                        state = 'AP'  # -> absent-present

                    cursor.execute(f"update class12 set {date} ='{state}' where name = '{name}';")
                    done_names.append(matches[matchindex])

                # setting up the box around the face
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('webcam', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cursor.execute(f"update class12 set {date} ='A' where {date} is null;")
    cap.release()
    cv2.destroyAllWindows()
    my_con.commit()
    my_con.close()


def take_photo_enocode():
    my_con = mysql.connector.connect(host='localhost', user='root', passwd='tiger', database='attendance')
    cursor = my_con.cursor()
    name_ = input('enter the name of the student')
    adno = input('enter admission number')
    rolno = input('enter the roll number')
    print('camera starting up')
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        if not success:
            print('failed to access the camera')
            break
        cv2.imshow('Press space bar to take photo', img)
        k = cv2.waitKey(1)
        if k % 256 == 27:  # ->escape is pressed
            break
        elif k % 256 == 32:  # ->space bar is pressed
            img1 = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            face_cur_frame = face_recognition.face_locations(img1)
            encode = face_recognition.face_encodings(img1, face_cur_frame)[0]
            file = open('class12_encode.dat', 'ab')
            data = [adno, encode, name_, img]
            try:
                pickle.dump(data, file)
                cursor.execute(f"insert into class12(adm_no,roll_no,name) values({adno},{rolno},'{name_}');")
                print('encoding complete')
                break
            except:  # need to handle if name already exist
                print(f'{adno} already exists ')
                break
            file.close()
    my_con.commit()
    my_con.close()
    cap.release()
    cv2.destroyAllWindows()

def show_attendace():
    pass
