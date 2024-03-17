from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///passport.db"
db = SQLAlchemy(app)


class Passport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(70), nullable=False)
    nationality = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)
    passport_number = db.Column(db.String(10), nullable=False, unique=True)


@app.route("/")
def index():
    return "<a href='http://127.0.0.1:5000/passport'>Паспортные данные</a>"


@app.route('/passport', methods=['GET'])
def get_passport_by_number():
    passport_number = request.args.get('passport_number')
    passport = Passport.query.filter_by(passport_number=passport_number).first()
    if passport:
        return jsonify({
            'full_name': passport.full_name,
            'nationality': passport.nationality,
            'birth_date': passport.birth_date,
            'passport_number': passport.passport_number
        })
    else:
        return jsonify({'error': 'Не найден паспорт за кодом'}), 404


def fill_database():
        passport_data = [
            {"full_name": "John Doe", "nationality": "US", "birth_date": "1939-09-01", "passport_number": "AB123456"},
            {"full_name": "Jane Doe", "nationality": "UK", "birth_date": "1945-09-02", "passport_number": "CD654321"},
            {"full_name": "Johnen Doe", "nationality": "UE", "birth_date": "2001-09-11", "passport_number": "EF767676"}
        ]
        for passport_info in passport_data:
            existing_passport = Passport.query.filter_by(passport_number=passport_info["passport_number"]).first()
            if existing_passport is None:
                passport = Passport(full_name=passport_info["full_name"],
                                    nationality=passport_info["nationality"],
                                    birth_date=passport_info["birth_date"],
                                    passport_number=passport_info["passport_number"])
                db.session.add(passport)
                db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fill_database()
    app.run(debug=True)