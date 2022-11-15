import pandas as pd

df = pd.read_csv("Rainfall_Weather.csv")

from flask import Flask, render_template, request
# from flask_ngrok import run_with_ngrok
from datetime import datetime
import pickle

filen = "KNN_rainfall.pkl"
model = pickle.load(open(filen, 'rb'))

app = Flask(__name__,template_folder="templates")
# run_with_ngrok(app)

@app.route("/")
def prec():
  return render_template("Precautions.html")

@app.route("/pred_in")
def pred_in():
  return render_template("pred_in.html")

@app.route("/pred_out")
def pred_out():
  MinTemp = request.args.get("MinTemp")
  MaxTemp = request.args.get("MaxTemp")
  Rainfall = request.args.get("Rainfall")
  Evaporation = request.args.get("Evaporation")
  Sunshine = request.args.get("Sunshine")
  WindGustSpeed = request.args.get("WindGustSpeed")
  WindSpeed9am = request.args.get("WindSpeed9am")
  WindSpeed3pm = request.args.get("WindSpeed3pm")
  Humidity9am = request.args.get("Humidity9am")
  Humidity3pm = request.args.get("Humidity3pm")
  Pressure9am = request.args.get("Pressure9am")
  Pressure3pm = request.args.get("Pressure3pm")
  Cloud9am = request.args.get("Cloud9am")
  Cloud3pm = request.args.get("Cloud3pm")
  Temp9am = request.args.get("Temp9am")
  Temp3pm = request.args.get("Temp3pm")
  lis = [[MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine, WindGustSpeed, WindSpeed9am, WindSpeed3pm, Humidity9am, Humidity3pm, Pressure9am, Pressure3pm ,Cloud9am, Cloud3pm, Temp9am, Temp3pm	]]
  lis = [list(map(float, lis[0]))]
  [pred] = model.predict(lis)
  return render_template("pred_out.html", Prediction_result = pred)


@app.route("/trend_in")
def trend_in():
  return render_template("trend_in.html")

@app.route("/trend_out")
def trend_out():
  loc = request.args.get("locations")
  yr = request.args.get("year")
  df['Date'] = pd.to_datetime(df['Date'])  
  sd = str(yr)+'-1-1'
  sd = datetime.strptime(sd, '%Y-%m-%d')
  ed = str(yr)+'-12-31'
  ed = datetime.strptime(ed, '%Y-%m-%d')
  date_mask = (df['Date'] >= sd ) & (df['Date'] <= ed)
  loc_mask = (df['Location']==loc)
  mask = date_mask & loc_mask
  data = df.loc[mask]
  return render_template("trend_out.html", tab = data.to_html(), loc=loc, yr = yr)

if __name__ == "__main__":
    app.run(debug=True)