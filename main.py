from app import create_app, db, init_data
from socket import gethostname

app = create_app()
with app.app_context():
    db.create_all()
    init_data()

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run(debug=True)
