import sys
import ctypes

from minecraft_cn_login_fix_tool.app.pages.main_window import MainPage

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    app.font().families().append("Microsoft YaHei UI")
    main_app = MainPage()
    main_app.show()
    app.exec_()


if __name__ == '__main__':
    if int(is_admin()) == 1:
        sys.exit(main())
    else:
        app = QApplication(sys.argv)
        w = QWidget()
        error_window = QMessageBox.critical(w, "警告", "请使用管理员身份运行！", QMessageBox.Yes)

