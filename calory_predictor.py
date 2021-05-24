#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from flask import request, Flask, render_template

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def calory():
    return render_template('calories-predictor.html')
        

@app.route('/cal_data',methods=['GET','POST'])
def cal_data():
    if request.method == "POST":
        exercise_df = pd.read_csv("./Data/exercise.csv")
        calories_df = pd.read_csv("./Data/calories.csv")
        df = pd.merge(exercise_df,calories_df,on='User_ID', how='left')
        encoder = LabelEncoder()
        df['Gender'] = encoder.fit_transform(df['Gender'].astype(str))
        del df[ 'User_ID' ]
        X = df.drop('Calories',axis = 1)
        y = df['Calories']
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.70, random_state=42)

        print("Training Prediction Model...")
        rf_model = RandomForestRegressor()
        rf_model.fit(X_train,y_train)
        # rf_model.fit(X,y)

        gender = request.form.get('gender')
        age = request.form.get('age')
        height = request.form.get('height')
        weight = request.form.get('weight')
        duration = request.form.get('duration')
        heart_rate = request.form.get('heart-rate')
        body_temp = request.form.get('body-temp')

        print("Took User Data...")
        #print()
        #gender = int(input("Enter Gender: "))
        #print(gender)
        input_data = [[gender, age, height, weight, duration, heart_rate, body_temp]]
        output_data = rf_model.predict(input_data)
        print("Predicted output...")
        print(output_data)
        cal=str(output_data[0])
        return render_template('calories-predictor.html',variable = cal)
    #print(type(output_data))
        
    # return render_template('calories-predictor.html',variable = cal)

if __name__ == '__main__':
    app.run(debug=True)
