# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dread_cosmetic_patches_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_DreadCosmeticPatchesDialog(object):
    def setupUi(self, DreadCosmeticPatchesDialog):
        if not DreadCosmeticPatchesDialog.objectName():
            DreadCosmeticPatchesDialog.setObjectName(u"DreadCosmeticPatchesDialog")
        DreadCosmeticPatchesDialog.resize(424, 203)
        self.gridLayout = QGridLayout(DreadCosmeticPatchesDialog)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.reset_button = QPushButton(DreadCosmeticPatchesDialog)
        self.reset_button.setObjectName(u"reset_button")

        self.gridLayout.addWidget(self.reset_button, 2, 2, 1, 1)

        self.accept_button = QPushButton(DreadCosmeticPatchesDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.gridLayout.addWidget(self.accept_button, 2, 0, 1, 1)

        self.cancel_button = QPushButton(DreadCosmeticPatchesDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 2, 1, 1, 1)

        self.scrollArea = QScrollArea(DreadCosmeticPatchesDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setObjectName(u"scroll_area_contents")
        self.scroll_area_contents.setGeometry(QRect(0, 0, 404, 156))
        self.verticalLayout = QVBoxLayout(self.scroll_area_contents)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.game_changes_box = QGroupBox(self.scroll_area_contents)
        self.game_changes_box.setObjectName(u"game_changes_box")
        self.game_changes_layout = QVBoxLayout(self.game_changes_box)
        self.game_changes_layout.setSpacing(6)
        self.game_changes_layout.setContentsMargins(11, 11, 11, 11)
        self.game_changes_layout.setObjectName(u"game_changes_layout")
        self.disable_hud_popup = QCheckBox(self.game_changes_box)
        self.disable_hud_popup.setObjectName(u"disable_hud_popup")

        self.game_changes_layout.addWidget(self.disable_hud_popup)

        self.open_map = QCheckBox(self.game_changes_box)
        self.open_map.setObjectName(u"open_map")

        self.game_changes_layout.addWidget(self.open_map)


        self.verticalLayout.addWidget(self.game_changes_box)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scroll_area_contents)

        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)


        self.retranslateUi(DreadCosmeticPatchesDialog)

        QMetaObject.connectSlotsByName(DreadCosmeticPatchesDialog)
    # setupUi

    def retranslateUi(self, DreadCosmeticPatchesDialog):
        DreadCosmeticPatchesDialog.setWindowTitle(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Metroid Dread - Cosmetic Options", None))
        self.reset_button.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Reset to Defaults", None))
        self.accept_button.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Accept", None))
        self.cancel_button.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Cancel", None))
        self.game_changes_box.setTitle(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Game Changes", None))
        self.disable_hud_popup.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Disable HUD popups", None))
        self.open_map.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Open map from start", None))
    # retranslateUi

