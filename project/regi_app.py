import sys
import sqlite3
import webbrowser  
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon  


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("/Projects/python/minipro/Design/register.ui", self)

        self.Background_Page()
        self.setFixedSize(985, 605)  
        self.setWindowTitle("Register")  
        self.setWindowIcon(QIcon("/Projects/python/minipro/Design/img/icon.png"))  

        # ตั้งค่าช่องข้อความสำหรับ Password ให้ซ่อนข้อความ
        self.password.setEchoMode(QLineEdit.Password)
        self.confirm.setEchoMode(QLineEdit.Password)

        # เชื่อมปุ่มกับฟังก์ชัน
        self.submit.clicked.connect(self.Create_User)  
        self.face_Button.clicked.connect(self.Open_Face)  
        self.gmail_Button.clicked.connect(self.Open_Gmail)  

        # สร้างตาราง ถ้ายังไม่มี
        self.create_Table()


    # สร้างตาราง (อย่าปิด self.conn ที่นี่)
    def create_Table(self):
        conn = sqlite3.connect("/Projects/python/minipro/projects.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS register (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                user_name TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                confirm_pass TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()  
        print("สร้างตารางแล้ว")


    # เพิ่มข้อมูลลงฐานข้อมูล (แก้ไขการใช้ SQL)
    def Create_User(self):
        First_name = self.fname.text()
        Last_name = self.lname.text()
        User_name = self.user.text()
        Email_name = self.email.text()
        Password = self.password.text()
        Confi_pass = self.confirm.text()

        # ตรวจสอบว่า check box ถูกติ๊กหรือไม่
        if not self.terms_checkBox.isChecked():
            QMessageBox.warning(self, 'ข้อผิดพลาด', 'กรุณายอมรับเงื่อนไขและข้อตกลงก่อนสมัครสมาชิก')
            return
        
        
       
        if First_name and Last_name and User_name and Email_name and Password and Confi_pass:
            # ตรวจสอบข้อมูลอื่น ๆ ว่าถูกต้องหรือไม่
            if Password != Confi_pass:
                QMessageBox.warning(self, 'ข้อผิดพลาด', 'รหัสผ่านไม่ตรงกัน')
                return
            
            try:
                # ใช้ parameterized query
                conn = sqlite3.connect("/Projects/python/minipro/projects.db")
                cursor = conn.cursor()

                query = '''INSERT INTO register (first_name, last_name, user_name, email, password, confirm_pass) 
                           VALUES (?, ?, ?, ?, ?, ?)'''
                cursor.execute(query, (First_name, Last_name, User_name, Email_name, Password, Confi_pass))

                conn.commit()
                conn.close()

                QMessageBox.information(self, 'สำเร็จ', 'สมัครสมาชิกเรียบร้อยแล้ว')
                self.Link_Main_App()  # ไปที่หน้าหลัก

                

            except sqlite3.IntegrityError:
                QMessageBox.warning(self, 'ข้อผิดพลาด', 'มีผู้ใช้นี้แล้วในระบบ')
                self.Clear_Data()
        else:
            QMessageBox.warning(self, 'ข้อผิดพลาด', 'กรุณากรอกข้อมูลให้ครบถ้วน')


    # ล้างข้อมูลหลังจากเพิ่มข้อมูลเสร็จ
    def Clear_Data(self):
        self.fname.clear()
        self.lname.clear()
        self.user.clear()
        self.email.clear()
        self.password.clear()
        self.confirm.clear()


    # เปิด Facebook
    def Open_Face(self):
        url = "https://www.facebook.com"
        QDesktopServices.openUrl(QUrl(url))  

    # เปิด Gmail
    def Open_Gmail(self):
        url = "https://www.gmail.com"
        QDesktopServices.openUrl(QUrl(url))  


    # ตั้งค่า Background Image
    def Background_Page(self):
        self.setStyleSheet("""
            QMainWindow {
                background-image: url("/Projects/python/minipro/Design/img/spoo.jpg");
                background-repeat: no-repeat;
                background-position: left;
                background-size: cover;
            }
        """)

    #function link ไปที่ main_app
    def Link_Main_App(self):
        from main_app import MymainApp # import class main
        self.main_window = MymainApp()  # เรียกคลาส main
        self.main_window.show()
        self.close()  # ปิดหน้าล็อกอิน 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
