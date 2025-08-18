import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QLineEdit
from PyQt5 import uic
from regi_app import MyApp # Import ไฟล์สมัครสมาชิก
from PyQt5.QtGui import QIcon  # Import สำหรับไอคอน
import subprocess  # ใช้เปิดไฟล์ Python อื่น





class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/Projects/python/minipro/Design/login.ui', self)  # เชื่อม ui

        #เรียกใช้background
        self.Background_Page_Login()
        # ล็อกหน้าต่างให้มีขนาด width - height 
        self.setFixedSize(871, 739) 
        # ตั้งชื่อTitle
        self.setWindowTitle("Login") 
        # ตั้งค่าไอคอน Title Bar
        self.setWindowIcon(QIcon("/Projects/python/minipro/Design/img/icon.png"))  

        # ตั้งค่าช่องข้อความสำหรับ Password ให้ซ่อนข้อความ
        self.passw.setEchoMode(QLineEdit.Password)

        # เชื่อมปุ่มกับฟังก์ชัน
        self.submit_Button.clicked.connect(self.Login_Data)
        self.sign.clicked.connect(self.Link_Regi)


        # เชื่อมต่อฐานข้อมูล
        self.conn = sqlite3.connect("/Projects/python/minipro/projects.db")
        self.cursor = self.conn.cursor()
  
    # function เรียกข้อมูลจาก database
    def Login_Data(self):
        User_Name = self.user.text().strip()
        Password = self.passw.text().strip()


        if User_Name and Password:
            try:
                # ใช้ SQL Query จากที่ user กับ pass
                Select_Data = "SELECT * FROM register WHERE user_name = ? AND password = ?"
                
                # เตรียมการ query โดยใช้ข้อมูลจากฟอร์ม
                self.cursor.execute(Select_Data, (User_Name, Password))
                result = self.cursor.fetchone()

                if result:  # ถ้าพบข้อมูลในฐานข้อมูล ให้แสดงข้อความ

                    if User_Name == 'admin' and Password == 'admin123': # เช็คว่าเป็น admin หรือไม่

                        QMessageBox.information(self, 'ยินดีต้อนรับ', 'เข้าสู่ระบบสำเร็จ')
                        
                        self.Link_Dashboard_App() # ถ้าเป็น admin ไปที่หน้าจัดการ (Dashboard)

                    else:  # ถ้าไม่ใช่ admin
                        QMessageBox.information(self, 'ยินดีต้อนรับ', 'เข้าสู่ระบบสำเร็จ')
                          
                        self.Link_Main_App()  # ไปที่หน้าหลัก (Main App)

                else: #ไม่พบให้แสดงข้อความ
                    QMessageBox.warning(self, 'ข้อมูลไม่ถูกต้อง', 'กรุณาระบุใหม่')
                    self.Clear_Data()


            except sqlite3.Error as e: # กรณีที่เชื่อมต่อแล้วเกิดปัญหา
                QMessageBox.warning(self, 'เกิดข้อผิดพลาด', f'ข้อผิดพลาด: {str(e)}')

        else:
            QMessageBox.warning(self, 'ข้อมูลไม่ครบถ้วน', 'กรุณากรอกข้อมูลให้ครบถ้วน')
            self.Clear_Data()


    # function รูป background
    def Background_Page_Login(self):
        """ ตั้งค่า Background Image """
        self.setStyleSheet("""
            QMainWindow {
                background-image: url("/Projects/python/minipro/Design/img/istock.jpg");
                background-repeat: no-repeat;
                background-position: left;
                background-size: cover;
            }
        """)

    #function link ไปที่ regi_app
    def Link_Regi(self):
        """ เปิดหน้าสมัครสมาชิก (จาก regi_app.py) """
        self.register_window = MyApp()  # เรียกคลาส register 
        self.register_window.show()
        self.close()  # ปิดหน้าล็อกอิน

    #function link ไปที่ main_app
    def Link_Main_App(self):
        from main_app import MymainApp # import class main
        self.main_window = MymainApp()  # เรียกคลาส main
        self.main_window.show()
        self.close()  # ปิดหน้าล็อกอิน 

    #function link ไปที่ dashboard
    def Link_Dashboard_App(self):
        from dashboard_app import MyDashboard # import class dashboard
        self.main_window = MyDashboard()   # เรียกคลาส Dashboard
        self.main_window.show()
        self.close()  # ปิดหน้าล็อกอิน 

    # ล้างข้อมูลหลังจากเพิ่มข้อมูลเสร็จ
    def Clear_Data(self):
        self.user.clear()
        self.passw.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())

