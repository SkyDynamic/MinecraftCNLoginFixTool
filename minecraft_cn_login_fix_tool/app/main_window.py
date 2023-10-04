from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSettings, QVariant, QSize, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QStackedWidget
from qfluentwidgets import NavigationInterface, qrouter, FluentIcon
from qframelesswindow import FramelessWindow, StandardTitleBar

from .pages.login_fix_page import LoginPage
from .pages.auth_fix_page import AuthPage

class MainWindow(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = StandardTitleBar(self)
        self.title.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Microsoft YaHei';
                padding: 0 4px
            }
        """)
        self.setTitleBar(self.title)
        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(
            self, showMenuButton=True, showReturnButton=True)
        self.stackWidget = QStackedWidget(self)

        self.login_interface = LoginPage(self)
        self.auth_interface = AuthPage(self)

        self.stackWidget.addWidget(self.login_interface)
        self.stackWidget.addWidget(self.auth_interface)

        self.initLayout()
        self.initNavigation()
        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)

    def initNavigation(self):
        self.navigationInterface.addItem(
            routeKey=self.login_interface.objectName(),
            icon=FluentIcon.DEVELOPER_TOOLS,
            text="启动器登录/皮肤下载",
            onClick=lambda: self.switchTo(self.login_interface)
        )
        
        self.navigationInterface.addItem(
            routeKey=self.auth_interface.objectName(),
            icon=FluentIcon.GAME,
            text="验证服务器",
            onClick=lambda: self.switchTo(self.auth_interface)
        )

        qrouter.setDefaultRouteKey(self.stackWidget, self.login_interface.objectName())
        self.navigationInterface.setCurrentItem(self.login_interface.objectName())

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(0)

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def initWindow(self):
        self.readSettings()
        self.setWindowIcon(QIcon('resources/icon.ico'))
        self.setWindowTitle(self.tr("Minecraft CN Login Fix Tool V1.1.0"))
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        super().closeEvent(event)
        self.saveSettings()

    def readSettings(self):
        settings = QSettings("SkyDynamic", "SimpleMCServerCreater")
        size = settings.value("size", QVariant(QSize(900, 700)))
        pos = settings.value("pos", QVariant(QPoint(200, 200)))
        self.resize(size)
        self.move(pos)

    def saveSettings(self):
        settings = QSettings("SkyDynamic", "SimpleMCServerCreater")
        settings.setValue("size", QVariant(self.size()))
        settings.setValue("pos", QVariant(self.pos()))
