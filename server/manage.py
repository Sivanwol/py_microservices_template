"""
The entry point to our Python Flask application.
"""
from .app import ApplicationMgr

ApplicationMgr.init()
appMgr = ApplicationMgr

if __name__ == "__main__":
    appMgr.application.run(host='0.0.0.0', port=3000 , debug=True)