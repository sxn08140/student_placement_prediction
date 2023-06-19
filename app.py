import numpy as np
from flask import Flask, request, render_template, jsonify
import pickle

app = Flask(__name__)
model_placement = pickle.load(open('sv_model.pkl', 'rb'))
model_salary = pickle.load(open('rfreg_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

	gender=int(request.form.get("gender"))
	ssc_p=int(request.form.get("ssc_p"))
	ssc_b=int(request.form.get("ssc_b"))
	hsc_p=int(request.form.get("hsc_p"))
	hsc_b=int(request.form.get("hsc_b"))
	degree_p=int(request.form.get("degree_p"))
	workex=int(request.form.get("workex"))
	etest_p=int(request.form.get("etest_p"))
	
	degree=request.form.get("degree_t")

	print("Degree:",degree)

	Comm_Mgmt=0
	Other_Degree=0
	Sci_Tech=0

	if degree=="Comm&Mgmt":
		Comm_Mgmt=1
		Other_Degree=0
		Sci_Tech=0
	elif degree=="Others":
		Comm_Mgmt=0
		Other_Degree=1
		Sci_Tech=0
	elif degree=="Sci&Tech":
		Comm_Mgmt=0
		Other_Degree=0
		Sci_Tech=1
	
	hsc=request.form.get("hsc_s")

	print("HSC:",hsc)

	Arts=0
	Commerce=0
	Science=0
	
	if hsc=="Arts":
		Arts=1
		Commerce=0
		Science=0
	elif hsc=="Commerce":
		Arts=0
		Commerce=1
		Science=0
	elif hsc=="Science":
		Arts=0
		Commerce=0
		Science=1

	print([gender,ssc_p,ssc_b,hsc_p,hsc_b,degree_p,workex,etest_p,Arts,Commerce,Science,Comm_Mgmt,Other_Degree,Sci_Tech])

	prediction =model_placement.predict([[gender,ssc_p,ssc_b,hsc_p,hsc_b,degree_p,workex,etest_p,Arts,Commerce,Science,Comm_Mgmt,Other_Degree,Sci_Tech]])

	output=""
	print("Prediction:",prediction)
	if prediction[0]==0:
		output="Not Placed"
	elif prediction[0]==1:
		output="Likely to be Placed"

	salary =model_salary.predict([[gender,ssc_p,ssc_b,hsc_p,hsc_b,degree_p,workex,etest_p,Arts,Commerce,Science,Comm_Mgmt,Other_Degree,Sci_Tech]])
	salaryhigh=salary+100000
	salarylow = salary - 100000

	if output=="Not Placed":
		salaryhigh=0
		salarylow=0

	return render_template('index.html', prediction_text=output,salary_high=salaryhigh,salary_low=salarylow)

if __name__ == "__main__":
	app.run(debug=True)
