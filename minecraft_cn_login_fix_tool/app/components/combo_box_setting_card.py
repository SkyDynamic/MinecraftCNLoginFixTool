from typing import Union, List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from qfluentwidgets import SettingCard, FluentIconBase, ComboBox


class ComboBoxSettingCard(SettingCard):

    def __init__(self, value: str, values: List[str], icon: Union[str, QIcon, FluentIconBase], title, content=None,
                 parent=None):
        super().__init__(icon, title, content, parent)

        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.comboBox.addItems(values)
        self.comboBox.setCurrentText(value)
        self.comboBox.setMinimumWidth(140)



