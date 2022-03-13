from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select, text
from datetime import datetime
from payments import pay_piastr

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Orders(db.Model):
    """валюта, 
    сумма, 
    время отправки, 
    описание, 
    идентификатор платежа в БД или файл"""
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(50), nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    send_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Orders %r>' % self.id

@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create-order', methods=['POST', 'GET'])
def create_order():
    if request.method == "POST":
        description = request.form['description']
        sum = request.form['sum']
        currency = request.form['paymentMethod']

        order = Orders(description=description, sum=int(sum), currency=currency)

        try:
            db.session.add(order)
            db.session.commit()
            
            try :
                sql_query = text("SELECT MAX(id) FROM orders")
                result = db.session.execute(sql_query)
                for id in result:
                    order_id = id[0]
                    #return order_id
                    
            except Exception as e:
                print(e)
                return "Error"
            db.session.commit()

            pay =  pay_piastr(description, currency, sum, order_id)
            print(pay)
            return redirect('/')
        except Exception as e:
            print(e)
            return "Error"

    else:
        return render_template("create-order.html")


if __name__ == "__main__":
    app.run(debug=True)
