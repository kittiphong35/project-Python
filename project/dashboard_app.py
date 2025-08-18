import sys  # นำเข้าโมดูล sys สำหรับการจัดการกับระบบปฏิบัติการ
import sqlite3  # นำเข้าโมดูล sqlite3 สำหรับการเชื่อมต่อและจัดการฐานข้อมูล SQLite
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QTableWidget, QLabel  # นำเข้า widget ของ PyQt5 ที่จำเป็น
from PyQt5 import uic  # ใช้สำหรับโหลด UI ที่ออกแบบไว้
from PyQt5.QtGui import QIcon  # ใช้สำหรับการตั้งค่าไอคอน


class MyDashboard(QMainWindow):  # สร้างคลาส MyDashboard ที่สืบทอดจาก QMainWindow
    def __init__(self):
        """ ฟังก์ชันเริ่มต้น: โหลด UI, กำหนดค่าเริ่มต้น และเชื่อมปุ่ม """
        super().__init__()  # เรียกใช้งานคอนสตรัคเตอร์ของ QMainWindow
        uic.loadUi('/Projects/python/minipro/Design/dashboard.ui', self)  # โหลดไฟล์ UI

        self.setWindowTitle("Dashboard")  # ตั้งชื่อ Title ของหน้าต่าง
        self.setWindowIcon(QIcon("/Projects/python/minipro/Design/img/icon.png"))  # ตั้งไอคอนใน Title Bar
        self.setFixedSize(1610, 828)  # ล็อกขนาดหน้าต่างไม่ให้ปรับขนาดได้

        # เชื่อมปุ่มเข้ากับฟังก์ชัน
        self.exit_but.clicked.connect(self.close)  # ปุ่มปิดหน้าต่าง
        self.add_Button.clicked.connect(self.Add_Data)  # ปุ่มเพิ่มข้อมูลสินค้า
        self.delete_Button.clicked.connect(self.Delete_Data)  # ปุ่มลบสินค้า
        self.home.clicked.connect(self.Link_Main_App)  # ปุ่มกลับไปหน้าหลัก
        self.Search.clicked.connect(self.Search_Data)  # ปุ่มค้นหา
        

        # สร้างตารางหากยังไม่มี
        self.Create_Table()

        # โหลดข้อมูลเมื่อโปรแกรมเริ่มต้น
        self.Show_Data()

    def Create_Table(self):
        """ สร้างตาราง products หากยังไม่มีอยู่ในฐานข้อมูล """
        self.conn = sqlite3.connect('/Projects/python/minipro/projects.db')  # เชื่อมต่อกับฐานข้อมูล
        self.cursor = self.conn.cursor()  # สร้าง cursor เพื่อใช้ในการ execute SQL

        # สร้างตาราง 'products' ถ้ายังไม่มี
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pro_name TEXT NOT NULL,
            category TEXT NOT NULL,
            supplier TEXT NOT NULL,
            stock INTEGER NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL,
            warehouse TEXT NOT NULL,
            image_path TEXT NOT NULL 
        )
        """)
        
        self.conn.commit()  # บันทึกการเปลี่ยนแปลง
        self.conn.close()  # ปิดการเชื่อมต่อฐานข้อมูล

    def Add_Data(self):
        """ เพิ่มข้อมูลสินค้าใหม่ลงในฐานข้อมูล """
        Pro_Name = self.pro_name.text().strip()  # ดึงชื่อสินค้าจาก TextField
        Category = self.category.text().strip()  # ดึงหมวดหมู่จาก TextField
        Supplier = self.supplier.text().strip()  # ดึงผู้จำหน่ายจาก TextField
        Stock = self.stock.text().strip()  # ดึงจำนวนสต็อกจาก TextField
        Price = self.price.text().strip()  # ดึงราคาจาก TextField
        DateTime = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm:ss")  # แปลงวันที่เวลาเป็น String
        Warehouse = self.house.text().strip()  # ดึงคลังสินค้า
        Image = self.img.text().strip()  # ดึงรูปสินค้า
       


        # ตรวจสอบว่าทุกข้อมูลครบถ้วนหรือไม่
        if Pro_Name and Category and Supplier and Stock and Price and Warehouse :
            try:
                self.conn = sqlite3.connect('projects.db')  # เชื่อมต่อกับฐานข้อมูล
                self.cursor = self.conn.cursor()  # สร้าง cursor

                # คำสั่ง SQL สำหรับเพิ่มข้อมูลสินค้า
                Call_Data = """
                INSERT INTO products (pro_name, category, supplier, stock, price, date, warehouse, image_path) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                self.cursor.execute(Call_Data, (Pro_Name, Category, Supplier, Stock, Price, DateTime, Warehouse, Image))  # เพิ่มข้อมูล
                self.conn.commit()  # บันทึกการเปลี่ยนแปลง
                self.conn.close()  # ปิดการเชื่อมต่อ

                QMessageBox.information(self, 'สำเร็จ', 'เพิ่มข้อมูลเรียบร้อยแล้ว')  # แสดงข้อความสำเร็จ
                self.Show_Data()  # รีเฟรชข้อมูลในตาราง
                self.Clear_Data()  # ล้างข้อมูลในฟิลด์



            except sqlite3.IntegrityError:  # ถ้ามีข้อมูลซ้ำ
                QMessageBox.warning(self, 'ข้อผิดพลาด', 'ข้อมูลซ้ำ')

        else:
            QMessageBox.warning(self, 'ข้อผิดพลาด', 'กรุณากรอกข้อมูลให้ครบถ้วน')  # ถ้าข้อมูลไม่ครบ


    def Show_Data(self):
        """ โหลดและแสดงข้อมูลสินค้าใน TableWidget """
        self.conn = sqlite3.connect('/Projects/python/minipro/projects.db')  # เชื่อมต่อกับฐานข้อมูล
        self.cursor = self.conn.cursor()  # สร้าง cursor

        Show_Sql = "SELECT * FROM products"  # คำสั่ง SQL สำหรับดึงข้อมูลทั้งหมดจากตาราง 'products'
        self.cursor.execute(Show_Sql)
        products = self.cursor.fetchall()  # ดึงข้อมูลทั้งหมดมาเก็บในตัวแปร products
        self.conn.close()  # ปิดการเชื่อมต่อ

        # ล้างข้อมูลเก่าจากตารางก่อนโหลดข้อมูลใหม่
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        # ตั้งจำนวนแถวในตารางตามข้อมูลที่มี
        self.tableWidget.setRowCount(len(products))
        self.tableWidget.setColumnCount(9)  # กำหนดจำนวนคอลัมน์
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Product Name", "Category", "Supplier", "Stock", "Price", "Date", "Warehouse", "Image"])

        # ปรับขนาดคอลัมน์
        for col_index in range(9):
             self.tableWidget.setColumnWidth(col_index, 160)

        # แสดงข้อมูลในแต่ละเซลล์ของตาราง
        for row_index, row_data in enumerate(products):
            for col_index, data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(data)))

        self.tableWidget.resizeRowsToContents()  # ปรับความสูงแถวให้พอดี

        for row_index in range(len(products)):
            self.tableWidget.setRowHeight(row_index, 40)  # ปรับความสูงของแถว

        self.tableWidget.horizontalHeader().setStretchLastSection(True)  # ปรับการแสดงผลคอลัมน์สุดท้าย

        # ทำให้สามารถแก้ไขข้อมูลในเซลล์ได้
        self.tableWidget.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)

        # เชื่อมต่อฟังก์ชันเมื่อมีการแก้ไขข้อมูลในตาราง
        self.tableWidget.itemChanged.connect(self.on_item_changed)

        # คำนวณยอดรวมของสินค้าและราคา
        self.Calculate_Sum()

    def on_item_changed(self, item):
        """ เมื่อมีการแก้ไขข้อมูลในเซลล์จะอัปเดตฐานข้อมูล """
        row = item.row()  # ดึงแถวที่มีการแก้ไข
        col = item.column()  # ดึงคอลัมน์ที่มีการแก้ไข
        new_value = item.text()  # ดึงค่าที่ถูกแก้ไข

        if col == 0:  # ไม่สามารถแก้ไข ID ได้
            return

        # ดึง ID ของสินค้าที่แก้ไข
        product_id = self.tableWidget.item(row, 0).text()

        self.conn = sqlite3.connect('/Projects/python/minipro/projects.db')
        self.cursor = self.conn.cursor()

        # คำสั่ง SQL สำหรับอัปเดตข้อมูลในฐานข้อมูล
        if col == 1:
            update_sql = "UPDATE products SET pro_name = ? WHERE id = ?"
            self.cursor.execute(update_sql, (new_value, product_id))
        elif col == 2:
            update_sql = "UPDATE products SET category = ? WHERE id = ?"
            self.cursor.execute(update_sql, (new_value, product_id))
        elif col == 3:
            update_sql = "UPDATE products SET supplier = ? WHERE id = ?"
            self.cursor.execute(update_sql, (new_value, product_id))
        elif col == 4:
            update_sql = "UPDATE products SET stock = ? WHERE id = ?"
            self.cursor.execute(update_sql, (new_value, product_id))
        elif col == 5:
            update_sql = "UPDATE products SET price = ? WHERE id = ?"
            self.cursor.execute(update_sql, (new_value, product_id))
        elif col == 6:
            update_sql = "UPDATE products SET date = ? WHERE id = ?"
            self.cursor.execute(update_sql, (new_value, product_id))
        elif col == 7:
            update_sql = "UPDATE products SET warehouse = ? WHERE id = ?"
            self.cursor.execute(update_sql, (new_value, product_id))
        elif col == 8:
            update_sql = "UPDATE products SET image_path = ? WHERE id = ?"
            self.cursor.execute(update_sql, (new_value, product_id))
       
        # บันทึกการเปลี่ยนแปลง
        self.conn.commit()
        self.conn.close()

    def Delete_Data(self):
        """ ลบสินค้าตาม ID ที่เลือก """
        selected_row = self.tableWidget.currentRow()  # ตรวจสอบแถวที่เลือก
        if selected_row == -1:
            QMessageBox.warning(self, 'ข้อผิดพลาด', 'กรุณาเลือกสินค้าที่ต้องการลบ')
            return

        product_id = self.tableWidget.item(selected_row, 0).text()  # ดึง ID ของสินค้าที่เลือก

        confirm = QMessageBox.question(self, 'ยืนยันการลบ', f'ต้องการลบสินค้า ID {product_id} หรือไม่?', QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                self.conn = sqlite3.connect('/Projects/python/minipro/projects.db')
                self.cursor = self.conn.cursor()

                # คำสั่ง SQL สำหรับลบข้อมูล
                Delete_Sql = "DELETE FROM products WHERE id = ?"
                self.cursor.execute(Delete_Sql, (product_id,))
                self.conn.commit()  # บันทึกการเปลี่ยนแปลง
                self.conn.close()

                QMessageBox.information(self, 'สำเร็จ', 'ลบสินค้าสำเร็จ')
                self.Show_Data()  # รีเฟรชข้อมูล

            except sqlite3.Error as e:
                QMessageBox.warning(self, 'ข้อผิดพลาด', f'เกิดข้อผิดพลาด: {str(e)}')  # ถ้ามีข้อผิดพลาด

    def Calculate_Sum(self):
        """ คำนวณยอดรวมของสินค้าทั้งหมด (จำนวนและราคารวม) """
        self.conn = sqlite3.connect('/Projects/python/minipro/projects.db')
        self.cursor = self.conn.cursor()

        # คำสั่ง SQL สำหรับคำนวณยอดรวม
        self.cursor.execute("SELECT SUM(stock), SUM(price * stock) FROM products")
        result = self.cursor.fetchone()
        
        total_stock = result[0] if result[0] is not None else 0
        total_price = result[1] if result[1] is not None else 0

        self.conn.close()

        # แสดงยอดรวม
        self.stock_label.setText(f"{total_stock}")
        self.price_label.setText(f"{total_price:,.2f}")


    #function link ไปที่ main_app
    def Link_Main_App(self):
        from main_app import MymainApp
        self.main_window = MymainApp()  # เรียกคลาส 
        self.main_window.show()
        self.close()  # ปิดหน้าล็อกอิน 

    def Clear_Data(self):
        self.pro_name.clear()
        self.category.clear()
        self.supplier.clear()
        self.stock.clear()
        self.price.clear()
        self.dateTimeEdit.clear()
        self.house.clear()
        self.img.clear()


    def Search_Data(self):
        """ ค้นหาสินค้าในฐานข้อมูล """
        search_term = self.Search_2.text().strip()
        if search_term:
            self.conn = sqlite3.connect('/Projects/python/minipro/projects.db')  # เชื่อมต่อฐานข้อมูล
            self.cursor = self.conn.cursor()  # สร้าง cursor

            query = "SELECT * FROM products WHERE pro_name LIKE ?"
            self.cursor.execute(query, ('%' + search_term + '%',))
            products = self.cursor.fetchall()  # ดึงข้อมูลที่ค้นหาได้

            self.conn.close()  # ปิดการเชื่อมต่อฐานข้อมูล

            # แสดงผลข้อมูลที่ค้นหาบนตาราง
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(len(products))

            for row_index, row_data in enumerate(products):
                for col_index, data in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(data)))

            

if __name__ == '__main__':
    app = QApplication(sys.argv)  # สร้างแอปพลิเคชัน PyQt
    ex = MyDashboard()  # สร้างออบเจ็กต์ของ MyDashboard
    ex.show()  # แสดงหน้าต่าง
    sys.exit(app.exec_())  # เริ่มการทำงานของแอปพลิเคชัน
