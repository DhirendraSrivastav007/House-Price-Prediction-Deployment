from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Data Wrangling and Data Analysis
import pandas as pd , numpy as np
# Feature Engineering / Feature Selection
from sklearn.pipeline import Pipeline
from category_encoders import GLMMEncoder
# Model Building
from xgboost import XGBRegressor
import pickle



app = Flask(__name__)
model_pipeline = pickle.load(open('static\house_price_model_pipeline', 'rb'))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///MyAPP.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    FullBath = db.Column(db.Integer)
    secondFlrSF = db.Column(db.Float)
    KitchenQual = db.Column(db.String(100), nullable=False)
    GrLivArea = db.Column(db.Float)
    Neighborhood = db.Column(db.String(100), nullable=False)
    GarageFinish = db.Column(db.String(100), nullable=False)
    ExterQual = db.Column(db.String(100), nullable=False)
    BsmtQual = db.Column(db.String(100), nullable=False)
    OverallQual = db.Column(db.Integer)
    GarageCars = db.Column(db.Integer)
    Prediction = db.Column(db.Float)

    # def __repr__(self) -> str:
    #     return f"{self.sno} - {self.title}"


@app.route('/',  methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        FullBath = int(request.form['FullBath'])
        secondFlrSF = float(request.form['2ndFlrSF'])
        KitchenQual = str(request.form['KitchenQual'])
        GrLivArea = float(request.form['GrLivArea'])
        Neighborhood = str(request.form['Neighborhood'])
        GarageFinish = str(request.form['GarageFinish'])
        ExterQual = str(request.form['ExterQual'])
        BsmtQual = str(request.form['BsmtQual'])
        OverallQual = int(request.form['OverallQual'])
        GarageCars = int(request.form['GarageCars'])

        Features = pd.DataFrame({'FullBath': FullBath, '2ndFlrSF' : secondFlrSF, 'KitchenQual' : KitchenQual,
         'GrLivArea':GrLivArea, 'Neighborhood':Neighborhood, 'GarageFinish':GarageFinish, 'ExterQual':ExterQual,
        'BsmtQual':BsmtQual, 'OverallQual':OverallQual, 'GarageCars':GarageCars}, index=[0])

        Prediction = model_pipeline.predict(Features)[0]

       


        todo = Todo(FullBath = FullBath, secondFlrSF = secondFlrSF,
                    KitchenQual = KitchenQual, GrLivArea = GrLivArea,
                    Neighborhood = Neighborhood, GarageFinish = GarageFinish,
                    ExterQual = ExterQual, BsmtQual = BsmtQual, OverallQual = OverallQual, GarageCars = GarageCars,
                    Prediction = Prediction)

        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
