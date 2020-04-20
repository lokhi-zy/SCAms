from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import os
import test
import train
import numpy as np
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/",methods=['GET','POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            return redirect("/systems")
        else:
            message = "Login Failed"
            return render_template('index2.html', message = message)
    
    return  render_template("index2.html")


@app.route('/test', methods=["GET", "POST"])
def index():

    modelpath = basedir + "/model/"
    modelfile = os.listdir(modelpath)
    standpath = basedir + "/standard/"
    standfile = os.listdir(standpath)

    return render_template("test.html" , modelfile = modelfile , standfile =standfile)
   

@app.route("/systems")
def systems():

    return render_template("systems.html")

@app.route("/introduce")
def introduce():

    return render_template("introduce.html")

@app.route("/model")
def model():

    return render_template("model.html")

@app.route("/loaddata" , methods=["POST"] )
def loaddata():
    datafile = request.files["datafile"]
    filename = datafile.filename
    path = basedir + "/data_train/"
    file_path = path + datafile.filename
    datafile.save(file_path)

    generation = request.form['generation']
    generation = int(generation)


    weight_final = train.train(generation,filename)
    lenth = len(weight_final)
 


    Accuracy = weight_final[lenth - 1]
    Accuracy = round(Accuracy,3) * 100
   

    model = weight_final   
    modelname = request.form['modelname']
    model_path = basedir + "/model/" + modelname
    np.savetxt(model_path,model)

    return render_template("model.html", Accuracy = Accuracy ,modelpath = model_path)



@app.route("/judge" , methods=["POST"] )
def judge():

    examplefile = request.files["examplefile"]
    examplename = examplefile.filename
    path = basedir + "/data_test/"
    file_path = path + examplefile.filename
    examplefile.save(file_path)

    standname = request.form['standname']
    modelname = request.form['modelname']

    result = test.test(standname,modelname,examplename)

    Accuracy = result[1]

    Accuracy = round(Accuracy,3) * 100

    print(Accuracy)
    if result[0] == 2:
        
        return render_template("test.html", result = 2 , Accuracy = Accuracy , mistake = (100 - Accuracy))

    else:
        return render_template("test.html", result = 1 , Accuracy = Accuracy , mistake = (100 - Accuracy))











if __name__ == '__main__':
    app.run()
