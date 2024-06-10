from PySide6.QtCore import QFile, QIODevice, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
	QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QPushButton, QComboBox,
	QLineEdit, QDoubleSpinBox, QLabel, QFileDialog
)
from PySide6.QtGui import QAction

from services.JsonService import JsonService


class QtUI:
	def __init__(
		self,
		ui_path: str,
		groups: dict[str, list],
		slots: dict[str, any]
	) -> None:
		# 1. UI Loader
		loader = QUiLoader()
		# 2. Application
		app = QApplication()

		self.json_service = JsonService(True)

		self.ui_path = ui_path
		self.app = app
		self.main_window = self.open_ui(loader, ui_path)
		self.warn_dialog = self.open_ui(loader, "./src/soccer-brackets/view/ui/warning.ui")
		self._bind_slots(slots)
		self.update_groups(groups)

	def open_ui(self, loader: QUiLoader, ui_path: str):
		ui_file = QFile(ui_path)
		if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
			raise Exception(f"Cannot open file: {ui_file.errorString()}")
		
		widget = loader.load(ui_file)
		ui_file.close()

		if not widget:
			raise Exception(loader.errorString())
		return widget		

	def get_app(self) -> QApplication:
		return self.app

	def get_main_widget(self) -> QWidget:
		return self.main_window

	def get_team_form_data(self):
		from model.Criterias import Criterias
		return {
			"group": self.get_main_widget().findChild(QComboBox, "comboBoxGrupo").currentText(),
			"name": self.get_main_widget().findChild(QLineEdit, "lineEditNombre").text(),
			Criterias.ACCURACY.name: self.get_main_widget().findChild(
					QComboBox, "comboBoxPrecision").currentText(),
			Criterias.RESISTANCE.name: self.get_main_widget().findChild(
					QDoubleSpinBox, "doubleSpinBoxResistencia").value(),
			Criterias.SPEED.name: self.get_main_widget().findChild(QDoubleSpinBox, "doubleSpinBoxVelocidad").value(),
			Criterias.STRENGTH.name: self.get_main_widget().findChild(QDoubleSpinBox, "doubleSpinBoxFuerza").value()
		}

	def get_sim_form_data(self):
		return {
			"criteria": self.get_main_widget().findChild(QComboBox, "comboBoxCriterio").currentIndex()
		}

	def _bind_slots(self, slots: dict[str, any]) -> QWidget:
		btn_add: QPushButton = self.main_window.findChild(QPushButton, "pushButtonAgregar")
		btn_add.clicked.connect(slots["add"])

		btn_simulate: QPushButton = self.main_window.findChild(QPushButton, "pushButtonSimular")
		btn_simulate.clicked.connect(lambda: slots["sim"](1 + self.get_sim_form_data()["criteria"]))

		btn_draw: QPushButton = self.main_window.findChild(QPushButton, "pushButtonVisualizar")
		btn_draw.clicked.connect(slots["draw"])

		actn_save: QAction = self.main_window.findChild(QAction, "actionGuardarCopaComo")
		actn_save.triggered.connect(slots["save"])

		actn_load: QAction = self.main_window.findChild(QAction, "actionCargarCopa")
		actn_load.triggered.connect(slots["load"])

		actn_load_recent: QAction = self.main_window.findChild(QAction, "actionCopaReciente0")
		actn_load_recent.triggered.connect(
			lambda: slots["load"](self.json_service.load_json(actn_load_recent.text()))
		)

	def update_groups(self, groups: dict):
		tree_groups: QTreeWidget = self.main_window.findChild(QTreeWidget, "treeWidgetGrupos")
		tree_groups.sortByColumn(0, Qt.SortOrder.AscendingOrder)
		while tree_groups.topLevelItemCount() > 0:
			tree_groups.takeTopLevelItem(0)

		# Only for the static analyzer
		from model.Team import Team
		from model.Criterias import Criterias
		groups: dict[str, list[Team]] = groups
		for g in groups:
			tree_group = QTreeWidgetItem()
			tree_group.setText(0, g)
			for team in groups[g]:
				tree_team = QTreeWidgetItem()
				tree_team.setText(1, team.name)
				for i in range(len(Criterias)):
					stat = team.stats[Criterias(1 + i).name]
					tree_team.setText(
						2 + i,
						f"{stat:.2f}" if type(stat) is float else stat
					)
				tree_group.addChild(tree_team)
			tree_groups.addTopLevelItem(tree_group)
		tree_groups.expandAll()
	
	def update_jornadas(self, jornadas: list[dict]):
		tree_jornadas: QTreeWidget = self.main_window.findChild(QTreeWidget, "treeWidgetJornadas")
		tree_jornadas.sortByColumn(0, Qt.SortOrder.AscendingOrder)
		while tree_jornadas.topLevelItemCount() > 0:
			tree_jornadas.takeTopLevelItem(0)

		from model.BinaryTree import BinaryTree
		from model.Standing import Standing
		jornadas: list[list[BinaryTree]] = jornadas
		for j in range(len(jornadas)):
			tree_jornada = QTreeWidgetItem()
			tree_jornada.setText(0, f"Jornada {j}")
			if j > 0:
				for bintree in jornadas[j]:
					tree_team = QTreeWidgetItem()
					standing1: Standing = bintree.get_left().get_node()
					standing2: Standing = bintree.get_right().get_node()
					tree_team.setText(
						0,
						f"{standing1.get_team().get_name()} ({standing1.get_goals()}) vs. " +
						f"{standing2.get_team().get_name()} ({standing2.get_goals()})"
					)
					tree_jornada.addChild(tree_team)
			else:
				for bintree in jornadas[j]:
					tree_team = QTreeWidgetItem()
					standing: Standing = bintree.get_node()
					tree_team.setText(0, f"(N/A) {standing.get_team().get_name()}")
					tree_jornada.addChild(tree_team)
			if len(jornadas[j]) < 32:
				btn_visualize: QPushButton = self.main_window.findChild(QPushButton, "pushButtonVisualizar")
				btn_visualize.setDisabled(True)
			if len(jornadas[j]) < 2:
				btn_simulate: QPushButton = self.main_window.findChild(QPushButton, "pushButtonSimular")
				btn_simulate.setDisabled(True)
				
				btn_visualize: QPushButton = self.main_window.findChild(QPushButton, "pushButtonVisualizar")
				btn_visualize.setEnabled(True)
			tree_jornadas.addTopLevelItem(tree_jornada)

	def show(self):
		self.main_window.show()
		self.app.exec()
	
	def warn(self, message: str):
		warning: QLabel = self.warn_dialog.findChild(QLabel, "labelMessage")
		warning.setText(message)
		self.warn_dialog.show()
	
	def open_file(self):
		file = QFileDialog.getOpenFileName(
			self.main_window,
			"Cargar copa",
			"./src/soccer-brackets/",
			"Archivo JSON (*.json);;Todos los archivos (*.*)"
		)
		data = self.json_service.load_json(file[0])
		return data

	def save_file(self, data):
		file = QFileDialog.getSaveFileName(
			self.main_window,
			"Guardar copa",
			"./src/soccer-brackets",
			"Archivo JSON (*.json);;Todos los archivos (*.*)"
		)
		# File path only, without filter used
		self.json_service.save_json(file[0], data)
		return True
