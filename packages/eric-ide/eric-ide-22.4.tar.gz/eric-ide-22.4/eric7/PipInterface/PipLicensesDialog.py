# -*- coding: utf-8 -*-

# Copyright (c) 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show the licenses of an environment.
"""

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QDialog, QTreeWidgetItem

from EricGui.EricOverrideCursor import EricOverrideCursor

from .Ui_PipLicensesDialog import Ui_PipLicensesDialog


class PipLicensesDialog(QDialog, Ui_PipLicensesDialog):
    """
    Class implementing a dialog to show the licenses of an environment.
    """
    LicensesPackageColumn = 0
    LicensesVersionColumn = 1
    LicensesLicenseColumn = 2
    
    SummaryCountColumn = 0
    SummaryLicenseColumn = 1
    
    def __init__(self, pip, environment, localPackages=True, usersite=False,
                 parent=None):
        """
        Constructor
        
        @param pip reference to the pip interface object
        @type Pip
        @param environment name of the environment to show the licenses for
        @type str
        @param localPackages flag indicating to show the licenses for local
            packages only
        @type bool
        @param usersite flag indicating to show the licenses for packages
            installed in user-site directory only
        @type bool
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.__pip = pip
        self.__environment = environment
        
        self.localCheckBox.setChecked(localPackages)
        self.userCheckBox.setChecked(usersite)
        
        self.localCheckBox.toggled.connect(self.__refreshLicenses)
        self.userCheckBox.toggled.connect(self.__refreshLicenses)
        
        if environment:
            self.environmentLabel.setText("<b>{0}</b>".format(
                self.tr('Licenses of "{0}"').format(environment)
            ))
        else:
            # That should never happen; play it safe.
            self.environmentLabel.setText(self.tr("No environment specified."))
        
        self.__refreshLicenses()
        
    @pyqtSlot()
    def __refreshLicenses(self):
        """
        Private slot to refresh the license lists.
        """
        with EricOverrideCursor():
            self.licensesList.clear()
            self.summaryList.clear()
            
            # step 1: show the licenses per package
            self.licensesList.setUpdatesEnabled(False)
            licenses = self.__pip.getLicenses(
                self.__environment,
                localPackages=self.localCheckBox.isChecked(),
                usersite=self.userCheckBox.isChecked(),
            )
            for lic in licenses:
                QTreeWidgetItem(self.licensesList, [
                    lic["Name"],
                    lic["Version"],
                    lic["License"].replace("; ", "\n"),
                ])
            
            self.licensesList.sortItems(
                PipLicensesDialog.LicensesPackageColumn,
                Qt.SortOrder.AscendingOrder)
            for col in range(self.licensesList.columnCount()):
                self.licensesList.resizeColumnToContents(col)
            self.licensesList.setUpdatesEnabled(True)
            
            # step 2: show the licenses summary
            self.summaryList.setUpdatesEnabled(False)
            licenses = self.__pip.getLicensesSummary(
                self.__environment,
                localPackages=self.localCheckBox.isChecked(),
                usersite=self.userCheckBox.isChecked(),
            )
            for lic in licenses:
                QTreeWidgetItem(self.summaryList, [
                    "{0:4d}".format(lic["Count"]),
                    lic["License"].replace("; ", "\n"),
                ])
            
            self.summaryList.sortItems(
                PipLicensesDialog.SummaryLicenseColumn,
                Qt.SortOrder.AscendingOrder)
            for col in range(self.summaryList.columnCount()):
                self.summaryList.resizeColumnToContents(col)
            self.summaryList.setUpdatesEnabled(True)
