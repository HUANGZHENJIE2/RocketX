from PyQt5.QtWidgets import QMessageBox

from application import Application

if __name__ == '__main__':
    debug = True
    if debug:
        app = Application()
        app.run()
    else:
        try:
            app = Application()
            app.run()
        except BaseException as be:
            errorMessageBox = QMessageBox()
            errorMessageBox.setWindowTitle('Error')
            errorMessageBox.setIcon(QMessageBox.Critical)
            errorMessageBox.setText(str(be))
            errorMessageBox.exec()
