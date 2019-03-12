"""To run the app throught UWSGI"""
from manage import app  # pylint: disable=R0401

if __name__ == '__main__':
    app.run()
