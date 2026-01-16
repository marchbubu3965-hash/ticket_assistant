from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QRadioButton,
    QButtonGroup,
    QSpinBox,
    QDateEdit,
    QGroupBox,
)
from PySide6.QtCore import QDate

from ui.station_autocomplete import StationAutoComplete


class TicketPanel(QWidget):
    def __init__(
        self,
        ticket_controller,
        employee_selection,
        station_controller,
        parent=None,
    ):
        super().__init__(parent)

        self.ticket_controller = ticket_controller
        self.employee_selection = employee_selection
        self.station_controller = station_controller

        self.employee_selection.subscribe(self._on_employee_changed)

        self._init_ui()

    # =========================
    # UI
    # =========================
    def _init_ui(self):
        layout = QVBoxLayout(self)

        # ===== 員工資訊 =====
        self.current_employee_label = QLabel("目前訂票人：尚未選擇")
        self.current_employee_label.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        layout.addWidget(self.current_employee_label)

        # ===== 身分證（顯示用）=====
        self.id_number_input = QLineEdit()
        self.id_number_input.setPlaceholderText("身分證字號")
        self.id_number_input.setReadOnly(True)
        layout.addWidget(self.id_number_input)

        # ===== 起訖站 =====
        self.from_station = StationAutoComplete(
            controller=self.station_controller,
            placeholder="起站（例如：台北 / 1000）",
        )
        self.to_station = StationAutoComplete(
            controller=self.station_controller,
            placeholder="迄站（例如：台中 / 3300）",
        )

        layout.addWidget(self.from_station)
        layout.addWidget(self.to_station)

        # ===== 行程類型 =====
        trip_box = QGroupBox("行程類型")
        trip_layout = QHBoxLayout(trip_box)

        self.one_way_radio = QRadioButton("單程")
        self.round_trip_radio = QRadioButton("來回")
        self.one_way_radio.setChecked(True)

        self.trip_group = QButtonGroup(self)
        self.trip_group.addButton(self.one_way_radio)
        self.trip_group.addButton(self.round_trip_radio)

        trip_layout.addWidget(self.one_way_radio)
        trip_layout.addWidget(self.round_trip_radio)
        layout.addWidget(trip_box)

        # ===== 訂票數量 =====
        self.ticket_count = QSpinBox()
        self.ticket_count.setRange(1, 10)
        self.ticket_count.setValue(1)
        self.ticket_count.setPrefix("張數：")
        layout.addWidget(self.ticket_count)

        # ===== 日期 =====
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(self.date_input)

        # ===== 車次 =====
        self.train_no_1 = QLineEdit()
        self.train_no_1.setPlaceholderText("車次 1（必填）")

        self.train_no_2 = QLineEdit()
        self.train_no_2.setPlaceholderText("車次 2（選填）")

        self.train_no_3 = QLineEdit()
        self.train_no_3.setPlaceholderText("車次 3（選填）")

        layout.addWidget(self.train_no_1)
        layout.addWidget(self.train_no_2)
        layout.addWidget(self.train_no_3)

        layout.addStretch()

        # ===== 執行訂票 =====
        self.submit_btn = QPushButton("開始訂票")
        self.submit_btn.clicked.connect(self._on_submit)
        layout.addWidget(self.submit_btn)

    # =========================
    # Employee Sync
    # =========================
    def _on_employee_changed(self, employee):
        if not employee:
            self.current_employee_label.setText("目前訂票人：尚未選擇")
            self.id_number_input.clear()
            return

        self.current_employee_label.setText(
            f"目前訂票人：{employee.emp_id} {employee.name}"
        )
        self.id_number_input.setText(employee.id_number)

    # =========================
    # Submit
    # =========================
    def _on_submit(self):
        employee = self.employee_selection.get()
        if not employee:
            QMessageBox.warning(self, "錯誤", "尚未選擇訂票員工")
            return

        from_code = self.from_station.get_station_code()
        to_code = self.to_station.get_station_code()

        if not from_code or not to_code:
            QMessageBox.warning(self, "錯誤", "請選擇起訖站")
            return

        train_nos = [
            self.train_no_1.text().strip(),
            self.train_no_2.text().strip(),
            self.train_no_3.text().strip(),
        ]

        try:
            self.ticket_controller.submit_ticket(
                employee=employee,
                from_station=from_code,
                to_station=to_code,
                date=self.date_input.date().toString("yyyy-MM-dd"),
                train_nos=train_nos,
                ticket_count=self.ticket_count.value(),
                one_way=self.one_way_radio.isChecked(),
            )

            QMessageBox.information(self, "完成", "訂票流程已啟動")

        except Exception as e:
            QMessageBox.critical(self, "訂票失敗", str(e))


# from PySide6.QtWidgets import (
#     QWidget,
#     QVBoxLayout,
#     QHBoxLayout,
#     QLabel,
#     QPushButton,
#     QLineEdit,
#     QMessageBox,
#     QRadioButton,
#     QButtonGroup,
#     QSpinBox,
#     QDateEdit,
#     QGroupBox,
# )
# from PySide6.QtCore import QDate

# from ui.station_autocomplete import StationAutoComplete


# class TicketPanel(QWidget):
#     def __init__(
#         self,
#         ticket_controller,
#         employee_selection,
#         station_controller,
#         parent=None,
#     ):
#         super().__init__(parent)

#         self.ticket_controller = ticket_controller
#         self.employee_selection = employee_selection
#         self.station_controller = station_controller

#         self.employee_selection.subscribe(self._on_employee_changed)

#         self._init_ui()

#     # =========================
#     # UI
#     # =========================
#     def _init_ui(self):
#         layout = QVBoxLayout(self)

#         # ===== 員工資訊 =====
#         self.current_employee_label = QLabel("目前訂票人：尚未選擇")
#         self.current_employee_label.setStyleSheet(
#             "font-size: 16px; font-weight: bold;"
#         )
#         layout.addWidget(self.current_employee_label)

#         # ===== 身分證（顯示用）=====
#         self.id_number_input = QLineEdit()
#         self.id_number_input.setPlaceholderText("身分證字號")
#         self.id_number_input.setReadOnly(True)
#         layout.addWidget(self.id_number_input)

#         # ===== 起訖站 =====
#         self.from_station = StationAutoComplete(
#             controller=self.station_controller,
#             placeholder="起站（例如：台北 / 1000）",
#         )
#         self.to_station = StationAutoComplete(
#             controller=self.station_controller,
#             placeholder="迄站（例如：台中 / 3300）",
#         )

#         layout.addWidget(self.from_station)
#         layout.addWidget(self.to_station)

#         # ===== 行程類型 =====
#         trip_box = QGroupBox("行程類型")
#         trip_layout = QHBoxLayout(trip_box)

#         self.one_way_radio = QRadioButton("單程")
#         self.round_trip_radio = QRadioButton("來回")
#         self.one_way_radio.setChecked(True)

#         self.trip_group = QButtonGroup(self)
#         self.trip_group.addButton(self.one_way_radio)
#         self.trip_group.addButton(self.round_trip_radio)

#         trip_layout.addWidget(self.one_way_radio)
#         trip_layout.addWidget(self.round_trip_radio)
#         layout.addWidget(trip_box)

#         # ===== 訂票數量 =====
#         self.ticket_count = QSpinBox()
#         self.ticket_count.setRange(1, 10)
#         self.ticket_count.setValue(1)
#         self.ticket_count.setPrefix("張數：")
#         layout.addWidget(self.ticket_count)

#         # ===== 日期 =====
#         self.date_input = QDateEdit()
#         self.date_input.setCalendarPopup(True)
#         self.date_input.setDate(QDate.currentDate())
#         self.date_input.setDisplayFormat("yyyy-MM-dd")
#         layout.addWidget(self.date_input)

#         # ===== 車次 =====
#         self.train_no_1 = QLineEdit()
#         self.train_no_1.setPlaceholderText("車次 1（必填）")

#         self.train_no_2 = QLineEdit()
#         self.train_no_2.setPlaceholderText("車次 2（選填）")

#         self.train_no_3 = QLineEdit()
#         self.train_no_3.setPlaceholderText("車次 3（選填）")

#         layout.addWidget(self.train_no_1)
#         layout.addWidget(self.train_no_2)
#         layout.addWidget(self.train_no_3)

#         layout.addStretch()

#         # ===== 執行訂票 =====
#         self.submit_btn = QPushButton("開始訂票")
#         self.submit_btn.clicked.connect(self._on_submit)
#         layout.addWidget(self.submit_btn)

#     # =========================
#     # Employee Sync
#     # =========================
#     def _on_employee_changed(self, employee):
#         if not employee:
#             self.current_employee_label.setText("目前訂票人：尚未選擇")
#             self.id_number_input.clear()
#             return

#         self.current_employee_label.setText(
#             f"目前訂票人：{employee.emp_id} {employee.name}"
#         )
#         self.id_number_input.setText(employee.id_number)

#     # =========================
#     # Submit
#     # =========================
#     def _on_submit(self):
#         employee = self.employee_selection.get()
#         if not employee:
#             QMessageBox.warning(self, "錯誤", "尚未選擇訂票員工")
#             return

#         from_code = self.from_station.get_station_code()
#         to_code = self.to_station.get_station_code()

#         if not from_code or not to_code:
#             QMessageBox.warning(self, "錯誤", "請選擇起訖站")
#             return

#         if from_code == to_code:
#             QMessageBox.warning(self, "錯誤", "起站與迄站不可相同")
#             return

#         train_nos = [
#             self.train_no_1.text().strip(),
#             self.train_no_2.text().strip(),
#             self.train_no_3.text().strip(),
#         ]

#         one_way = self.one_way_radio.isChecked()
#         ticket_count = self.ticket_count.value()
#         date_str = self.date_input.date().toString("yyyy-MM-dd")

#         try:
#             self.ticket_controller.submit_ticket(
#                 employee=employee,
#                 from_station=from_code,
#                 to_station=to_code,
#                 date=date_str,
#                 train_nos=train_nos,
#                 ticket_count=ticket_count,
#                 one_way=one_way,
#             )

#             QMessageBox.information(self, "完成", "訂票流程已啟動")

#         except Exception as e:
#             QMessageBox.critical(self, "訂票失敗", str(e))



