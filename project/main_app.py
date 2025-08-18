import sys  # ใช้สำหรับการจัดการระบบ เช่น รับพารามิเตอร์จากคอมมานด์ไลน์
import sqlite3  # ใช้สำหรับเชื่อมต่อและจัดการฐานข้อมูล SQLite
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QTableWidgetItem, QWidget, QVBoxLayout, QTableWidget, QPushButton, QHeaderView  # ใช้สร้าง GUI
from PyQt5 import uic  # ใช้โหลดไฟล์ .ui ที่ออกแบบด้วย Qt Designer
from log_app import MyApplication  # นำเข้าโมดูลที่ใช้สำหรับหน้าล็อกอิน
from PyQt5.QtGui import QIcon, QPixmap  # ใช้จัดการไอคอนและรูปภาพ
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog  # ใช้สำหรับการพิมพ์
from PyQt5.QtGui import QPainter  # ใช้สำหรับการสร้างรูปภาพ


class MyCartWindow(QWidget):
    """ หน้าตะกร้าสินค้า """
    def __init__(self, cart):
        super().__init__()
        self.cart = cart
        uic.loadUi("/Projects/python/minipro/Design/mycart.ui", self)
        self.setFixedSize(600, 400)
        self.setWindowIcon(QIcon("/Projects/python/minipro/Design/img/icon.png"))
        self.setWindowTitle("MyCart")

        self.printButton.clicked.connect(self.Print_Receipt)
        self.checkout_button.clicked.connect(self.checkout)
        
        
        self.update_table()

    def update_table(self):
        """ อัปเดตตารางให้แสดงสินค้าทั้งหมดในตะกร้า """
        self.table.setColumnCount(3)  # ตั้งค่าให้มี 3 คอลัมน์
        self.table.setHorizontalHeaderLabels(["ชื่อสินค้า", "ราคา", "จำนวน"])  # ตั้งค่าหัวตาราง
        self.table.setRowCount(len(self.cart))  # กำหนดจำนวนแถวตามจำนวนสินค้าในตะกร้า
        
        for row, (prod_id, name, price, qty) in enumerate(self.cart):
            self.table.setItem(row, 0, QTableWidgetItem(name))  # คอลัมน์ชื่อสินค้า
            self.table.setItem(row, 1, QTableWidgetItem(f"{float(price):,.2f} บาท"))  # คอลัมน์ราคา
            self.table.setItem(row, 2, QTableWidgetItem(str(int(qty))))  # คอลัมน์จำนวน

         # ปรับขนาดคอลัมน์
        self.table.setColumnWidth(0, 250)  # กำหนดความกว้างของคอลัมน์ชื่อสินค้า
        self.table.setColumnWidth(1, 100)  # กำหนดความกว้างของคอลัมน์ราคา
        self.table.setColumnWidth(2, 80)   # กำหนดความกว้างของคอลัมน์จำนวน

        # หรือให้คอลัมน์ปรับขนาดอัตโนมัติ
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def checkout(self):
        """ ชำระเงิน """
        total = sum(float(price) * int(qty) for _, _, price, qty in self.cart)
        QMessageBox.information(self, "ชำระเงิน", f"ยอดรวม: {total} บาท")
        self.cart.clear()
        self.update_table()


    def Print_Receipt(self):
        """ พิมพ์สลิปไปยังเครื่องพิมพ์ """
        if not self.cart:
            QMessageBox.warning(self, "ตะกร้าว่าง", "ไม่มีสินค้าในตะกร้า!")
            return

        # เตรียมข้อความใบเสร็จ
        receipt_text = "===== ใบเสร็จรับเงิน =====\n"
        total_price = 0

        for prod_id, name, price, qty in self.cart:
            line = f"{name} x {qty} - {float(price) * int(qty):,.2f} บาท\n"
            receipt_text += line
            total_price += float(price) * int(qty)

        receipt_text += f"\nรวมทั้งหมด: {total_price:,.2f} บาท"

        # ตั้งค่าเครื่องพิมพ์
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)
            painter.drawText(100, 100, receipt_text)
            painter.end()


class MymainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/Projects/python/minipro/Design/main.ui', self)  # โหลด UI จากไฟล์ .ui

        # ล็อกหน้าต่างให้มีขนาดคงที่
        self.setFixedSize(1179, 838)
        self.setWindowTitle("MainApp")  # ตั้งชื่อหน้าต่าง
        self.setWindowIcon(QIcon("/Projects/python/minipro/Design/img/icon.png"))  # ตั้งไอคอนของแอป

        # เชื่อมปุ่มต่าง ๆ เข้ากับฟังก์ชันที่เกี่ยวข้อง
        self.search_Button.clicked.connect(self.Search_Data)  # ปุ่มค้นหา
        self.log_out.clicked.connect(self.Log_Out)  # ปุ่มออกจากระบบ
        self.next_button.clicked.connect(self.Next_Page)  # ปุ่มถัดไป
        self.next_button2.clicked.connect(self.Before_Page) # ปุ่มก่อนหน้า
        self.mycart.clicked.connect(self.open_cart_window) # เปิดหน้าตะกร้า
        

        self.Button_img()
        self.Mycart_img()
        self.Background_Page()
        




        # เชื่อมต่อฐานข้อมูล SQLite
        self.conn = sqlite3.connect('/Projects/python/minipro/projects.db')
        self.cursor = self.conn.cursor()

        # เก็บรายการสินค้าและหน้าปัจจุบัน
        self.products = []  # รายการสินค้าทั้งหมดจากฐานข้อมูล
        self.current_index = 0  # ตัวชี้ตำแหน่งสินค้าปัจจุบัน
        self.cart = []  # ตะกร้าสินค้า

        # โหลดข้อมูลเมื่อเปิดโปรแกรม
        self.Load_All_Data()
        

    def Load_All_Data(self):
        """ โหลดสินค้าจากฐานข้อมูลและแสดงผล """
        query = "SELECT id, pro_name, price, stock, image_path FROM products"
        self.cursor.execute(query)
        self.products = self.cursor.fetchall()  # ดึงข้อมูลทั้งหมดจากฐานข้อมูล
        self.current_index = 0  # รีเซ็ตตำแหน่งเป็นหน้าแรก
        self.Display_Products()


    def Display_Products(self):
        """ แสดงสินค้าบน UI (ทีละ 4 ชิ้น) """
        labels = []
        for i in range(1, 5):
            labels.append((
                getattr(self, f"label_name{i}"),
                getattr(self, f"label_price{i}"),
                getattr(self, f"label_stock{i}"),
                getattr(self, f"label_img{i}"),
                getattr(self, f"add{i}")
            ))

        # ล้าง UI ก่อนแสดงผลใหม่
        for label_set in labels:
            label_set[0].clear()
            label_set[1].clear()
            label_set[2].clear()
            label_set[3].clear()

        for i, product in enumerate(self.products[self.current_index:self.current_index + 4]):
            id, name, price, stock, img_path = product
            labels[i][0].setText(f"ชื่อสินค้า: {name}")
            labels[i][1].setText(f"ราคา: {price} บาท")
            labels[i][2].setText(f"จำนวน: {stock} ชิ้น")

            # โหลดรูปสินค้า
            img_full_path = f"/Projects/python/minipro/Design/img/{img_path}"
            pixmap = QPixmap(img_full_path)
            labels[i][3].setPixmap(pixmap)
            labels[i][3].setScaledContents(True)

            # เชื่อมปุ่ม "เพิ่มสินค้า" กับฟังก์ชันเพิ่มลงตะกร้า
            labels[i][4].clicked.connect(lambda _, prod=product: self.Add_To_Cart(prod))


    def Next_Page(self):
        """ แสดงสินค้าถัดไป """
        if self.current_index + 4 < len(self.products):  # ตรวจสอบว่ามีสินค้าเหลือให้แสดงหรือไม่
            self.current_index += 4  # ขยับไปยังสินค้าถัดไป
            self.Display_Products()


    def Before_Page(self):  
        """ แสดงสินค้าก่อนหน้า """ 
        if self.current_index > 0:  # ตรวจสอบว่ามีสินค้าก่อนหน้าหรือไม่
            self.current_index -= 4  # ขยับไปยังชุดสินค้าก่อนหน้า
            self.Display_Products()


    def Search_Data(self):
        """ ค้นหาสินค้าในฐานข้อมูล """
        search_term = self.search.text().strip()
        if search_term:
            query = "SELECT id, pro_name, price, stock, image_path FROM products WHERE pro_name LIKE ?"
            self.cursor.execute(query, ('%' + search_term + '%',))
            self.products = self.cursor.fetchall()
            self.current_index = 0  # รีเซ็ตตำแหน่งเป็นหน้าแรก
            self.Display_Products()


    def Add_To_Cart(self, product):
        """ เพิ่มสินค้าลงตะกร้าและลดจำนวนสต็อก """
        prod_id, name, price, stock, img_path = product

        if stock > 0:
            # ลดสต็อกในฐานข้อมูล
            new_stock = stock - 1
            update_query = "UPDATE products SET stock = ? WHERE id = ?"
            self.cursor.execute(update_query, (new_stock, prod_id))
            self.conn.commit()  # บันทึกการเปลี่ยนแปลงในฐานข้อมูล

            # ตรวจสอบว่าสินค้าซ้ำในตะกร้าหรือไม่
            for i, (cart_prod_id, _, _, cart_qty) in enumerate(self.cart):
                if cart_prod_id == prod_id:
                    self.cart[i] = (prod_id, name, price, cart_qty + 1)  # เพิ่มจำนวนสินค้า
                    break
            else:
                self.cart.append((prod_id, name, price, 1))  # เพิ่มสินค้าใหม่พร้อม qty=1

            # โหลดข้อมูลสินค้าใหม่ เพื่ออัปเดต UI
            self.Load_All_Data()

            QMessageBox.information(self, "เพิ่มสินค้า", f"เพิ่ม {name} ลงในตะกร้าเรียบร้อย!")
        else:
            QMessageBox.warning(self, "สต็อกหมด", f"สินค้า {name} หมดแล้ว ไม่สามารถเพิ่มได้!")


    def Button_img(self):
        """ ตั้งค่าไอคอนปุ่ม """
        self.log_out.setStyleSheet("""
        QPushButton {
            background-image: url("/Projects/python/minipro/Design/img/logout.png");
            background-repeat: no-repeat;
            background-position: center;
            border: none;
        }
        """)

    def Mycart_img(self):
        """ ตั้งค่าไอคอนปุ่ม """
        self.mycart.setStyleSheet("""
        QPushButton {
            background-image: url("/Projects/python/minipro/Design/img/cart.png");
            background-repeat: no-repeat;
            background-position: center;
            border: none;
        }
        """)

    def Background_Page(self):
        self.setStyleSheet("""
            QMainWindow {
                background-image: url("/Projects/python/minipro/Design/img/isto.jpg");
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)


    def Log_Out(self):
        """ ออกจากระบบกลับไปหน้า Login """
        self.login_window = MyApplication()
        self.login_window.show()
        self.close()


    def open_cart_window(self):
        """ เปิดหน้าตะกร้าสินค้า """
        self.cart_window = MyCartWindow(self.cart)
        self.cart_window.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)  # สร้าง QApplication สำหรับรัน GUI
    window = MymainApp()
    window.show()  # แสดงหน้าต่างหลักของแอป
    sys.exit(app.exec_())  # รันแอปพลิเคชัน