from SmartCamera import creat_app
from SmartCamera.main import check_for_objects
import threading

app=creat_app()

if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
