from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class MyCart(QWidget):
    def __init__(self):
        super().__init__()

        self.cart = []  # เก็บข้อมูลสินค้า
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # ตารางสินค้า
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ชื่อสินค้า", "ราคา", "จำนวน"])
        layout.addWidget(self.table)

        # **เพิ่ม QLabel สำหรับแสดงยอดรวม**
        self.total_label = QLabel("ยอดรวม: 0.00 บาท")
        layout.addWidget(self.total_label)

        # ปุ่มชำระเงินและพิมพ์ใบเสร็จ
        self.pay_button = QPushButton("ชำระเงิน")
        self.print_button = QPushButton("พิมพ์ใบเสร็จ")
        layout.addWidget(self.pay_button)
        layout.addWidget(self.print_button)

        self.setLayout(layout)

    def update_cart(self, cart_data):
        """ อัปเดตสินค้าในตะกร้าและคำนวณยอดรวม """
        self.cart = cart_data
        self.table.setRowCount(len(self.cart))

        total_price = 0
        for row, (prod_id, name, price, qty) in enumerate(self.cart):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{price:,.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(str(qty)))
            total_price += float(price) * int(qty)

        # **อัปเดตยอดรวมใน QLabel**
        self.total_label.setText(f"ยอดรวม: {total_price:,.2f} บาท")
