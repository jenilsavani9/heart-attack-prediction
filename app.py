from logging import debug
from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
   return render_template("home.html")

@app.route('/predict', methods=['POST'])
def predict():
   if request.method == "POST":
      age = int(request.form.get('age'))
      sex_cat = request.form.get('sex')
      if sex_cat == "male":
         sex = 1
      else:
         sex = 0
      exang_cat = request.form.get('exang')
      if exang_cat == "Yes":
         exang = 1
      else:
         exang = 0
      ca = int(request.form.get('ca'))
      cp_cat = request.form.get('cp')
      if cp_cat == "Typical Angina":
         cp = 0
      elif cp_cat == "Atypical Angina":
         cp = 1
      elif cp_cat == "Non-anginal Pain":
         cp = 2
      else:
         cp = 3
      trtbps = int(request.form.get('trtbps'))
      chol = int(request.form.get('chol'))
      fbs_cat = int(request.form.get('fbs'))
      if fbs_cat >= 120:
         fbs = 1
      else:
         fbs = 0
      rest_ecg_cat = request.form.get('rest_ecg')
      if rest_ecg_cat == "hypertrophy":
         rest_ecg = 0
      elif rest_ecg_cat == "Normal":
         rest_ecg = 1
      else:
         rest_ecg = 2
      thalach = int(request.form.get('thalach'))
      oldpeak = float(request.form.get('oldpeak'))
      slp_cat = request.form.get('slp')   
      if slp_cat == "Downsloping":
         slp = 0
      elif slp_cat == "Flat":
         slp = 1
      else:
         slp = 2
      
      thall = 1

      col = [age, sex, cp, trtbps, chol, fbs, rest_ecg, thalach, exang, oldpeak, slp, ca, thall]
      col_mean = [54.366336633663366,0.6831683168316832,0.966996699669967,131.62376237623764,
                  246.26402640264027,0.1485148514851485,0.528052805280528,149.64686468646866,
                  0.32673267326732675,1.0396039603960396,1.3993399339933994,0.7293729372937293,
                  2.3135313531353137,0.5445544554455446]
      
      col_std = [9.082100989837857,0.46601082333962385,1.0320524894832985,17.5381428135171,
               51.83075098793003,0.35619787492797644,0.525859596359298,22.905161114914094,
               0.4697944645223165,1.1610750220686348,0.6162261453459619,1.022606364969327,
               0.6122765072781409,0.4988347841643913]

      col_ans = []
      for i in range(len(col)):
         col_ans.append((col[i]-col_mean[i])/col_std[i])
      print(col)
      model = joblib.load('svc_clf.pkl', 'rb')

      prediction = model.predict([col_ans])
      print(prediction)
      if prediction[0] == 0:
         pre = "You Are out of denger"
      else:
         pre = "you are in denger"
      return render_template("predict.html", prediction=pre, ans = prediction[0])
   else:
      return render_template("home.html")

if __name__=="__main__":
    app.run(debug=True)