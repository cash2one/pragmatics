#!flask/bin/python
from ybsuggestions import app
from ybsuggestions.crawler import scheduler

if __name__ == "__main__":
    #scheduler.start()

    app.run(host='0.0.0.0', debug=True)