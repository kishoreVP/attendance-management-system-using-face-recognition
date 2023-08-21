import mysql.connector
import datetime
import attendance
import attendance as atd
from prettytable import PrettyTable
print('\n ATTENDANCE SYSTEM INITIATED')
cont = True

#############################################      :)   MAIN MENU   (:      #######################################################################################
my_con = mysql.connector.connect(host='localhost', user='root', passwd='tiger', database='attendance')
cursor = my_con.cursor()
today=str(datetime.date.today()).replace('-', '_')
while cont:

    print('\n MENU \n')
    print('1.START ATTENDANCE')
    print('2.ADD PEOPLE')
    print('3.MANIPULATE DATABASE')
    print("4.QUIT")
############################################       :)  ENTERING THE CHOICE     (:             #############################################################
    choice = input('\n ENTER THE CHOICE:::: ')
    if choice == '1':
        atd.take_attendace()
    elif choice == '2':
        print('1.BULK INSERTION USING A FOLDER CONTAINING IMAGES')
        print('2.SINGLE PERSON USING CAMERA OPTIONS')
        print('3.BACK TO MAIN MENU')
        choi = input()
        if choi == '1':
            print(
                '\n NOTE:enter the path of the folder containing images,with names in the format =>name,class(ex 10A),roll_number,admission number')
            print('(with no space)')
            exec(open('DB_sql.py').read())
        elif choi == '2':
            attendance.take_photo_enocode()
        elif choi==3:
            break
    elif choice == '3':
            print("1.LIST OF ABSENTEES")
            print("2.MANUALLY UPDATE ATTENDANCE")
            print("3.BACK TO MAIN MENU")
            ch2=int(input("\n ENTER YOUR CHOICE:"))

            if ch2 == 1:
                
                
                col_name = ['adm_no','roll_no','name']
                mytable = PrettyTable(col_name)
                cursor.execute(f"select adm_no,roll_no,name from class12 where {today} = 'A';")
                
                lst_abs = cursor.fetchone()
                while lst_abs != None:
                    mytable.add_row(lst_abs)
                    lst_abs = cursor.fetchone()           
                    
                print(mytable)
                
            elif ch2 == 2:
                adm_id = 'adminnumber'
                usr_adm = input('ENTER ADMIN CODE::')
                if usr_adm == adm_id:
                    while True:
                        adm_no = input("ENTER THE ADMISSION NUMBER OF STUDENT")
                        state = input(f"ENTER THE STATE OF {adm_no} (A\P\AP\PA):::")
                        try:
                            cursor.execute(f"update class12 set {today}='{state}' where adm_no={adm_no};")
                            cursor.commit()
                            n=input("DO YOU WANT TO ADD MORE (y/n)::")
                            if n.lower() == 'n':
                                break

                        except:
                            print("ENTER CORRECT DETAILS")

                else:
                    print("\n WRONG ID")

                
            elif ch2 == 3:
                pass
            else:
                print("\nENTER THE CORRECT CHOICE ")        
        
    elif choice == '4':
        cont = False
    else:
        print('\n ERROR ! ENTER THE CORRECT CHOICE $$$')
  
