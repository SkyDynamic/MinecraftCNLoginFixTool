import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


def main():
    from minecraft_cn_login_fix_tool.app.pages.main_window import MainPage
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    app.font().families().append("Microsoft YaHei UI")
    main_app = MainPage()
    main_app.show()
    app.exec_()


if __name__ == '__main__':
    sys.exit(main())
