"""
Author: Avo-Catto
Page: window.py
Note: containing window with main processes
"""
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

import sys, json
import datetime

from main import *

# create window
class main(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 600)
        self.setWindowTitle("Rucksackproblem")
        self.setWindowIcon(qg.QIcon("./icon.png"))
        self.draw()

        check_file()

    def draw(self):

        # label Algorithmus:
        self.lab_algorythm = qw.QLabel(self, text="Algorithmus:")
        self.lab_algorythm.setStyleSheet("font-size: 20px")
        self.lab_algorythm.move(30, 30)

        # combo box of algorythms
        self.combo_algorythm = qw.QComboBox(self)
        self.combo_algorythm.setStyleSheet("font-size: 20px")
        self.combo_algorythm.addItems([" rekursiv", " greedy", " smart greedy"])
        self.combo_algorythm.setFixedSize(160, 30)
        self.combo_algorythm.move(150, 28)

        # scroll box of items
        self.scroll_items = qw.QScrollArea(self)
        self.scroll_items.setFixedSize(300, 330)
        self.scroll_items.move(30, 160)

        self.load_items()

        self.scroll_items.setVerticalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOn)

        # label Gegenstände
        self.lab_items = qw.QLabel(self, text=f"Gegenstände: {self.layout_list.count()}")
        self.lab_items.setStyleSheet("font-size: 20px")
        self.lab_items.move(30, 120)

        # selected item
        self.selec_item_lab = qw.QLabel(self, text="Name:")
        self.selec_item_lab.setStyleSheet("font-size: 20px")
        self.selec_item_lab.move(350, 160)

        self.selec_item_edit = qw.QLineEdit(self)
        self.selec_item_edit.setPlaceholderText("Gegenstand...")
        self.selec_item_edit.setStyleSheet("font-size: 20px")
        self.selec_item_edit.setFixedSize(200, 40)
        self.selec_item_edit.move(350, 200)

        # weight
        self.selec_item_weight_lab = qw.QLabel(self, text="Gewicht in kg:")
        self.selec_item_weight_lab.setStyleSheet("font-size: 20px")
        self.selec_item_weight_lab.move(350, 260)

        self.selec_item_weight_edit = qw.QLineEdit(self)
        self.selec_item_weight_edit.setPlaceholderText("Gewicht...")
        self.selec_item_weight_edit.setStyleSheet("font-size: 20px")
        self.selec_item_weight_edit.setFixedSize(200, 40)
        self.selec_item_weight_edit.move(350, 300)

        # worth
        self.selec_item_worth_lab = qw.QLabel(self, text="Wert in €:")
        self.selec_item_worth_lab.setStyleSheet("font-size: 20px")
        self.selec_item_worth_lab.move(350, 360)

        self.selec_item_worth_edit = qw.QLineEdit(self)
        self.selec_item_worth_edit.setPlaceholderText("Wert...")
        self.selec_item_worth_edit.setStyleSheet("font-size: 20px")
        self.selec_item_worth_edit.setFixedSize(200, 40)
        self.selec_item_worth_edit.move(350, 400)

        # button add
        self.add_but = qw.QPushButton(self, text="Hinzufügen")
        self.add_but.setStyleSheet("font-size: 20px")
        self.add_but.setFixedSize(160, 40)
        self.add_but.move(80, 520)
        self.add_but.clicked.connect(self.add)

        # button delete
        self.delete_but = qw.QPushButton(self, text="Löschen")
        self.delete_but.setStyleSheet("font-size: 20px")
        self.delete_but.setFixedSize(160, 40)
        self.delete_but.move(300, 520)
        self.delete_but.clicked.connect(self.delete)

        # button save
        self.save_but = qw.QPushButton(self, text="Übernehmen")
        self.save_but.setStyleSheet("font-size: 20px")
        self.save_but.setFixedSize(160, 40)
        self.save_but.move(520, 520)
        self.save_but.clicked.connect(self.save)

        # button start
        self.start_but = qw.QPushButton(self, text="Start")
        self.start_but.setStyleSheet("font-size: 20px")
        self.start_but.setFixedSize(160, 40)
        self.start_but.move(740, 520)
        self.start_but.clicked.connect(self.start)

        # label benötigte Zeit
        self.lab_time = qw.QLabel(self, text="Benötigte Zeit: 0 sek")
        self.lab_time.setStyleSheet("font-size: 20px")
        self.lab_time.setFixedWidth(300)
        self.lab_time.move(640, 30)
        
        # max weight label
        self.lab_max_weight = qw.QLabel(self, text="Maximales Gewicht: ")
        self.lab_max_weight.setStyleSheet("font-size: 20px")
        self.lab_max_weight.move(640, 75)

        # max weight edit
        self.max_weight_edit = qw.QLineEdit(self)
        self.max_weight_edit.setPlaceholderText("kg")
        self.max_weight_edit.setStyleSheet("font-size: 20px")
        self.max_weight_edit.setFixedSize(80, 35)
        self.max_weight_edit.move(825, 70)

        # label Rucksack
        self.lab_backpack = qw.QLabel(self, text="Rucksack: 0kg 0€")
        self.lab_backpack.setStyleSheet("font-size: 20px")
        self.lab_backpack.setFixedWidth(300)
        self.lab_backpack.move(640, 120)

        # scroll box of backpack
        self.scroll_items_backpack = qw.QScrollArea(self)
        self.scroll_items_backpack.setFixedSize(300, 330)
        self.scroll_items_backpack.move(640, 160)
        self.scroll_items_backpack.setVerticalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOn)
       


    # gui functions
    def get_items(self):
        items = []

        with open("./items.json", "r") as file:
            self.item_f = json.load(file)
            for i in self.item_f:
                if i == "zero":
                    pass
                else:
                    items.append(f" {i}   {self.item_f[i][0]}kg {self.item_f[i][1]}€")

        return items
    

    def get_backpack_items(self, items):
        output = []

        for i in items:
            output.append(f" {i}   {self.item_f[i][0]}kg {self.item_f[i][1]}€")

        return output

    
    def load_items(self):
        self.layout_list = qw.QVBoxLayout()
        self.layout_list.setAlignment(qc.Qt.AlignTop)
        self.widget_scroll = qw.QWidget()
        for i in self.get_items():
            object = qw.QPushButton()
            object.setFixedSize(260, 40)
            object.setText(i)
            object.setStyleSheet("font-size: 15px; text-align: left")
            object.clicked.connect(self.select)
            self.layout_list.addWidget(object)
        self.widget_scroll.setLayout(self.layout_list)
        self.scroll_items.setWidget(self.widget_scroll)
        try:
            self.lab_items.setText(f"Gegenstände: {self.layout_list.count()}")
        except:
            pass
    

    def load_backpack(self, items):
        self.layout_list_backpack = qw.QVBoxLayout()
        self.layout_list_backpack.setAlignment(qc.Qt.AlignTop)
        self.widget_scroll_backpack = qw.QWidget()
        for i in self.get_backpack_items(items):
            object = qw.QLabel()
            object.setFixedSize(260, 40)
            object.setText(i)
            object.setStyleSheet("font-size: 15px; text-align: left; border: 1px solid rgb(190,190,190); background-color: rgb(227,227,227)")
            self.layout_list_backpack.addWidget(object)
        self.widget_scroll_backpack.setLayout(self.layout_list_backpack)
        self.scroll_items_backpack.setWidget(self.widget_scroll_backpack)
    

    def select(self):
        try: self.selectet_obj.setEnabled(True)
        except: pass

        self.selectet_obj = self.sender()
        self.selectet_obj_text = self.selectet_obj.text().split()
        self.selec_item_edit.setText(self.selectet_obj_text[0])
        self.selec_item_weight_edit.setText(self.selectet_obj_text[1].removesuffix("kg"))
        self.selec_item_worth_edit.setText(self.selectet_obj_text[2].removesuffix("€"))
        self.selectet_obj.setEnabled(False)
    
    def clear(self):
        self.selec_item_edit.setText("")
        self.selec_item_weight_edit.setText("")
        self.selec_item_worth_edit.setText("")


    # button functions
    def add(self):
        self.item_f.update({"unbenannt": [0, 0]})
        with open("./items.json", "w") as file:
            json.dump(self.item_f, file)
        self.load_items()
        try: self.selectet_obj.setEnabled(True); self.selectet_obj = None
        except: pass
        self.clear()


    def delete(self):
        # delete item
        try: self.layout_list.removeWidget(self.selectet_obj)
        except: pass
        self.selectet_obj = None
        with open("./items.json", "r") as file:
            items = json.load(file)
            try: items.pop(self.selectet_obj_text[0])
            except: pass
        with open("./items.json", "w") as file:
            json.dump(items, file)
        self.load_items()


    def save(self):
        try:
            if self.selec_item_edit.text():
                self.item_f[self.selectet_obj.text().split()[0]]
                name = self.selec_item_edit.text().replace(" ", "_")
                self.selectet_obj.setText(f" {name}   {float(self.selec_item_weight_edit.text())}kg {float(self.selec_item_worth_edit.text())}€")
                for key in self.item_f:
                    if key == self.selectet_obj_text[0]:
                        self.item_f.pop(key)
                        self.item_f.update({name: [float(self.selec_item_weight_edit.text()), float(self.selec_item_worth_edit.text())]})
                        with open("./items.json", "w") as file:
                            json.dump(self.item_f, file)
                        break

                self.load_items()
                self.selectet_obj.setEnabled(True)
                self.selectet_obj = None
                self.clear()
        except:
            pass


    def start(self):
        try:
            algorithm = self.combo_algorythm.currentText().strip()
            weight_limit = float(self.max_weight_edit.text())

            if algorithm == "rekursiv":

                start_time = datetime.datetime.now()
                data = recursively_algorythm(weight_limit)
                end_time = datetime.datetime.now()
                result_time = int(datetime.timedelta.total_seconds(end_time - start_time))

                self.lab_time.setText(f"Benötigte Zeit: {result_time} sek")
                self.lab_backpack.setText(f"Rucksack: {round(data[0], 2)}kg {round(data[1], 2)}€")
                self.load_backpack(data[2])

            elif algorithm == "greedy":

                start_time = datetime.datetime.now()
                data = greedy_algorythm(weight_limit)
                end_time = datetime.datetime.now()
                result_time = int(datetime.timedelta.total_seconds(end_time - start_time))

                self.lab_time.setText(f"Benötigte Zeit: {result_time} sek")
                self.lab_backpack.setText(f"Rucksack: {round(data[2], 2)}kg {round(data[1], 2)}€")
                self.load_backpack(data[0])
            
            elif algorithm == "smart greedy":

                start_time = datetime.datetime.now()
                data = smart_greedy_algorithm(weight_limit)
                end_time = datetime.datetime.now()
                result_time = int(datetime.timedelta.total_seconds(end_time - start_time))

                self.lab_time.setText(f"Benötigte Zeit: {result_time} sek")
                self.lab_backpack.setText(f"Rucksack: {round(data[2], 2)}kg {round(data[1], 2)}€")
                self.load_backpack(data[0])
            
            else:
                ...

        except:
            pass


# show window
def show_gui():
    app = qw.QApplication(sys.argv)
    window = main()
    window.show()
    app.exec()
