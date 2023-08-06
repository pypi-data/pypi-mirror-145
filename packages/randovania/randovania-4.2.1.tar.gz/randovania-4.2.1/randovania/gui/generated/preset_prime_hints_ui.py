# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_prime_hints.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetPrimeHints(object):
    def setupUi(self, PresetPrimeHints):
        if not PresetPrimeHints.objectName():
            PresetPrimeHints.setObjectName(u"PresetPrimeHints")
        PresetPrimeHints.resize(423, 259)
        self.centralWidget = QWidget(PresetPrimeHints)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.hint_layout = QVBoxLayout(self.centralWidget)
        self.hint_layout.setSpacing(6)
        self.hint_layout.setContentsMargins(11, 11, 11, 11)
        self.hint_layout.setObjectName(u"hint_layout")
        self.hint_layout.setContentsMargins(4, 8, 4, 0)
        self.hint_artifact_label = QLabel(self.centralWidget)
        self.hint_artifact_label.setObjectName(u"hint_artifact_label")
        self.hint_artifact_label.setWordWrap(True)

        self.hint_layout.addWidget(self.hint_artifact_label)

        self.hint_artifact_combo = QComboBox(self.centralWidget)
        self.hint_artifact_combo.addItem("")
        self.hint_artifact_combo.addItem("")
        self.hint_artifact_combo.addItem("")
        self.hint_artifact_combo.setObjectName(u"hint_artifact_combo")

        self.hint_layout.addWidget(self.hint_artifact_combo)

        PresetPrimeHints.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetPrimeHints)

        QMetaObject.connectSlotsByName(PresetPrimeHints)
    # setupUi

    def retranslateUi(self, PresetPrimeHints):
        PresetPrimeHints.setWindowTitle(QCoreApplication.translate("PresetPrimeHints", u"Hints", None))
        self.hint_artifact_label.setText(QCoreApplication.translate("PresetPrimeHints", u"<html><head/><body><p>This controls how precise the hints for Chozo Artifacts in Artifact Temple are.</p><p><span style=\" font-weight:600;\">No hints</span>: The scans provide no useful information.</p><p><span style=\" font-weight:600;\">Show only the area name</span>: Each scan says the corresponding artifact is in &quot;Tallon Overworld&quot;, &quot;Chozo Ruins&quot;, etc.</p><p><span style=\" font-weight:600;\">Show area and room name</span>: Each scan says the corresponding artifact is in &quot;Tallon Overworld - Transport Tunnel B&quot;, &quot;Phazon Mines - Metroid Quarantine B&quot;, etc. For rooms with more than one item location, there's no way to distinguish which one of them that artifact is in.</p></body></html>", None))
        self.hint_artifact_combo.setItemText(0, QCoreApplication.translate("PresetPrimeHints", u"No hints", None))
        self.hint_artifact_combo.setItemText(1, QCoreApplication.translate("PresetPrimeHints", u"Show only the area name", None))
        self.hint_artifact_combo.setItemText(2, QCoreApplication.translate("PresetPrimeHints", u"Show area and room name", None))

    # retranslateUi

