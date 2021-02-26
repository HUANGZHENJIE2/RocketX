from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu


class HelpMenu(QMenu):
    def __init__(self, app):
        super(HelpMenu, self).__init__()
        self.app = app

        self.feedbackAction = self.addAction("feedback")
        self.aboutAction = self.addAction("About")

        self.init()

    def init(self):

        self.setStyleSheet(
            '''
                QMenu {
                    background-color: rgb(236,236,237);
                    border-width: 1px 1px 1px 1px;
                    border-style: solid;
                    border-color: #c6c6c6;
                    font: 9pt "Arial";
                    padding: 3px 0px
                }
                
                QMenu::item {
                    font-size:9pt "Arial";
                    color: rgb(0,0,0);
                    background-color: rgb(236,236,237);
                    padding: 8px 40px 8px 40px;
                }
                
                QMenu::item:selected {
                    background-color : rgb(255, 255, 255);
                }
            '''
        )
        pros = self.app.strings.properties
        self.feedbackAction.setText(pros["feedback"])
        self.aboutAction.setText(pros["about"])
        self.aboutAction.triggered.connect(self.aboutActionTriggered)
        self.feedbackAction.triggered.connect(self.feedbackActionTriggered)

    def aboutActionTriggered(self):
        if self.app.aboutWindow.isVisible():
            self.app.aboutWindow.hide()
        self.app.aboutWindow.show()

    def feedbackActionTriggered(self):
        if self.app.feedbackWindow.isVisible():
            self.app.feedbackWindow.hide()
        self.app.feedbackWindow.show()
