from extension import app
from extension import db

@app.before_first_request
def create():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
