# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dread_game_export_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_DreadGameExportDialog(object):
    def setupUi(self, DreadGameExportDialog):
        if not DreadGameExportDialog.objectName():
            DreadGameExportDialog.setObjectName(u"DreadGameExportDialog")
        DreadGameExportDialog.resize(508, 270)
        self.gridLayout = QGridLayout(DreadGameExportDialog)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.output_file_label = QLabel(DreadGameExportDialog)
        self.output_file_label.setObjectName(u"output_file_label")
        self.output_file_label.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.output_file_label, 4, 0, 1, 2)

        self.cancel_button = QPushButton(DreadGameExportDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 8, 2, 1, 1)

        self.output_file_edit = QLineEdit(DreadGameExportDialog)
        self.output_file_edit.setObjectName(u"output_file_edit")

        self.gridLayout.addWidget(self.output_file_edit, 5, 0, 1, 2)

        self.input_file_edit = QLineEdit(DreadGameExportDialog)
        self.input_file_edit.setObjectName(u"input_file_edit")

        self.gridLayout.addWidget(self.input_file_edit, 2, 0, 1, 2)

        self.output_file_button = QPushButton(DreadGameExportDialog)
        self.output_file_button.setObjectName(u"output_file_button")
        self.output_file_button.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.output_file_button, 5, 2, 1, 1)

        self.accept_button = QPushButton(DreadGameExportDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.gridLayout.addWidget(self.accept_button, 8, 0, 1, 1)

        self.auto_save_spoiler_check = QCheckBox(DreadGameExportDialog)
        self.auto_save_spoiler_check.setObjectName(u"auto_save_spoiler_check")

        self.gridLayout.addWidget(self.auto_save_spoiler_check, 7, 0, 1, 1)

        self.input_file_label = QLabel(DreadGameExportDialog)
        self.input_file_label.setObjectName(u"input_file_label")
        self.input_file_label.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.input_file_label, 1, 0, 1, 2)

        self.input_file_button = QPushButton(DreadGameExportDialog)
        self.input_file_button.setObjectName(u"input_file_button")
        self.input_file_button.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.input_file_button, 2, 2, 1, 1)

        self.description_label = QLabel(DreadGameExportDialog)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setWordWrap(True)

        self.gridLayout.addWidget(self.description_label, 0, 0, 1, 3)


        self.retranslateUi(DreadGameExportDialog)

        QMetaObject.connectSlotsByName(DreadGameExportDialog)
    # setupUi

    def retranslateUi(self, DreadGameExportDialog):
        DreadGameExportDialog.setWindowTitle(QCoreApplication.translate("DreadGameExportDialog", u"Game Patching", None))
        self.output_file_label.setText(QCoreApplication.translate("DreadGameExportDialog", u"Output Path", None))
        self.cancel_button.setText(QCoreApplication.translate("DreadGameExportDialog", u"Cancel", None))
        self.output_file_edit.setPlaceholderText(QCoreApplication.translate("DreadGameExportDialog", u"Path where to place randomized game", None))
        self.input_file_edit.setPlaceholderText(QCoreApplication.translate("DreadGameExportDialog", u"Path to vanilla extracted RomFS", None))
        self.output_file_button.setText(QCoreApplication.translate("DreadGameExportDialog", u"Select File", None))
        self.accept_button.setText(QCoreApplication.translate("DreadGameExportDialog", u"Accept", None))
        self.auto_save_spoiler_check.setText(QCoreApplication.translate("DreadGameExportDialog", u"Include a spoiler log on same directory", None))
        self.input_file_label.setText(QCoreApplication.translate("DreadGameExportDialog", u"Input Path (Unmodified Dread extracted RomFS)", None))
        self.input_file_button.setText(QCoreApplication.translate("DreadGameExportDialog", u"Select File", None))
        self.description_label.setText(QCoreApplication.translate("DreadGameExportDialog", u"<html><head/><body><p>In order to create the randomized game, an extracted RomFS of Metroid Dread for the Nintendo Switch is necessary.</p></body></html>", None))
    # retranslateUi

