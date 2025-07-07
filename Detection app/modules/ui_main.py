# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainkuLFMO.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGraphicsView, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTextBrowser, QTextEdit, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1365, 884)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1024, 768))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background"
                        "-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/PyDracula.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(18"
                        "9, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb("
                        "189, 147, 249);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border"
                        "-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-sty"
                        "le: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb"
                        "(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-co"
                        "lor: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-c"
                        "olor: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
""
                        "QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     su"
                        "bcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	back"
                        "ground-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subco"
                        "ntrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    h"
                        "eight: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLi"
                        "nkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.horizontalLayout_8 = QHBoxLayout(self.styleSheet)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Semibold"])
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy1)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy1.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy1)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_widgets = QPushButton(self.topMenu)
        self.btn_widgets.setObjectName(u"btn_widgets")
        sizePolicy1.setHeightForWidth(self.btn_widgets.sizePolicy().hasHeightForWidth())
        self.btn_widgets.setSizePolicy(sizePolicy1)
        self.btn_widgets.setMinimumSize(QSize(0, 45))
        self.btn_widgets.setFont(font)
        self.btn_widgets.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_widgets.setLayoutDirection(Qt.LeftToRight)
        self.btn_widgets.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-gamepad.png);\n"
"background-image: url(:/icons/images/icons/cil-input-power.png);")

        self.verticalLayout_8.addWidget(self.btn_widgets)

        self.btn_new = QPushButton(self.topMenu)
        self.btn_new.setObjectName(u"btn_new")
        sizePolicy1.setHeightForWidth(self.btn_new.sizePolicy().hasHeightForWidth())
        self.btn_new.setSizePolicy(sizePolicy1)
        self.btn_new.setMinimumSize(QSize(0, 45))
        self.btn_new.setFont(font)
        self.btn_new.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_new.setLayoutDirection(Qt.LeftToRight)
        self.btn_new.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_settings.png);")

        self.verticalLayout_8.addWidget(self.btn_new)

        self.btn_save = QPushButton(self.topMenu)
        self.btn_save.setObjectName(u"btn_save")
        sizePolicy1.setHeightForWidth(self.btn_save.sizePolicy().hasHeightForWidth())
        self.btn_save.setSizePolicy(sizePolicy1)
        self.btn_save.setMinimumSize(QSize(0, 45))
        self.btn_save.setFont(font)
        self.btn_save.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_save.setLayoutDirection(Qt.LeftToRight)
        self.btn_save.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-save.png);")

        self.verticalLayout_8.addWidget(self.btn_save)

        self.btn_computer = QPushButton(self.topMenu)
        self.btn_computer.setObjectName(u"btn_computer")
        self.btn_computer.setMinimumSize(QSize(0, 45))
        self.btn_computer.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-devices.png);")

        self.verticalLayout_8.addWidget(self.btn_computer)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)

        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setFrameShape(QFrame.NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.btn_share = QPushButton(self.extraTopMenu)
        self.btn_share.setObjectName(u"btn_share")
        sizePolicy1.setHeightForWidth(self.btn_share.sizePolicy().hasHeightForWidth())
        self.btn_share.setSizePolicy(sizePolicy1)
        self.btn_share.setMinimumSize(QSize(0, 45))
        self.btn_share.setFont(font)
        self.btn_share.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_share.setLayoutDirection(Qt.LeftToRight)
        self.btn_share.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-share-boxed.png);")

        self.verticalLayout_11.addWidget(self.btn_share)

        self.btn_adjustments = QPushButton(self.extraTopMenu)
        self.btn_adjustments.setObjectName(u"btn_adjustments")
        sizePolicy1.setHeightForWidth(self.btn_adjustments.sizePolicy().hasHeightForWidth())
        self.btn_adjustments.setSizePolicy(sizePolicy1)
        self.btn_adjustments.setMinimumSize(QSize(0, 45))
        self.btn_adjustments.setFont(font)
        self.btn_adjustments.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_adjustments.setLayoutDirection(Qt.LeftToRight)
        self.btn_adjustments.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-equalizer.png);")

        self.verticalLayout_11.addWidget(self.btn_adjustments)

        self.btn_more = QPushButton(self.extraTopMenu)
        self.btn_more.setObjectName(u"btn_more")
        sizePolicy1.setHeightForWidth(self.btn_more.sizePolicy().hasHeightForWidth())
        self.btn_more.setSizePolicy(sizePolicy1)
        self.btn_more.setMinimumSize(QSize(0, 45))
        self.btn_more.setFont(font)
        self.btn_more.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_more.setLayoutDirection(Qt.LeftToRight)
        self.btn_more.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-layers.png);")

        self.verticalLayout_11.addWidget(self.btn_more)


        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignTop)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.setStyleSheet(u"background: transparent;")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)


        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy2)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        self.titleRightInfo.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy3)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsTopBtn.setIcon(icon1)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_49 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(1024, 768))
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"background-position: center;\n"
"background-repeat: no-repeat;")
        self.verticalLayout_36 = QVBoxLayout(self.home)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_35 = QVBoxLayout()
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.verticalGroupBox_8 = QGroupBox(self.home)
        self.verticalGroupBox_8.setObjectName(u"verticalGroupBox_8")
        font4 = QFont()
        font4.setFamilies([u"Microsoft YaHei UI"])
        font4.setPointSize(20)
        font4.setBold(False)
        font4.setItalic(False)
        self.verticalGroupBox_8.setFont(font4)
        self.verticalGroupBox_8.setStyleSheet(u"font: 20pt \"Microsoft YaHei UI\";")
        self.verticalGroupBox_8.setAlignment(Qt.AlignCenter)
        self.verticalGroupBox_8.setFlat(False)
        self.verticalLayout_32 = QVBoxLayout(self.verticalGroupBox_8)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.verticalLayout_29 = QVBoxLayout()
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.label_4 = QLabel(self.verticalGroupBox_8)
        self.label_4.setObjectName(u"label_4")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy4)
        self.label_4.setMinimumSize(QSize(310, 310))
        self.label_4.setMaximumSize(QSize(1500, 1500))
        self.label_4.setPixmap(QPixmap(u":/images/images/images/175213819725034291201-310310.png"))
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_29.addWidget(self.label_4)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_29.addItem(self.verticalSpacer_5)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_12)

        self.btn_charge = QPushButton(self.verticalGroupBox_8)
        self.btn_charge.setObjectName(u"btn_charge")
        self.btn_charge.setMinimumSize(QSize(180, 60))
        self.btn_charge.setMaximumSize(QSize(1000, 1000))
        self.btn_charge.setLayoutDirection(Qt.LeftToRight)
        self.btn_charge.setStyleSheet(u"background-color: rgb(52, 59, 72);\n"
"font: 20pt \"Microsoft YaHei UI\";\n"
"alternate-background-color: rgb(255, 255, 255);")

        self.horizontalLayout_23.addWidget(self.btn_charge)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_11)

        self.horizontalLayout_23.setStretch(0, 1)
        self.horizontalLayout_23.setStretch(1, 2)
        self.horizontalLayout_23.setStretch(2, 1)

        self.verticalLayout_29.addLayout(self.horizontalLayout_23)

        self.label_100 = QLabel(self.verticalGroupBox_8)
        self.label_100.setObjectName(u"label_100")
        self.label_100.setFocusPolicy(Qt.NoFocus)
        self.label_100.setStyleSheet(u"font: 12pt \"\u5fae\u8f6f\u96c5\u9ed1\";")
        self.label_100.setAlignment(Qt.AlignCenter)

        self.verticalLayout_29.addWidget(self.label_100)

        self.verticalLayout_29.setStretch(0, 12)
        self.verticalLayout_29.setStretch(1, 2)
        self.verticalLayout_29.setStretch(2, 4)
        self.verticalLayout_29.setStretch(3, 1)

        self.verticalLayout_32.addLayout(self.verticalLayout_29)


        self.horizontalLayout_19.addWidget(self.verticalGroupBox_8)

        self.verticalGroupBox_9 = QGroupBox(self.home)
        self.verticalGroupBox_9.setObjectName(u"verticalGroupBox_9")
        self.verticalGroupBox_9.setFont(font4)
        self.verticalGroupBox_9.setStyleSheet(u"font: 20pt \"Microsoft YaHei UI\";")
        self.verticalGroupBox_9.setAlignment(Qt.AlignCenter)
        self.verticalGroupBox_9.setFlat(False)
        self.verticalLayout_54 = QVBoxLayout(self.verticalGroupBox_9)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.verticalLayout_53 = QVBoxLayout()
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.verticalLayout_33 = QVBoxLayout()
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_33.addItem(self.verticalSpacer_7)

        self.verticalLayout_31 = QVBoxLayout()
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.verticalLayout_30 = QVBoxLayout()
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_102 = QLabel(self.verticalGroupBox_9)
        self.label_102.setObjectName(u"label_102")
        self.label_102.setFocusPolicy(Qt.NoFocus)
        self.label_102.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_17.addWidget(self.label_102)

        self.lineEdit = QLineEdit(self.verticalGroupBox_9)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 0))
        self.lineEdit.setStyleSheet(u"background-color: rgb(52, 59, 72);\n"
"font: 20pt \"Microsoft YaHei UI\";")
        self.lineEdit.setInputMethodHints(Qt.ImhDigitsOnly)

        self.horizontalLayout_17.addWidget(self.lineEdit)

        self.label_5 = QLabel(self.verticalGroupBox_9)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_17.addWidget(self.label_5)


        self.verticalLayout_30.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_103 = QLabel(self.verticalGroupBox_9)
        self.label_103.setObjectName(u"label_103")
        self.label_103.setFocusPolicy(Qt.NoFocus)
        self.label_103.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_18.addWidget(self.label_103)

        self.lineEdit_5 = QLineEdit(self.verticalGroupBox_9)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(0, 0))
        self.lineEdit_5.setStyleSheet(u"background-color: rgb(52, 59, 72);\n"
"font: 20pt \"Microsoft YaHei UI\";")
        self.lineEdit_5.setInputMethodHints(Qt.ImhDigitsOnly)

        self.horizontalLayout_18.addWidget(self.lineEdit_5)

        self.label_6 = QLabel(self.verticalGroupBox_9)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_18.addWidget(self.label_6)


        self.verticalLayout_30.addLayout(self.horizontalLayout_18)


        self.verticalLayout_31.addLayout(self.verticalLayout_30)

        self.horizontalLayout_72 = QHBoxLayout()
        self.horizontalLayout_72.setObjectName(u"horizontalLayout_72")
        self.label_105 = QLabel(self.verticalGroupBox_9)
        self.label_105.setObjectName(u"label_105")
        self.label_105.setFocusPolicy(Qt.NoFocus)
        self.label_105.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_72.addWidget(self.label_105)

        self.lineEdit_9 = QLineEdit(self.verticalGroupBox_9)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setMinimumSize(QSize(0, 0))
        self.lineEdit_9.setStyleSheet(u"background-color: rgb(52, 59, 72);\n"
"font: 20pt \"Microsoft YaHei UI\";")
        self.lineEdit_9.setInputMethodHints(Qt.ImhDigitsOnly)

        self.horizontalLayout_72.addWidget(self.lineEdit_9)

        self.label_31 = QLabel(self.verticalGroupBox_9)
        self.label_31.setObjectName(u"label_31")

        self.horizontalLayout_72.addWidget(self.label_31)


        self.verticalLayout_31.addLayout(self.horizontalLayout_72)


        self.verticalLayout_33.addLayout(self.verticalLayout_31)

        self.label_104 = QLabel(self.verticalGroupBox_9)
        self.label_104.setObjectName(u"label_104")
        self.label_104.setFocusPolicy(Qt.NoFocus)
        self.label_104.setStyleSheet(u"font: 12pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(255, 0, 0);")
        self.label_104.setAlignment(Qt.AlignCenter)

        self.verticalLayout_33.addWidget(self.label_104)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_33.addItem(self.verticalSpacer_6)


        self.verticalLayout_53.addLayout(self.verticalLayout_33)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_14)

        self.btn_discharge = QPushButton(self.verticalGroupBox_9)
        self.btn_discharge.setObjectName(u"btn_discharge")
        self.btn_discharge.setMinimumSize(QSize(180, 60))
        self.btn_discharge.setMaximumSize(QSize(1000, 1000))
        self.btn_discharge.setLayoutDirection(Qt.LeftToRight)
        self.btn_discharge.setStyleSheet(u"background-color: rgb(52, 59, 72);\n"
"font: 20pt \"Microsoft YaHei UI\";")
        self.btn_discharge.setAutoDefault(False)

        self.horizontalLayout_24.addWidget(self.btn_discharge)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_13)

        self.horizontalLayout_24.setStretch(0, 1)
        self.horizontalLayout_24.setStretch(1, 2)
        self.horizontalLayout_24.setStretch(2, 1)

        self.verticalLayout_53.addLayout(self.horizontalLayout_24)

        self.label_101 = QLabel(self.verticalGroupBox_9)
        self.label_101.setObjectName(u"label_101")
        self.label_101.setFocusPolicy(Qt.NoFocus)
        self.label_101.setStyleSheet(u"font: 12pt \"\u5fae\u8f6f\u96c5\u9ed1\";")
        self.label_101.setAlignment(Qt.AlignCenter)

        self.verticalLayout_53.addWidget(self.label_101)

        self.verticalLayout_53.setStretch(0, 16)
        self.verticalLayout_53.setStretch(1, 4)
        self.verticalLayout_53.setStretch(2, 1)

        self.verticalLayout_54.addLayout(self.verticalLayout_53)


        self.horizontalLayout_19.addWidget(self.verticalGroupBox_9)

        self.horizontalLayout_19.setStretch(0, 1)
        self.horizontalLayout_19.setStretch(1, 1)

        self.verticalLayout_35.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout_34 = QVBoxLayout()
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_96 = QLabel(self.home)
        self.label_96.setObjectName(u"label_96")
        self.label_96.setFocusPolicy(Qt.NoFocus)
        self.label_96.setStyleSheet(u"font: 16pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_20.addWidget(self.label_96)

        self.label_97 = QLabel(self.home)
        self.label_97.setObjectName(u"label_97")
        self.label_97.setFocusPolicy(Qt.NoFocus)
        self.label_97.setStyleSheet(u"font: 16pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_97.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_20.addWidget(self.label_97)


        self.verticalLayout_34.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_98 = QLabel(self.home)
        self.label_98.setObjectName(u"label_98")
        self.label_98.setFocusPolicy(Qt.NoFocus)
        self.label_98.setStyleSheet(u"font: 16pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_21.addWidget(self.label_98)

        self.label_99 = QLabel(self.home)
        self.label_99.setObjectName(u"label_99")
        self.label_99.setFocusPolicy(Qt.NoFocus)
        self.label_99.setStyleSheet(u"font: 16pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_99.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_21.addWidget(self.label_99)

        self.horizontalLayout_21.setStretch(0, 11)
        self.horizontalLayout_21.setStretch(1, 4)

        self.verticalLayout_34.addLayout(self.horizontalLayout_21)


        self.horizontalLayout_22.addLayout(self.verticalLayout_34)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_7)

        self.label_3 = QLabel(self.home)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(130, 130))
        self.label_3.setMaximumSize(QSize(300, 300))
        self.label_3.setPixmap(QPixmap(u":/images/images/images/weixin-130130.png"))
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_22.addWidget(self.label_3)

        self.horizontalLayout_22.setStretch(0, 10)
        self.horizontalLayout_22.setStretch(1, 20)
        self.horizontalLayout_22.setStretch(2, 8)

        self.verticalLayout_35.addLayout(self.horizontalLayout_22)


        self.verticalLayout_36.addLayout(self.verticalLayout_35)

        self.stackedWidget.addWidget(self.home)
        self.widgets = QWidget()
        self.widgets.setObjectName(u"widgets")
        self.widgets.setStyleSheet(u"b")
        self.verticalLayout_42 = QVBoxLayout(self.widgets)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.verticalLayout_41 = QVBoxLayout()
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.label_29 = QLabel(self.widgets)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFocusPolicy(Qt.NoFocus)
        self.label_29.setLayoutDirection(Qt.LeftToRight)
        self.label_29.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(170, 0, 255);")
        self.label_29.setFrameShadow(QFrame.Plain)
        self.label_29.setAlignment(Qt.AlignCenter)

        self.verticalLayout_41.addWidget(self.label_29)

        self.horizontalLayout_44 = QHBoxLayout()
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_44.addItem(self.horizontalSpacer_3)

        self.verticalGroupBox_5 = QGroupBox(self.widgets)
        self.verticalGroupBox_5.setObjectName(u"verticalGroupBox_5")
        self.verticalGroupBox_5.setFont(font4)
        self.verticalGroupBox_5.setStyleSheet(u"font: 20pt \"Microsoft YaHei UI\";")
        self.verticalGroupBox_5.setAlignment(Qt.AlignCenter)
        self.verticalGroupBox_5.setFlat(False)
        self.verticalLayout_16 = QVBoxLayout(self.verticalGroupBox_5)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_7 = QLabel(self.verticalGroupBox_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFocusPolicy(Qt.NoFocus)
        self.label_7.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_9.addWidget(self.label_7)

        self.label_8 = QLabel(self.verticalGroupBox_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFocusPolicy(Qt.NoFocus)
        self.label_8.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_8)

        self.label_9 = QLabel(self.verticalGroupBox_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFocusPolicy(Qt.NoFocus)
        self.label_9.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_9.addWidget(self.label_9)

        self.label_11 = QLabel(self.verticalGroupBox_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFocusPolicy(Qt.NoFocus)
        self.label_11.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_11)

        self.label_10 = QLabel(self.verticalGroupBox_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFocusPolicy(Qt.NoFocus)
        self.label_10.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_9.addWidget(self.label_10)

        self.label_13 = QLabel(self.verticalGroupBox_5)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFocusPolicy(Qt.NoFocus)
        self.label_13.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_13)

        self.label_12 = QLabel(self.verticalGroupBox_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFocusPolicy(Qt.NoFocus)
        self.label_12.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_9.addWidget(self.label_12)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_14 = QLabel(self.verticalGroupBox_5)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFocusPolicy(Qt.NoFocus)
        self.label_14.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_11.addWidget(self.label_14)

        self.label_15 = QLabel(self.verticalGroupBox_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFocusPolicy(Qt.NoFocus)
        self.label_15.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_15)

        self.label_16 = QLabel(self.verticalGroupBox_5)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFocusPolicy(Qt.NoFocus)
        self.label_16.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_11.addWidget(self.label_16)

        self.label_17 = QLabel(self.verticalGroupBox_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFocusPolicy(Qt.NoFocus)
        self.label_17.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_17)

        self.label_18 = QLabel(self.verticalGroupBox_5)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFocusPolicy(Qt.NoFocus)
        self.label_18.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_11.addWidget(self.label_18)

        self.label_19 = QLabel(self.verticalGroupBox_5)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFocusPolicy(Qt.NoFocus)
        self.label_19.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_19)

        self.label_20 = QLabel(self.verticalGroupBox_5)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFocusPolicy(Qt.NoFocus)
        self.label_20.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_11.addWidget(self.label_20)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_21 = QLabel(self.verticalGroupBox_5)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFocusPolicy(Qt.NoFocus)
        self.label_21.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_28.addWidget(self.label_21)

        self.label_22 = QLabel(self.verticalGroupBox_5)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFocusPolicy(Qt.NoFocus)
        self.label_22.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_28.addWidget(self.label_22)

        self.label_23 = QLabel(self.verticalGroupBox_5)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFocusPolicy(Qt.NoFocus)
        self.label_23.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_28.addWidget(self.label_23)


        self.verticalLayout.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.label_24 = QLabel(self.verticalGroupBox_5)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFocusPolicy(Qt.NoFocus)
        self.label_24.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_30.addWidget(self.label_24)

        self.label_25 = QLabel(self.verticalGroupBox_5)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFocusPolicy(Qt.NoFocus)
        self.label_25.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_25.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_30.addWidget(self.label_25)

        self.label_26 = QLabel(self.verticalGroupBox_5)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFocusPolicy(Qt.NoFocus)
        self.label_26.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_30.addWidget(self.label_26)


        self.verticalLayout.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_27 = QLabel(self.verticalGroupBox_5)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFocusPolicy(Qt.NoFocus)
        self.label_27.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_31.addWidget(self.label_27)

        self.label_35 = QLabel(self.verticalGroupBox_5)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFocusPolicy(Qt.NoFocus)
        self.label_35.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_35.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_31.addWidget(self.label_35)

        self.label_36 = QLabel(self.verticalGroupBox_5)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFocusPolicy(Qt.NoFocus)
        self.label_36.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_31.addWidget(self.label_36)


        self.verticalLayout.addLayout(self.horizontalLayout_31)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.label_37 = QLabel(self.verticalGroupBox_5)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setFocusPolicy(Qt.NoFocus)
        self.label_37.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_32.addWidget(self.label_37)

        self.label_38 = QLabel(self.verticalGroupBox_5)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setFocusPolicy(Qt.NoFocus)
        self.label_38.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_38.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_32.addWidget(self.label_38)

        self.label_39 = QLabel(self.verticalGroupBox_5)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFocusPolicy(Qt.NoFocus)
        self.label_39.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_32.addWidget(self.label_39)


        self.verticalLayout.addLayout(self.horizontalLayout_32)


        self.verticalLayout_16.addLayout(self.verticalLayout)


        self.horizontalLayout_44.addWidget(self.verticalGroupBox_5)

        self.verticalGroupBox_6 = QGroupBox(self.widgets)
        self.verticalGroupBox_6.setObjectName(u"verticalGroupBox_6")
        self.verticalGroupBox_6.setFont(font4)
        self.verticalGroupBox_6.setStyleSheet(u"font: 20pt \"Microsoft YaHei UI\";")
        self.verticalGroupBox_6.setAlignment(Qt.AlignCenter)
        self.verticalGroupBox_6.setFlat(False)
        self.verticalLayout_17 = QVBoxLayout(self.verticalGroupBox_6)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_40 = QLabel(self.verticalGroupBox_6)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setFocusPolicy(Qt.NoFocus)
        self.label_40.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_12.addWidget(self.label_40)

        self.label_41 = QLabel(self.verticalGroupBox_6)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setFocusPolicy(Qt.NoFocus)
        self.label_41.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_41.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_41)

        self.label_42 = QLabel(self.verticalGroupBox_6)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setFocusPolicy(Qt.NoFocus)
        self.label_42.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_12.addWidget(self.label_42)


        self.verticalLayout_18.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.label_47 = QLabel(self.verticalGroupBox_6)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFocusPolicy(Qt.NoFocus)
        self.label_47.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_33.addWidget(self.label_47)

        self.label_48 = QLabel(self.verticalGroupBox_6)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFocusPolicy(Qt.NoFocus)
        self.label_48.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_48.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_33.addWidget(self.label_48)

        self.label_49 = QLabel(self.verticalGroupBox_6)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFocusPolicy(Qt.NoFocus)
        self.label_49.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_33.addWidget(self.label_49)


        self.verticalLayout_18.addLayout(self.horizontalLayout_33)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.label_54 = QLabel(self.verticalGroupBox_6)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setFocusPolicy(Qt.NoFocus)
        self.label_54.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_34.addWidget(self.label_54)

        self.label_55 = QLabel(self.verticalGroupBox_6)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setFocusPolicy(Qt.NoFocus)
        self.label_55.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_55.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_34.addWidget(self.label_55)

        self.label_56 = QLabel(self.verticalGroupBox_6)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setFocusPolicy(Qt.NoFocus)
        self.label_56.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_34.addWidget(self.label_56)


        self.verticalLayout_18.addLayout(self.horizontalLayout_34)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.label_57 = QLabel(self.verticalGroupBox_6)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setFocusPolicy(Qt.NoFocus)
        self.label_57.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_35.addWidget(self.label_57)

        self.label_58 = QLabel(self.verticalGroupBox_6)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setFocusPolicy(Qt.NoFocus)
        self.label_58.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_58.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_35.addWidget(self.label_58)

        self.label_59 = QLabel(self.verticalGroupBox_6)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setFocusPolicy(Qt.NoFocus)
        self.label_59.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_35.addWidget(self.label_59)


        self.verticalLayout_18.addLayout(self.horizontalLayout_35)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.label_60 = QLabel(self.verticalGroupBox_6)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setFocusPolicy(Qt.NoFocus)
        self.label_60.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_36.addWidget(self.label_60)

        self.label_61 = QLabel(self.verticalGroupBox_6)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setFocusPolicy(Qt.NoFocus)
        self.label_61.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_61.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_36.addWidget(self.label_61)

        self.label_62 = QLabel(self.verticalGroupBox_6)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setFocusPolicy(Qt.NoFocus)
        self.label_62.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_36.addWidget(self.label_62)


        self.verticalLayout_18.addLayout(self.horizontalLayout_36)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.label_63 = QLabel(self.verticalGroupBox_6)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setFocusPolicy(Qt.NoFocus)
        self.label_63.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_37.addWidget(self.label_63)

        self.label_64 = QLabel(self.verticalGroupBox_6)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setFocusPolicy(Qt.NoFocus)
        self.label_64.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_64.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_37.addWidget(self.label_64)

        self.label_65 = QLabel(self.verticalGroupBox_6)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setFocusPolicy(Qt.NoFocus)
        self.label_65.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_37.addWidget(self.label_65)


        self.verticalLayout_18.addLayout(self.horizontalLayout_37)


        self.verticalLayout_17.addLayout(self.verticalLayout_18)


        self.horizontalLayout_44.addWidget(self.verticalGroupBox_6)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_44.addItem(self.horizontalSpacer_4)

        self.horizontalLayout_44.setStretch(0, 1)
        self.horizontalLayout_44.setStretch(1, 4)
        self.horizontalLayout_44.setStretch(2, 4)
        self.horizontalLayout_44.setStretch(3, 1)

        self.verticalLayout_41.addLayout(self.horizontalLayout_44)

        self.horizontalLayout_69 = QHBoxLayout()
        self.horizontalLayout_69.setObjectName(u"horizontalLayout_69")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_69.addItem(self.horizontalSpacer_5)

        self.verticalGroupBox_7 = QGroupBox(self.widgets)
        self.verticalGroupBox_7.setObjectName(u"verticalGroupBox_7")
        self.verticalGroupBox_7.setFont(font4)
        self.verticalGroupBox_7.setStyleSheet(u"font: 20pt \"Microsoft YaHei UI\";")
        self.verticalGroupBox_7.setAlignment(Qt.AlignCenter)
        self.verticalGroupBox_7.setFlat(False)
        self.verticalLayout_38 = QVBoxLayout(self.verticalGroupBox_7)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.horizontalLayout_68 = QHBoxLayout()
        self.horizontalLayout_68.setObjectName(u"horizontalLayout_68")
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.label_43 = QLabel(self.verticalGroupBox_7)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setFocusPolicy(Qt.NoFocus)
        self.label_43.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_38.addWidget(self.label_43)

        self.label_44 = QLabel(self.verticalGroupBox_7)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFocusPolicy(Qt.NoFocus)
        self.label_44.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_44.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_38.addWidget(self.label_44)

        self.label_45 = QLabel(self.verticalGroupBox_7)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFocusPolicy(Qt.NoFocus)
        self.label_45.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_38.addWidget(self.label_45)


        self.verticalLayout_19.addLayout(self.horizontalLayout_38)

        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.label_50 = QLabel(self.verticalGroupBox_7)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFocusPolicy(Qt.NoFocus)
        self.label_50.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_39.addWidget(self.label_50)

        self.label_51 = QLabel(self.verticalGroupBox_7)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setFocusPolicy(Qt.NoFocus)
        self.label_51.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_51.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_39.addWidget(self.label_51)

        self.label_52 = QLabel(self.verticalGroupBox_7)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFocusPolicy(Qt.NoFocus)
        self.label_52.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_39.addWidget(self.label_52)


        self.verticalLayout_19.addLayout(self.horizontalLayout_39)

        self.horizontalLayout_56 = QHBoxLayout()
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.label_110 = QLabel(self.verticalGroupBox_7)
        self.label_110.setObjectName(u"label_110")
        self.label_110.setFocusPolicy(Qt.NoFocus)
        self.label_110.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_56.addWidget(self.label_110)

        self.label_111 = QLabel(self.verticalGroupBox_7)
        self.label_111.setObjectName(u"label_111")
        self.label_111.setFocusPolicy(Qt.NoFocus)
        self.label_111.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_111.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_56.addWidget(self.label_111)

        self.label_112 = QLabel(self.verticalGroupBox_7)
        self.label_112.setObjectName(u"label_112")
        self.label_112.setFocusPolicy(Qt.NoFocus)
        self.label_112.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_56.addWidget(self.label_112)


        self.verticalLayout_19.addLayout(self.horizontalLayout_56)

        self.horizontalLayout_57 = QHBoxLayout()
        self.horizontalLayout_57.setObjectName(u"horizontalLayout_57")
        self.label_113 = QLabel(self.verticalGroupBox_7)
        self.label_113.setObjectName(u"label_113")
        self.label_113.setFocusPolicy(Qt.NoFocus)
        self.label_113.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_57.addWidget(self.label_113)

        self.label_114 = QLabel(self.verticalGroupBox_7)
        self.label_114.setObjectName(u"label_114")
        self.label_114.setFocusPolicy(Qt.NoFocus)
        self.label_114.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_114.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_57.addWidget(self.label_114)

        self.label_115 = QLabel(self.verticalGroupBox_7)
        self.label_115.setObjectName(u"label_115")
        self.label_115.setFocusPolicy(Qt.NoFocus)
        self.label_115.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_57.addWidget(self.label_115)


        self.verticalLayout_19.addLayout(self.horizontalLayout_57)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.label_81 = QLabel(self.verticalGroupBox_7)
        self.label_81.setObjectName(u"label_81")
        self.label_81.setFocusPolicy(Qt.NoFocus)
        self.label_81.setStyleSheet(u"font: 18pt \"\u5fae\u8f6f\u96c5\u9ed1\";")
        self.label_81.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_25.addWidget(self.label_81)

        self.label_144 = QLabel(self.verticalGroupBox_7)
        self.label_144.setObjectName(u"label_144")
        self.label_144.setFocusPolicy(Qt.NoFocus)
        self.label_144.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_144.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_25.addWidget(self.label_144)

        self.label_145 = QLabel(self.verticalGroupBox_7)
        self.label_145.setObjectName(u"label_145")
        self.label_145.setFocusPolicy(Qt.NoFocus)
        self.label_145.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_25.addWidget(self.label_145)


        self.verticalLayout_19.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.label_66 = QLabel(self.verticalGroupBox_7)
        self.label_66.setObjectName(u"label_66")
        self.label_66.setFocusPolicy(Qt.NoFocus)
        self.label_66.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_40.addWidget(self.label_66)

        self.label_67 = QLabel(self.verticalGroupBox_7)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setFocusPolicy(Qt.NoFocus)
        self.label_67.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_67.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_40.addWidget(self.label_67)


        self.verticalLayout_19.addLayout(self.horizontalLayout_40)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_41 = QHBoxLayout()
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.label_69 = QLabel(self.verticalGroupBox_7)
        self.label_69.setObjectName(u"label_69")
        self.label_69.setFocusPolicy(Qt.NoFocus)
        self.label_69.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_41.addWidget(self.label_69)

        self.label_70 = QLabel(self.verticalGroupBox_7)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setFocusPolicy(Qt.NoFocus)
        self.label_70.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_70.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_41.addWidget(self.label_70)

        self.label_71 = QLabel(self.verticalGroupBox_7)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setFocusPolicy(Qt.NoFocus)
        self.label_71.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_41.addWidget(self.label_71)


        self.horizontalLayout_26.addLayout(self.horizontalLayout_41)

        self.horizontalLayout_58 = QHBoxLayout()
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.label_116 = QLabel(self.verticalGroupBox_7)
        self.label_116.setObjectName(u"label_116")
        self.label_116.setFocusPolicy(Qt.NoFocus)
        self.label_116.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_58.addWidget(self.label_116)

        self.label_117 = QLabel(self.verticalGroupBox_7)
        self.label_117.setObjectName(u"label_117")
        self.label_117.setFocusPolicy(Qt.NoFocus)
        self.label_117.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_117.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_58.addWidget(self.label_117)


        self.horizontalLayout_26.addLayout(self.horizontalLayout_58)


        self.verticalLayout_19.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_42 = QHBoxLayout()
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.label_72 = QLabel(self.verticalGroupBox_7)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setFocusPolicy(Qt.NoFocus)
        self.label_72.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_42.addWidget(self.label_72)

        self.label_73 = QLabel(self.verticalGroupBox_7)
        self.label_73.setObjectName(u"label_73")
        self.label_73.setFocusPolicy(Qt.NoFocus)
        self.label_73.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_73.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_42.addWidget(self.label_73)

        self.label_74 = QLabel(self.verticalGroupBox_7)
        self.label_74.setObjectName(u"label_74")
        self.label_74.setFocusPolicy(Qt.NoFocus)
        self.label_74.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_42.addWidget(self.label_74)


        self.horizontalLayout_27.addLayout(self.horizontalLayout_42)

        self.horizontalLayout_63 = QHBoxLayout()
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.label_118 = QLabel(self.verticalGroupBox_7)
        self.label_118.setObjectName(u"label_118")
        self.label_118.setFocusPolicy(Qt.NoFocus)
        self.label_118.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_63.addWidget(self.label_118)

        self.label_119 = QLabel(self.verticalGroupBox_7)
        self.label_119.setObjectName(u"label_119")
        self.label_119.setFocusPolicy(Qt.NoFocus)
        self.label_119.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_119.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_63.addWidget(self.label_119)


        self.horizontalLayout_27.addLayout(self.horizontalLayout_63)


        self.verticalLayout_19.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_43 = QHBoxLayout()
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.label_75 = QLabel(self.verticalGroupBox_7)
        self.label_75.setObjectName(u"label_75")
        self.label_75.setFocusPolicy(Qt.NoFocus)
        self.label_75.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_43.addWidget(self.label_75)

        self.label_76 = QLabel(self.verticalGroupBox_7)
        self.label_76.setObjectName(u"label_76")
        self.label_76.setFocusPolicy(Qt.NoFocus)
        self.label_76.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_76.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_43.addWidget(self.label_76)

        self.label_77 = QLabel(self.verticalGroupBox_7)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setFocusPolicy(Qt.NoFocus)
        self.label_77.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_43.addWidget(self.label_77)


        self.horizontalLayout_29.addLayout(self.horizontalLayout_43)

        self.horizontalLayout_64 = QHBoxLayout()
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.label_120 = QLabel(self.verticalGroupBox_7)
        self.label_120.setObjectName(u"label_120")
        self.label_120.setFocusPolicy(Qt.NoFocus)
        self.label_120.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_64.addWidget(self.label_120)

        self.label_121 = QLabel(self.verticalGroupBox_7)
        self.label_121.setObjectName(u"label_121")
        self.label_121.setFocusPolicy(Qt.NoFocus)
        self.label_121.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_121.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_64.addWidget(self.label_121)


        self.horizontalLayout_29.addLayout(self.horizontalLayout_64)


        self.verticalLayout_19.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_45 = QHBoxLayout()
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.label_78 = QLabel(self.verticalGroupBox_7)
        self.label_78.setObjectName(u"label_78")
        self.label_78.setFocusPolicy(Qt.NoFocus)
        self.label_78.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_45.addWidget(self.label_78)

        self.label_79 = QLabel(self.verticalGroupBox_7)
        self.label_79.setObjectName(u"label_79")
        self.label_79.setFocusPolicy(Qt.NoFocus)
        self.label_79.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_79.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_45.addWidget(self.label_79)

        self.label_80 = QLabel(self.verticalGroupBox_7)
        self.label_80.setObjectName(u"label_80")
        self.label_80.setFocusPolicy(Qt.NoFocus)
        self.label_80.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_45.addWidget(self.label_80)


        self.verticalLayout_19.addLayout(self.horizontalLayout_45)


        self.horizontalLayout_68.addLayout(self.verticalLayout_19)

        self.verticalLayout_37 = QVBoxLayout()
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.horizontalLayout_46 = QHBoxLayout()
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.label_46 = QLabel(self.verticalGroupBox_7)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setFocusPolicy(Qt.NoFocus)
        self.label_46.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_46.addWidget(self.label_46)

        self.label_53 = QLabel(self.verticalGroupBox_7)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setFocusPolicy(Qt.NoFocus)
        self.label_53.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_53.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_46.addWidget(self.label_53)


        self.verticalLayout_37.addLayout(self.horizontalLayout_46)

        self.horizontalLayout_47 = QHBoxLayout()
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.label_68 = QLabel(self.verticalGroupBox_7)
        self.label_68.setObjectName(u"label_68")
        self.label_68.setFocusPolicy(Qt.NoFocus)
        self.label_68.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_47.addWidget(self.label_68)

        self.label_82 = QLabel(self.verticalGroupBox_7)
        self.label_82.setObjectName(u"label_82")
        self.label_82.setFocusPolicy(Qt.NoFocus)
        self.label_82.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_82.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_47.addWidget(self.label_82)

        self.label_95 = QLabel(self.verticalGroupBox_7)
        self.label_95.setObjectName(u"label_95")
        self.label_95.setFocusPolicy(Qt.NoFocus)
        self.label_95.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_47.addWidget(self.label_95)


        self.verticalLayout_37.addLayout(self.horizontalLayout_47)

        self.horizontalLayout_48 = QHBoxLayout()
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.label_84 = QLabel(self.verticalGroupBox_7)
        self.label_84.setObjectName(u"label_84")
        self.label_84.setFocusPolicy(Qt.NoFocus)
        self.label_84.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_48.addWidget(self.label_84)

        self.label_85 = QLabel(self.verticalGroupBox_7)
        self.label_85.setObjectName(u"label_85")
        self.label_85.setFocusPolicy(Qt.NoFocus)
        self.label_85.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_85.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_48.addWidget(self.label_85)

        self.label_86 = QLabel(self.verticalGroupBox_7)
        self.label_86.setObjectName(u"label_86")
        self.label_86.setFocusPolicy(Qt.NoFocus)
        self.label_86.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_48.addWidget(self.label_86)


        self.verticalLayout_37.addLayout(self.horizontalLayout_48)

        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.label_83 = QLabel(self.verticalGroupBox_7)
        self.label_83.setObjectName(u"label_83")
        self.label_83.setFocusPolicy(Qt.NoFocus)
        self.label_83.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_49.addWidget(self.label_83)

        self.label_87 = QLabel(self.verticalGroupBox_7)
        self.label_87.setObjectName(u"label_87")
        self.label_87.setFocusPolicy(Qt.NoFocus)
        self.label_87.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_87.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_49.addWidget(self.label_87)

        self.label_88 = QLabel(self.verticalGroupBox_7)
        self.label_88.setObjectName(u"label_88")
        self.label_88.setFocusPolicy(Qt.NoFocus)
        self.label_88.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_49.addWidget(self.label_88)


        self.verticalLayout_37.addLayout(self.horizontalLayout_49)

        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.label_89 = QLabel(self.verticalGroupBox_7)
        self.label_89.setObjectName(u"label_89")
        self.label_89.setFocusPolicy(Qt.NoFocus)
        self.label_89.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_50.addWidget(self.label_89)

        self.label_90 = QLabel(self.verticalGroupBox_7)
        self.label_90.setObjectName(u"label_90")
        self.label_90.setFocusPolicy(Qt.NoFocus)
        self.label_90.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_90.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_50.addWidget(self.label_90)


        self.verticalLayout_37.addLayout(self.horizontalLayout_50)

        self.horizontalLayout_51 = QHBoxLayout()
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.label_91 = QLabel(self.verticalGroupBox_7)
        self.label_91.setObjectName(u"label_91")
        self.label_91.setFocusPolicy(Qt.NoFocus)
        self.label_91.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_51.addWidget(self.label_91)

        self.label_92 = QLabel(self.verticalGroupBox_7)
        self.label_92.setObjectName(u"label_92")
        self.label_92.setFocusPolicy(Qt.NoFocus)
        self.label_92.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_92.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_51.addWidget(self.label_92)


        self.verticalLayout_37.addLayout(self.horizontalLayout_51)

        self.horizontalLayout_52 = QHBoxLayout()
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.label_93 = QLabel(self.verticalGroupBox_7)
        self.label_93.setObjectName(u"label_93")
        self.label_93.setFocusPolicy(Qt.NoFocus)
        self.label_93.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_52.addWidget(self.label_93)

        self.label_94 = QLabel(self.verticalGroupBox_7)
        self.label_94.setObjectName(u"label_94")
        self.label_94.setFocusPolicy(Qt.NoFocus)
        self.label_94.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_94.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_52.addWidget(self.label_94)


        self.verticalLayout_37.addLayout(self.horizontalLayout_52)

        self.horizontalLayout_65 = QHBoxLayout()
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.label_122 = QLabel(self.verticalGroupBox_7)
        self.label_122.setObjectName(u"label_122")
        self.label_122.setFocusPolicy(Qt.NoFocus)
        self.label_122.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_65.addWidget(self.label_122)

        self.label_123 = QLabel(self.verticalGroupBox_7)
        self.label_123.setObjectName(u"label_123")
        self.label_123.setFocusPolicy(Qt.NoFocus)
        self.label_123.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_123.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_65.addWidget(self.label_123)

        self.label_137 = QLabel(self.verticalGroupBox_7)
        self.label_137.setObjectName(u"label_137")
        self.label_137.setFocusPolicy(Qt.NoFocus)
        self.label_137.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_65.addWidget(self.label_137)


        self.verticalLayout_37.addLayout(self.horizontalLayout_65)

        self.horizontalLayout_66 = QHBoxLayout()
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.label_138 = QLabel(self.verticalGroupBox_7)
        self.label_138.setObjectName(u"label_138")
        self.label_138.setFocusPolicy(Qt.NoFocus)
        self.label_138.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_66.addWidget(self.label_138)

        self.label_139 = QLabel(self.verticalGroupBox_7)
        self.label_139.setObjectName(u"label_139")
        self.label_139.setFocusPolicy(Qt.NoFocus)
        self.label_139.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_139.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_66.addWidget(self.label_139)

        self.label_140 = QLabel(self.verticalGroupBox_7)
        self.label_140.setObjectName(u"label_140")
        self.label_140.setFocusPolicy(Qt.NoFocus)
        self.label_140.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_66.addWidget(self.label_140)


        self.verticalLayout_37.addLayout(self.horizontalLayout_66)

        self.horizontalLayout_67 = QHBoxLayout()
        self.horizontalLayout_67.setObjectName(u"horizontalLayout_67")
        self.label_141 = QLabel(self.verticalGroupBox_7)
        self.label_141.setObjectName(u"label_141")
        self.label_141.setFocusPolicy(Qt.NoFocus)
        self.label_141.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_67.addWidget(self.label_141)

        self.label_142 = QLabel(self.verticalGroupBox_7)
        self.label_142.setObjectName(u"label_142")
        self.label_142.setFocusPolicy(Qt.NoFocus)
        self.label_142.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"color: rgb(0, 0, 255);")
        self.label_142.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_67.addWidget(self.label_142)

        self.label_143 = QLabel(self.verticalGroupBox_7)
        self.label_143.setObjectName(u"label_143")
        self.label_143.setFocusPolicy(Qt.NoFocus)
        self.label_143.setStyleSheet(u"font: 20pt \"\u5fae\u8f6f\u96c5\u9ed1\";")

        self.horizontalLayout_67.addWidget(self.label_143)


        self.verticalLayout_37.addLayout(self.horizontalLayout_67)


        self.horizontalLayout_68.addLayout(self.verticalLayout_37)


        self.verticalLayout_38.addLayout(self.horizontalLayout_68)


        self.horizontalLayout_69.addWidget(self.verticalGroupBox_7)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_69.addItem(self.horizontalSpacer_6)

        self.horizontalLayout_69.setStretch(0, 1)
        self.horizontalLayout_69.setStretch(1, 8)
        self.horizontalLayout_69.setStretch(2, 1)

        self.verticalLayout_41.addLayout(self.horizontalLayout_69)

        self.horizontalLayout_62 = QHBoxLayout()
        self.horizontalLayout_62.setObjectName(u"horizontalLayout_62")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_62.addItem(self.horizontalSpacer_8)

        self.verticalGroupBox_10 = QGroupBox(self.widgets)
        self.verticalGroupBox_10.setObjectName(u"verticalGroupBox_10")
        font5 = QFont()
        font5.setFamilies([u"Microsoft YaHei UI"])
        font5.setPointSize(16)
        font5.setBold(False)
        font5.setItalic(False)
        self.verticalGroupBox_10.setFont(font5)
        self.verticalGroupBox_10.setStyleSheet(u"font: 16pt \"Microsoft YaHei UI\";")
        self.verticalGroupBox_10.setAlignment(Qt.AlignCenter)
        self.verticalGroupBox_10.setFlat(False)
        self.verticalLayout_40 = QVBoxLayout(self.verticalGroupBox_10)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.horizontalLayout_61 = QHBoxLayout()
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.verticalLayout_39 = QVBoxLayout()
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.horizontalLayout_59 = QHBoxLayout()
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.label_124 = QLabel(self.verticalGroupBox_10)
        self.label_124.setObjectName(u"label_124")
        self.label_124.setFocusPolicy(Qt.NoFocus)
        self.label_124.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_59.addWidget(self.label_124)

        self.label_125 = QLabel(self.verticalGroupBox_10)
        self.label_125.setObjectName(u"label_125")
        self.label_125.setFocusPolicy(Qt.NoFocus)
        self.label_125.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";\n"
"color: rgb(0, 0, 255);")
        self.label_125.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_59.addWidget(self.label_125)

        self.label_126 = QLabel(self.verticalGroupBox_10)
        self.label_126.setObjectName(u"label_126")
        self.label_126.setFocusPolicy(Qt.NoFocus)
        self.label_126.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_59.addWidget(self.label_126)

        self.label_127 = QLabel(self.verticalGroupBox_10)
        self.label_127.setObjectName(u"label_127")
        self.label_127.setFocusPolicy(Qt.NoFocus)
        self.label_127.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";\n"
"color: rgb(0, 0, 255);")
        self.label_127.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_59.addWidget(self.label_127)

        self.label_131 = QLabel(self.verticalGroupBox_10)
        self.label_131.setObjectName(u"label_131")
        self.label_131.setFocusPolicy(Qt.NoFocus)
        self.label_131.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_59.addWidget(self.label_131)

        self.label_154 = QLabel(self.verticalGroupBox_10)
        self.label_154.setObjectName(u"label_154")
        self.label_154.setFocusPolicy(Qt.NoFocus)
        self.label_154.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";\n"
"color: rgb(0, 0, 255);")
        self.label_154.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_59.addWidget(self.label_154)

        self.label_129 = QLabel(self.verticalGroupBox_10)
        self.label_129.setObjectName(u"label_129")
        self.label_129.setFocusPolicy(Qt.NoFocus)
        self.label_129.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_59.addWidget(self.label_129)

        self.label_128 = QLabel(self.verticalGroupBox_10)
        self.label_128.setObjectName(u"label_128")
        self.label_128.setFocusPolicy(Qt.NoFocus)
        self.label_128.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";\n"
"color: rgb(0, 0, 255);")
        self.label_128.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_59.addWidget(self.label_128)

        self.label_132 = QLabel(self.verticalGroupBox_10)
        self.label_132.setObjectName(u"label_132")
        self.label_132.setFocusPolicy(Qt.NoFocus)
        self.label_132.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_59.addWidget(self.label_132)

        self.label_130 = QLabel(self.verticalGroupBox_10)
        self.label_130.setObjectName(u"label_130")
        self.label_130.setFocusPolicy(Qt.NoFocus)
        self.label_130.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";\n"
"color: rgb(0, 0, 255);")
        self.label_130.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_59.addWidget(self.label_130)


        self.verticalLayout_39.addLayout(self.horizontalLayout_59)

        self.horizontalLayout_60 = QHBoxLayout()
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.label_133 = QLabel(self.verticalGroupBox_10)
        self.label_133.setObjectName(u"label_133")
        self.label_133.setFocusPolicy(Qt.NoFocus)
        self.label_133.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_60.addWidget(self.label_133)

        self.label_134 = QLabel(self.verticalGroupBox_10)
        self.label_134.setObjectName(u"label_134")
        self.label_134.setFocusPolicy(Qt.NoFocus)
        self.label_134.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";\n"
"color: rgb(0, 0, 255);")
        self.label_134.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_60.addWidget(self.label_134)

        self.label_135 = QLabel(self.verticalGroupBox_10)
        self.label_135.setObjectName(u"label_135")
        self.label_135.setFocusPolicy(Qt.NoFocus)
        self.label_135.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_60.addWidget(self.label_135)

        self.label_136 = QLabel(self.verticalGroupBox_10)
        self.label_136.setObjectName(u"label_136")
        self.label_136.setFocusPolicy(Qt.NoFocus)
        self.label_136.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";\n"
"color: rgb(0, 0, 255);")
        self.label_136.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_60.addWidget(self.label_136)

        self.label_150 = QLabel(self.verticalGroupBox_10)
        self.label_150.setObjectName(u"label_150")
        self.label_150.setFocusPolicy(Qt.NoFocus)
        self.label_150.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_60.addWidget(self.label_150)

        self.label_151 = QLabel(self.verticalGroupBox_10)
        self.label_151.setObjectName(u"label_151")
        self.label_151.setFocusPolicy(Qt.NoFocus)
        self.label_151.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";\n"
"color: rgb(0, 0, 255);")
        self.label_151.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_60.addWidget(self.label_151)

        self.label_152 = QLabel(self.verticalGroupBox_10)
        self.label_152.setObjectName(u"label_152")
        self.label_152.setFocusPolicy(Qt.NoFocus)
        self.label_152.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_60.addWidget(self.label_152)

        self.label_153 = QLabel(self.verticalGroupBox_10)
        self.label_153.setObjectName(u"label_153")
        self.label_153.setFocusPolicy(Qt.NoFocus)
        self.label_153.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";\n"
"color: rgb(0, 0, 255);")
        self.label_153.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_60.addWidget(self.label_153)

        self.label_155 = QLabel(self.verticalGroupBox_10)
        self.label_155.setObjectName(u"label_155")
        self.label_155.setFocusPolicy(Qt.NoFocus)
        self.label_155.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_60.addWidget(self.label_155)

        self.label_156 = QLabel(self.verticalGroupBox_10)
        self.label_156.setObjectName(u"label_156")
        self.label_156.setFocusPolicy(Qt.NoFocus)
        self.label_156.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";\n"
"color: rgb(0, 0, 255);")
        self.label_156.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_60.addWidget(self.label_156)


        self.verticalLayout_39.addLayout(self.horizontalLayout_60)


        self.horizontalLayout_61.addLayout(self.verticalLayout_39)

        self.horizontalLayout_61.setStretch(0, 8)

        self.verticalLayout_40.addLayout(self.horizontalLayout_61)


        self.horizontalLayout_62.addWidget(self.verticalGroupBox_10)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_62.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_62.setStretch(0, 1)
        self.horizontalLayout_62.setStretch(1, 8)
        self.horizontalLayout_62.setStretch(2, 1)

        self.verticalLayout_41.addLayout(self.horizontalLayout_62)


        self.verticalLayout_42.addLayout(self.verticalLayout_41)

        self.stackedWidget.addWidget(self.widgets)
        self.new_page = QWidget()
        self.new_page.setObjectName(u"new_page")
        self.horizontalLayout_16 = QHBoxLayout(self.new_page)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")

        self.verticalLayout_15.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setSpacing(6)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout_27.setContentsMargins(0, -1, 0, 0)
        self.formGroupBox = QGroupBox(self.new_page)
        self.formGroupBox.setObjectName(u"formGroupBox")
        self.formLayout = QFormLayout(self.formGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.s1__lb_1 = QLabel(self.formGroupBox)
        self.s1__lb_1.setObjectName(u"s1__lb_1")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.s1__lb_1)

        self.s1__box_1 = QPushButton(self.formGroupBox)
        self.s1__box_1.setObjectName(u"s1__box_1")
        self.s1__box_1.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.s1__box_1.setAutoRepeatInterval(100)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.s1__box_1)

        self.s1__lb_2 = QLabel(self.formGroupBox)
        self.s1__lb_2.setObjectName(u"s1__lb_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.s1__lb_2)

        self.s1__box_2 = QComboBox(self.formGroupBox)
        self.s1__box_2.setObjectName(u"s1__box_2")
        self.s1__box_2.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.s1__box_2)

        self.s1__lb_3 = QLabel(self.formGroupBox)
        self.s1__lb_3.setObjectName(u"s1__lb_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.s1__lb_3)

        self.s1__box_3 = QComboBox(self.formGroupBox)
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.setObjectName(u"s1__box_3")
        self.s1__box_3.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.s1__box_3)

        self.s1__lb_4 = QLabel(self.formGroupBox)
        self.s1__lb_4.setObjectName(u"s1__lb_4")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.s1__lb_4)

        self.s1__box_4 = QComboBox(self.formGroupBox)
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.s1__box_4.setObjectName(u"s1__box_4")
        self.s1__box_4.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.s1__box_4)

        self.s1__lb_5 = QLabel(self.formGroupBox)
        self.s1__lb_5.setObjectName(u"s1__lb_5")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.s1__lb_5)

        self.s1__box_5 = QComboBox(self.formGroupBox)
        self.s1__box_5.addItem("")
        self.s1__box_5.setObjectName(u"s1__box_5")
        self.s1__box_5.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.s1__box_5)

        self.open_button = QPushButton(self.formGroupBox)
        self.open_button.setObjectName(u"open_button")
        self.open_button.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout.setWidget(7, QFormLayout.SpanningRole, self.open_button)

        self.close_button = QPushButton(self.formGroupBox)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout.setWidget(8, QFormLayout.SpanningRole, self.close_button)

        self.s1__lb_6 = QLabel(self.formGroupBox)
        self.s1__lb_6.setObjectName(u"s1__lb_6")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.s1__lb_6)

        self.s1__box_6 = QComboBox(self.formGroupBox)
        self.s1__box_6.addItem("")
        self.s1__box_6.setObjectName(u"s1__box_6")
        self.s1__box_6.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.s1__box_6)

        self.state_label = QLabel(self.formGroupBox)
        self.state_label.setObjectName(u"state_label")
        self.state_label.setStyleSheet(u"color: rgb(0, 85, 255);")
        self.state_label.setTextFormat(Qt.AutoText)
        self.state_label.setScaledContents(True)
        self.state_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.state_label)


        self.verticalLayout_27.addWidget(self.formGroupBox)

        self.formGroupBox_2 = QGroupBox(self.new_page)
        self.formGroupBox_2.setObjectName(u"formGroupBox_2")
        self.formLayout_2 = QFormLayout(self.formGroupBox_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(10)
        self.formLayout_2.setVerticalSpacing(10)
        self.formLayout_2.setContentsMargins(10, 10, 10, 10)
        self.label = QLabel(self.formGroupBox_2)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.formGroupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_2 = QLineEdit(self.formGroupBox_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.lineEdit_2)

        self.lineEdit_4 = QLineEdit(self.formGroupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.lineEdit_4)


        self.verticalLayout_27.addWidget(self.formGroupBox_2)


        self.horizontalLayout_14.addLayout(self.verticalLayout_27)

        self.verticalLayout_28 = QVBoxLayout()
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalGroupBox = QGroupBox(self.new_page)
        self.verticalGroupBox.setObjectName(u"verticalGroupBox")
        self.verticalLayout_23 = QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(10, 10, 10, 10)
        self.s2__receive_text = QTextBrowser(self.verticalGroupBox)
        self.s2__receive_text.setObjectName(u"s2__receive_text")

        self.verticalLayout_23.addWidget(self.s2__receive_text)


        self.horizontalLayout_7.addWidget(self.verticalGroupBox)

        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_24.addItem(self.verticalSpacer_4)

        self.hex_receive = QCheckBox(self.new_page)
        self.hex_receive.setObjectName(u"hex_receive")

        self.verticalLayout_24.addWidget(self.hex_receive)

        self.s2__clear_button = QPushButton(self.new_page)
        self.s2__clear_button.setObjectName(u"s2__clear_button")
        self.s2__clear_button.setAutoFillBackground(False)
        self.s2__clear_button.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.verticalLayout_24.addWidget(self.s2__clear_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_24.addItem(self.verticalSpacer)


        self.horizontalLayout_7.addLayout(self.verticalLayout_24)


        self.verticalLayout_28.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalGroupBox_2 = QGroupBox(self.new_page)
        self.verticalGroupBox_2.setObjectName(u"verticalGroupBox_2")
        self.verticalLayout_20 = QVBoxLayout(self.verticalGroupBox_2)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(10, 10, 10, 10)
        self.s3__send_text = QTextEdit(self.verticalGroupBox_2)
        self.s3__send_text.setObjectName(u"s3__send_text")

        self.verticalLayout_20.addWidget(self.s3__send_text)


        self.verticalLayout_26.addWidget(self.verticalGroupBox_2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.timer_send_cb = QCheckBox(self.new_page)
        self.timer_send_cb.setObjectName(u"timer_send_cb")

        self.horizontalLayout_10.addWidget(self.timer_send_cb)

        self.lineEdit_3 = QLineEdit(self.new_page)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.lineEdit_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.lineEdit_3)

        self.dw = QLabel(self.new_page)
        self.dw.setObjectName(u"dw")

        self.horizontalLayout_10.addWidget(self.dw)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer)

        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 1)
        self.horizontalLayout_10.setStretch(2, 1)
        self.horizontalLayout_10.setStretch(3, 4)

        self.verticalLayout_26.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_13.addLayout(self.verticalLayout_26)

        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_2)

        self.hex_send = QCheckBox(self.new_page)
        self.hex_send.setObjectName(u"hex_send")

        self.verticalLayout_25.addWidget(self.hex_send)

        self.s3__send_button = QPushButton(self.new_page)
        self.s3__send_button.setObjectName(u"s3__send_button")
        self.s3__send_button.setAutoFillBackground(False)
        self.s3__send_button.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.verticalLayout_25.addWidget(self.s3__send_button)

        self.s3__clear_button = QPushButton(self.new_page)
        self.s3__clear_button.setObjectName(u"s3__clear_button")
        self.s3__clear_button.setAutoFillBackground(False)
        self.s3__clear_button.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.verticalLayout_25.addWidget(self.s3__clear_button)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_3)


        self.horizontalLayout_13.addLayout(self.verticalLayout_25)


        self.verticalLayout_28.addLayout(self.horizontalLayout_13)


        self.horizontalLayout_14.addLayout(self.verticalLayout_28)

        self.horizontalLayout_14.setStretch(0, 1)
        self.horizontalLayout_14.setStretch(1, 5)

        self.verticalLayout_15.addLayout(self.horizontalLayout_14)


        self.horizontalLayout_16.addLayout(self.verticalLayout_15)

        self.stackedWidget.addWidget(self.new_page)
        self.can_page = QWidget()
        self.can_page.setObjectName(u"can_page")
        self.verticalLayout_52 = QVBoxLayout(self.can_page)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.verticalLayout_43 = QVBoxLayout()
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.horizontalLayout_53 = QHBoxLayout()
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")

        self.verticalLayout_43.addLayout(self.horizontalLayout_53)

        self.horizontalLayout_54 = QHBoxLayout()
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.verticalLayout_44 = QVBoxLayout()
        self.verticalLayout_44.setSpacing(6)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.verticalLayout_44.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout_44.setContentsMargins(0, -1, 0, 0)
        self.formGroupBox_3 = QGroupBox(self.can_page)
        self.formGroupBox_3.setObjectName(u"formGroupBox_3")
        self.formLayout_3 = QFormLayout(self.formGroupBox_3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setHorizontalSpacing(10)
        self.formLayout_3.setVerticalSpacing(10)
        self.formLayout_3.setContentsMargins(10, 10, 10, 10)
        self.s1__lb_7 = QLabel(self.formGroupBox_3)
        self.s1__lb_7.setObjectName(u"s1__lb_7")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.s1__lb_7)

        self.s1__box_7 = QPushButton(self.formGroupBox_3)
        self.s1__box_7.setObjectName(u"s1__box_7")
        self.s1__box_7.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.s1__box_7.setAutoRepeatInterval(100)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.s1__box_7)

        self.s1__lb_8 = QLabel(self.formGroupBox_3)
        self.s1__lb_8.setObjectName(u"s1__lb_8")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.s1__lb_8)

        self.s1__box_8 = QComboBox(self.formGroupBox_3)
        self.s1__box_8.setObjectName(u"s1__box_8")
        self.s1__box_8.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.s1__box_8)

        self.s1__lb_9 = QLabel(self.formGroupBox_3)
        self.s1__lb_9.setObjectName(u"s1__lb_9")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.s1__lb_9)

        self.s1__box_9 = QComboBox(self.formGroupBox_3)
        self.s1__box_9.addItem("")
        self.s1__box_9.addItem("")
        self.s1__box_9.setObjectName(u"s1__box_9")
        self.s1__box_9.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.s1__box_9)

        self.s1__lb_10 = QLabel(self.formGroupBox_3)
        self.s1__lb_10.setObjectName(u"s1__lb_10")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.s1__lb_10)

        self.s1__box_10 = QComboBox(self.formGroupBox_3)
        self.s1__box_10.addItem("")
        self.s1__box_10.addItem("")
        self.s1__box_10.setObjectName(u"s1__box_10")
        self.s1__box_10.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.s1__box_10)

        self.s1__lb_11 = QLabel(self.formGroupBox_3)
        self.s1__lb_11.setObjectName(u"s1__lb_11")

        self.formLayout_3.setWidget(5, QFormLayout.LabelRole, self.s1__lb_11)

        self.s1__box_11 = QComboBox(self.formGroupBox_3)
        self.s1__box_11.setObjectName(u"s1__box_11")
        self.s1__box_11.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.s1__box_11)

        self.open_button_2 = QPushButton(self.formGroupBox_3)
        self.open_button_2.setObjectName(u"open_button_2")
        self.open_button_2.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_3.setWidget(7, QFormLayout.SpanningRole, self.open_button_2)

        self.close_button_2 = QPushButton(self.formGroupBox_3)
        self.close_button_2.setObjectName(u"close_button_2")
        self.close_button_2.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_3.setWidget(8, QFormLayout.SpanningRole, self.close_button_2)

        self.s1__lb_12 = QLabel(self.formGroupBox_3)
        self.s1__lb_12.setObjectName(u"s1__lb_12")

        self.formLayout_3.setWidget(6, QFormLayout.LabelRole, self.s1__lb_12)

        self.s1__box_12 = QComboBox(self.formGroupBox_3)
        self.s1__box_12.setObjectName(u"s1__box_12")
        self.s1__box_12.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_3.setWidget(6, QFormLayout.FieldRole, self.s1__box_12)

        self.state_label_2 = QLabel(self.formGroupBox_3)
        self.state_label_2.setObjectName(u"state_label_2")
        self.state_label_2.setStyleSheet(u"color: rgb(0, 85, 255);")
        self.state_label_2.setTextFormat(Qt.AutoText)
        self.state_label_2.setScaledContents(True)
        self.state_label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_3.setWidget(2, QFormLayout.SpanningRole, self.state_label_2)


        self.verticalLayout_44.addWidget(self.formGroupBox_3)

        self.formGroupBox_4 = QGroupBox(self.can_page)
        self.formGroupBox_4.setObjectName(u"formGroupBox_4")
        self.formLayout_4 = QFormLayout(self.formGroupBox_4)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setHorizontalSpacing(10)
        self.formLayout_4.setVerticalSpacing(10)
        self.formLayout_4.setContentsMargins(10, 10, 10, 10)
        self.label_28 = QLabel(self.formGroupBox_4)
        self.label_28.setObjectName(u"label_28")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_28)

        self.label_30 = QLabel(self.formGroupBox_4)
        self.label_30.setObjectName(u"label_30")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_30)

        self.lineEdit_6 = QLineEdit(self.formGroupBox_4)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.lineEdit_6)

        self.lineEdit_7 = QLineEdit(self.formGroupBox_4)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.lineEdit_7)


        self.verticalLayout_44.addWidget(self.formGroupBox_4)


        self.horizontalLayout_54.addLayout(self.verticalLayout_44)

        self.verticalLayout_45 = QVBoxLayout()
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.horizontalLayout_55 = QHBoxLayout()
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.verticalGroupBox_3 = QGroupBox(self.can_page)
        self.verticalGroupBox_3.setObjectName(u"verticalGroupBox_3")
        self.verticalLayout_46 = QVBoxLayout(self.verticalGroupBox_3)
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")
        self.verticalLayout_46.setContentsMargins(10, 10, 10, 10)
        self.s2__receive_text_2 = QTextBrowser(self.verticalGroupBox_3)
        self.s2__receive_text_2.setObjectName(u"s2__receive_text_2")

        self.verticalLayout_46.addWidget(self.s2__receive_text_2)


        self.horizontalLayout_55.addWidget(self.verticalGroupBox_3)

        self.verticalLayout_47 = QVBoxLayout()
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_47.addItem(self.verticalSpacer_9)

        self.hex_receive_2 = QCheckBox(self.can_page)
        self.hex_receive_2.setObjectName(u"hex_receive_2")

        self.verticalLayout_47.addWidget(self.hex_receive_2)

        self.s2__clear_button_2 = QPushButton(self.can_page)
        self.s2__clear_button_2.setObjectName(u"s2__clear_button_2")
        self.s2__clear_button_2.setAutoFillBackground(False)
        self.s2__clear_button_2.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.verticalLayout_47.addWidget(self.s2__clear_button_2)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_47.addItem(self.verticalSpacer_10)


        self.horizontalLayout_55.addLayout(self.verticalLayout_47)


        self.verticalLayout_45.addLayout(self.horizontalLayout_55)

        self.horizontalLayout_70 = QHBoxLayout()
        self.horizontalLayout_70.setObjectName(u"horizontalLayout_70")
        self.verticalLayout_48 = QVBoxLayout()
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.verticalGroupBox_4 = QGroupBox(self.can_page)
        self.verticalGroupBox_4.setObjectName(u"verticalGroupBox_4")
        self.verticalLayout_50 = QVBoxLayout(self.verticalGroupBox_4)
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.verticalLayout_50.setContentsMargins(10, 10, 10, 10)
        self.s3__send_text_2 = QTextEdit(self.verticalGroupBox_4)
        self.s3__send_text_2.setObjectName(u"s3__send_text_2")

        self.verticalLayout_50.addWidget(self.s3__send_text_2)


        self.verticalLayout_48.addWidget(self.verticalGroupBox_4)

        self.horizontalLayout_71 = QHBoxLayout()
        self.horizontalLayout_71.setObjectName(u"horizontalLayout_71")
        self.timer_send_cb_2 = QCheckBox(self.can_page)
        self.timer_send_cb_2.setObjectName(u"timer_send_cb_2")

        self.horizontalLayout_71.addWidget(self.timer_send_cb_2)

        self.lineEdit_8 = QLineEdit(self.can_page)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.lineEdit_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_71.addWidget(self.lineEdit_8)

        self.dw_2 = QLabel(self.can_page)
        self.dw_2.setObjectName(u"dw_2")

        self.horizontalLayout_71.addWidget(self.dw_2)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_71.addItem(self.horizontalSpacer_9)

        self.horizontalLayout_71.setStretch(0, 1)
        self.horizontalLayout_71.setStretch(1, 1)
        self.horizontalLayout_71.setStretch(2, 1)
        self.horizontalLayout_71.setStretch(3, 4)

        self.verticalLayout_48.addLayout(self.horizontalLayout_71)


        self.horizontalLayout_70.addLayout(self.verticalLayout_48)

        self.verticalLayout_51 = QVBoxLayout()
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_51.addItem(self.verticalSpacer_11)

        self.hex_send_2 = QCheckBox(self.can_page)
        self.hex_send_2.setObjectName(u"hex_send_2")

        self.verticalLayout_51.addWidget(self.hex_send_2)

        self.s3__send_button_2 = QPushButton(self.can_page)
        self.s3__send_button_2.setObjectName(u"s3__send_button_2")
        self.s3__send_button_2.setAutoFillBackground(False)
        self.s3__send_button_2.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.verticalLayout_51.addWidget(self.s3__send_button_2)

        self.s3__clear_button_2 = QPushButton(self.can_page)
        self.s3__clear_button_2.setObjectName(u"s3__clear_button_2")
        self.s3__clear_button_2.setAutoFillBackground(False)
        self.s3__clear_button_2.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.verticalLayout_51.addWidget(self.s3__clear_button_2)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_51.addItem(self.verticalSpacer_12)


        self.horizontalLayout_70.addLayout(self.verticalLayout_51)


        self.verticalLayout_45.addLayout(self.horizontalLayout_70)


        self.horizontalLayout_54.addLayout(self.verticalLayout_45)

        self.horizontalLayout_54.setStretch(0, 1)
        self.horizontalLayout_54.setStretch(1, 5)

        self.verticalLayout_43.addLayout(self.horizontalLayout_54)


        self.verticalLayout_52.addLayout(self.verticalLayout_43)

        self.stackedWidget.addWidget(self.can_page)
        self.computer_info = QWidget()
        self.computer_info.setObjectName(u"computer_info")
        self.verticalLayout_22 = QVBoxLayout(self.computer_info)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.graphicsView = QGraphicsView(self.computer_info)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_21.addWidget(self.graphicsView)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.computer_info_start = QPushButton(self.computer_info)
        self.computer_info_start.setObjectName(u"computer_info_start")
        self.computer_info_start.setLayoutDirection(Qt.LeftToRight)
        self.computer_info_start.setAutoFillBackground(False)
        self.computer_info_start.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.horizontalLayout_6.addWidget(self.computer_info_start)

        self.computer_info_clear = QPushButton(self.computer_info)
        self.computer_info_clear.setObjectName(u"computer_info_clear")
        self.computer_info_clear.setLayoutDirection(Qt.LeftToRight)
        self.computer_info_clear.setAutoFillBackground(False)
        self.computer_info_clear.setStyleSheet(u"background-color: rgb(52, 59, 72);")

        self.horizontalLayout_6.addWidget(self.computer_info_clear)


        self.verticalLayout_21.addLayout(self.horizontalLayout_6)


        self.verticalLayout_22.addLayout(self.verticalLayout_21)

        self.stackedWidget.addWidget(self.computer_info)

        self.verticalLayout_49.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.btn_skin = QPushButton(self.topMenus)
        self.btn_skin.setObjectName(u"btn_skin")
        sizePolicy1.setHeightForWidth(self.btn_skin.sizePolicy().hasHeightForWidth())
        self.btn_skin.setSizePolicy(sizePolicy1)
        self.btn_skin.setMinimumSize(QSize(0, 45))
        self.btn_skin.setFont(font)
        self.btn_skin.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_skin.setLayoutDirection(Qt.LeftToRight)
        self.btn_skin.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-gamepad.png);\n"
"background-image: url(:/icons/images/icons/cil-loop.png);")

        self.verticalLayout_14.addWidget(self.btn_skin)

        self.btn_print = QPushButton(self.topMenus)
        self.btn_print.setObjectName(u"btn_print")
        sizePolicy1.setHeightForWidth(self.btn_print.sizePolicy().hasHeightForWidth())
        self.btn_print.setSizePolicy(sizePolicy1)
        self.btn_print.setMinimumSize(QSize(0, 45))
        self.btn_print.setFont(font)
        self.btn_print.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_print.setLayoutDirection(Qt.LeftToRight)
        self.btn_print.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-print.png);")

        self.verticalLayout_14.addWidget(self.btn_print)

        self.btn_logout = QPushButton(self.topMenus)
        self.btn_logout.setObjectName(u"btn_logout")
        sizePolicy1.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
        self.btn_logout.setSizePolicy(sizePolicy1)
        self.btn_logout.setMinimumSize(QSize(0, 45))
        self.btn_logout.setFont(font)
        self.btn_logout.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_logout.setLayoutDirection(Qt.LeftToRight)
        self.btn_logout.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-account-logout.png);")

        self.verticalLayout_14.addWidget(self.btn_logout)


        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)


        self.verticalLayout_7.addWidget(self.contentSettings)


        self.horizontalLayout_4.addWidget(self.extraRightBox)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font6 = QFont()
        font6.setFamilies([u"Microsoft YaHei UI"])
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        self.creditsLabel.setFont(font6)
        self.creditsLabel.setStyleSheet(u"font: 10pt \"Microsoft YaHei UI\";")
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setFont(font6)
        self.version.setStyleSheet(u"font: 10pt \"Microsoft YaHei UI\";")
        self.version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.horizontalLayout_8.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.s1__box_1.setDefault(True)
        self.s1__box_7.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"V2G", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Intelligent charge and discharge control system</p></body></html>", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"\u9690\u85cf", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u754c\u9762", None))
        self.btn_widgets.setText(QCoreApplication.translate("MainWindow", u"\u5145\u653e\u7535\u63a7\u5236", None))
        self.btn_new.setText(QCoreApplication.translate("MainWindow", u"\u4e32\u53e3\u6570\u636e", None))
        self.btn_save.setText(QCoreApplication.translate("MainWindow", u"CAN\u6570\u636e", None))
        self.btn_computer.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5206\u6790", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"Left Box", None))
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
        self.btn_share.setText(QCoreApplication.translate("MainWindow", u"Share", None))
        self.btn_adjustments.setText(QCoreApplication.translate("MainWindow", u"Adjustments", None))
        self.btn_more.setText(QCoreApplication.translate("MainWindow", u"More", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">PyDracula</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">An interface created using Python and PySide (support for PyQt), and with colors based on the Dracula theme created by Zen"
                        "o Rocha.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">MIT License</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#bd93f9;\">Created by: Wanderson M. Pimenta</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Convert UI</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#ffffff;\">pyside6-uic main.ui &gt; ui_main.py</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-in"
                        "dent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Convert QRC</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#ffffff;\">pyside6-rcc resources.qrc -o resources_rc.py</span></p></body></html>", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"\u7535\u52a8\u6c7d\u8f66\u5145\u653e\u7535\u63a7\u5236\u7cfb\u7edf", None))
#if QT_CONFIG(tooltip)
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.settingsTopBtn.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.verticalGroupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"\u5145\u7535", None))
        self.label_4.setText("")
        self.btn_charge.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5145\u7535", None))
        self.label_100.setText(QCoreApplication.translate("MainWindow", u"\u5145\u7535\u8bf7\u626b\u7801", None))
        self.verticalGroupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"\u653e\u7535", None))
        self.label_102.setText(QCoreApplication.translate("MainWindow", u"\u653e\u7535\u7535\u538b\uff1a", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"300", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"V \u8303\u56f4300-1000", None))
        self.label_103.setText(QCoreApplication.translate("MainWindow", u"\u653e\u7535\u7535\u6d41\uff1a", None))
        self.lineEdit_5.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"A \u8303\u56f40-250", None))
        self.label_105.setText(QCoreApplication.translate("MainWindow", u"\u653e\u7535\u622a\u6b62SOC\uff1a", None))
        self.lineEdit_9.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u" % \u8303\u56f40-100%", None))
        self.label_104.setText(QCoreApplication.translate("MainWindow", u"\u53c2\u6570\u8bbe\u7f6e\u540e\uff0c\u6309\u56de\u8f66\u952e\u751f\u6548", None))
        self.btn_discharge.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u653e\u7535", None))
        self.label_101.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u7535\u538b\u548c\u7535\u6d41\u540e\u5f00\u59cb\u653e\u7535", None))
        self.label_96.setText(QCoreApplication.translate("MainWindow", u"\u4e91\u5e73\u53f0\u901a\u4fe1\u72b6\u6001:", None))
        self.label_97.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_98.setText(QCoreApplication.translate("MainWindow", u"\u5145\u653e\u7535\u63a7\u5236\u5668\u901a\u4fe1\u72b6\u6001:", None))
        self.label_99.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_3.setText("")
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"\u5f85\u673a", None))
        self.verticalGroupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u4ea4\u6d41\u4fa7", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u7535\u538b:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u7535\u6d41:", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u529f\u7387:", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"kW", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\u53c2\u8003\u6548\u7387:", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"%", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"\u7d2f\u8ba1\u5145\u7535:", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"\u7d2f\u8ba1\u653e\u7535:", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.verticalGroupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\u76f4\u6d41\u4fa7", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"\u5145\u7535\u7535\u538b:", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"\u5145\u7535\u7535\u6d41:", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"\u5145\u7535\u529f\u7387:", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"kW", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"\u672c\u6b21\u7d2f\u8ba1\u7535\u91cf:", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"\u5145\u7535\u65f6\u957f:", None))
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u"min", None))
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"\u8d39\u7528:", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_65.setText(QCoreApplication.translate("MainWindow", u"\u5143", None))
        self.verticalGroupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"\u7535\u6c60\u6570\u636e", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"\u9700\u6c42\u7535\u538b:", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"\u9700\u6c42\u7535\u6d41:", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_110.setText(QCoreApplication.translate("MainWindow", u"\u5b9e\u9645\u7535\u538b:", None))
        self.label_111.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_112.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.label_113.setText(QCoreApplication.translate("MainWindow", u"\u5b9e\u9645\u7535\u6d41:", None))
        self.label_114.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_115.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_81.setText(QCoreApplication.translate("MainWindow", u"SOC", None))
        self.label_144.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_145.setText(QCoreApplication.translate("MainWindow", u"%", None))
        self.label_66.setText(QCoreApplication.translate("MainWindow", u"\u5145\u7535\u6a21\u5f0f:", None))
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_69.setText(QCoreApplication.translate("MainWindow", u"\u6700\u9ad8\u7535\u6c60\u6e29\u5ea6:", None))
        self.label_70.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_71.setText(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.label_116.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u53f7:", None))
        self.label_117.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_72.setText(QCoreApplication.translate("MainWindow", u"\u6700\u4f4e\u7535\u6c60\u6e29\u5ea6:", None))
        self.label_73.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_74.setText(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.label_118.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u53f7:", None))
        self.label_119.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_75.setText(QCoreApplication.translate("MainWindow", u"\u6700\u9ad8\u5355\u4f53\u7535\u538b:", None))
        self.label_76.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_77.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.label_120.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u53f7:", None))
        self.label_121.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_78.setText(QCoreApplication.translate("MainWindow", u"\u5269\u4f59\u5145\u7535\u65f6\u95f4:", None))
        self.label_79.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_80.setText(QCoreApplication.translate("MainWindow", u"min", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"\u7535\u6c60\u7c7b\u578b:", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_68.setText(QCoreApplication.translate("MainWindow", u"\u7535\u6c60\u6807\u79f0\u603b\u80fd\u91cf:", None))
        self.label_82.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_95.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.label_84.setText(QCoreApplication.translate("MainWindow", u"\u7535\u6c60\u7cfb\u7edf\u989d\u5b9a\u5bb9\u91cf:", None))
        self.label_85.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_86.setText(QCoreApplication.translate("MainWindow", u"Ah", None))
        self.label_83.setText(QCoreApplication.translate("MainWindow", u"\u7535\u6c60\u7cfb\u7edf\u989d\u5b9a\u603b\u7535\u538b:", None))
        self.label_87.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_88.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.label_89.setText(QCoreApplication.translate("MainWindow", u"\u7535\u6c60\u751f\u4ea7\u65e5\u671f:", None))
        self.label_90.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_91.setText(QCoreApplication.translate("MainWindow", u"\u7535\u6c60\u7ec4\u5145\u7535\u6b21\u6570:", None))
        self.label_92.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_93.setText(QCoreApplication.translate("MainWindow", u"VIN:", None))
        self.label_94.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_122.setText(QCoreApplication.translate("MainWindow", u"\u6700\u9ad8\u5141\u8bb8\u5145\u7535\u7535\u6d41:", None))
        self.label_123.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_137.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_138.setText(QCoreApplication.translate("MainWindow", u"\u6700\u9ad8\u5141\u8bb8\u5145\u7535\u603b\u7535\u538b:", None))
        self.label_139.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_140.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.label_141.setText(QCoreApplication.translate("MainWindow", u"\u6700\u9ad8\u5141\u8bb8\u6e29\u5ea6:", None))
        self.label_142.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_143.setText(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.verticalGroupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u72b6\u6001", None))
        self.label_124.setText(QCoreApplication.translate("MainWindow", u"\u6545\u969c\u4ee3\u7801:", None))
        self.label_125.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_126.setText(QCoreApplication.translate("MainWindow", u"\u544a\u8b66\u4ee3\u7801:", None))
        self.label_127.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_131.setText(QCoreApplication.translate("MainWindow", u"\u5145\u7535\u67aa\u8fde\u63a5\u72b6\u6001:", None))
        self.label_154.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_129.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559:", None))
        self.label_128.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_132.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559:", None))
        self.label_130.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_133.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559:", None))
        self.label_134.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_135.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559:", None))
        self.label_136.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_150.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559:", None))
        self.label_151.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_152.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559:", None))
        self.label_153.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_155.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559:", None))
        self.label_156.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.formGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u4e32\u53e3\u8bbe\u7f6e", None))
        self.s1__lb_1.setText(QCoreApplication.translate("MainWindow", u"\u4e32\u53e3\u68c0\u6d4b\uff1a", None))
        self.s1__box_1.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u4e32\u53e3", None))
        self.s1__lb_2.setText(QCoreApplication.translate("MainWindow", u"\u4e32\u53e3\u9009\u62e9\uff1a", None))
        self.s1__lb_3.setText(QCoreApplication.translate("MainWindow", u"\u6ce2\u7279\u7387\uff1a", None))
        self.s1__box_3.setItemText(0, QCoreApplication.translate("MainWindow", u"115200", None))
        self.s1__box_3.setItemText(1, QCoreApplication.translate("MainWindow", u"2400", None))
        self.s1__box_3.setItemText(2, QCoreApplication.translate("MainWindow", u"4800", None))
        self.s1__box_3.setItemText(3, QCoreApplication.translate("MainWindow", u"9600", None))
        self.s1__box_3.setItemText(4, QCoreApplication.translate("MainWindow", u"14400", None))
        self.s1__box_3.setItemText(5, QCoreApplication.translate("MainWindow", u"19200", None))
        self.s1__box_3.setItemText(6, QCoreApplication.translate("MainWindow", u"38400", None))
        self.s1__box_3.setItemText(7, QCoreApplication.translate("MainWindow", u"57600", None))
        self.s1__box_3.setItemText(8, QCoreApplication.translate("MainWindow", u"76800", None))
        self.s1__box_3.setItemText(9, QCoreApplication.translate("MainWindow", u"12800", None))
        self.s1__box_3.setItemText(10, QCoreApplication.translate("MainWindow", u"230400", None))
        self.s1__box_3.setItemText(11, QCoreApplication.translate("MainWindow", u"460800", None))

        self.s1__lb_4.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u4f4d\uff1a", None))
        self.s1__box_4.setItemText(0, QCoreApplication.translate("MainWindow", u"8", None))
        self.s1__box_4.setItemText(1, QCoreApplication.translate("MainWindow", u"7", None))
        self.s1__box_4.setItemText(2, QCoreApplication.translate("MainWindow", u"6", None))
        self.s1__box_4.setItemText(3, QCoreApplication.translate("MainWindow", u"5", None))

        self.s1__lb_5.setText(QCoreApplication.translate("MainWindow", u"\u6821\u9a8c\u4f4d\uff1a", None))
        self.s1__box_5.setItemText(0, QCoreApplication.translate("MainWindow", u"N", None))

        self.open_button.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u4e32\u53e3", None))
        self.close_button.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u4e32\u53e3", None))
        self.s1__lb_6.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u4f4d\uff1a", None))
        self.s1__box_6.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))

        self.state_label.setText("")
        self.formGroupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u4e32\u53e3\u72b6\u6001", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u63a5\u6536\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u53d1\u9001\uff1a", None))
        self.verticalGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u63a5\u6536\u533a", None))
        self.hex_receive.setText(QCoreApplication.translate("MainWindow", u"Hex\u63a5\u6536", None))
        self.s2__clear_button.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664", None))
        self.verticalGroupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u533a", None))
        self.s3__send_text.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.timer_send_cb.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u65f6\u53d1\u9001", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.dw.setText(QCoreApplication.translate("MainWindow", u"ms/\u6b21", None))
        self.hex_send.setText(QCoreApplication.translate("MainWindow", u"Hex\u53d1\u9001", None))
        self.s3__send_button.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001", None))
        self.s3__clear_button.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664", None))
        self.formGroupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"CAN\u8bbe\u7f6e", None))
        self.s1__lb_7.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u68c0\u6d4b\uff1a", None))
        self.s1__box_7.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4bCAN\u8bbe\u5907", None))
        self.s1__lb_8.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u9009\u62e9\uff1a", None))
        self.s1__lb_9.setText(QCoreApplication.translate("MainWindow", u"CAN\u901a\u9053\uff1a", None))
        self.s1__box_9.setItemText(0, QCoreApplication.translate("MainWindow", u"0", None))
        self.s1__box_9.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))

        self.s1__lb_10.setText(QCoreApplication.translate("MainWindow", u"\u6ce2\u7279\u7387:", None))
        self.s1__box_10.setItemText(0, QCoreApplication.translate("MainWindow", u"250kbps", None))
        self.s1__box_10.setItemText(1, QCoreApplication.translate("MainWindow", u"125kbps", None))

        self.s1__lb_11.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559\uff1a", None))
        self.open_button_2.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u8bbe\u5907", None))
        self.close_button_2.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u8bbe\u5907", None))
        self.s1__lb_12.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559\uff1a", None))
        self.state_label_2.setText("")
        self.formGroupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"CAN\u72b6\u6001", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u63a5\u6536\uff1a", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u53d1\u9001\uff1a", None))
        self.verticalGroupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u63a5\u6536\u533a", None))
        self.hex_receive_2.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559", None))
        self.s2__clear_button_2.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664", None))
        self.verticalGroupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u533a", None))
        self.s3__send_text_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.timer_send_cb_2.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u65f6\u53d1\u9001", None))
        self.lineEdit_8.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.dw_2.setText(QCoreApplication.translate("MainWindow", u"ms/\u6b21", None))
        self.hex_send_2.setText(QCoreApplication.translate("MainWindow", u"\u9884\u7559", None))
        self.s3__send_button_2.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001", None))
        self.s3__clear_button_2.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664", None))
        self.computer_info_start.setText(QCoreApplication.translate("MainWindow", u"\u7ed8\u56fe", None))
        self.computer_info_clear.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664", None))
        self.btn_skin.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u6362\u76ae\u80a4", None))
        self.btn_print.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5370", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa\u767b\u5f55", None))
        self.creditsLabel.setText("")
        self.version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi

