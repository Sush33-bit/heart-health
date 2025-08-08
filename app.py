from flask import Flask, render_template, request
import pandas as pd
import os
import pickle
import csv
import smtplib 

app = Flask(__name__)
with open ("model.pkl" , "rb") as f:
    model=pickle.load(f)

@app.route('/')
def index():
    return render_template('check2.html')

@app.route('/checkup')
def checkup():
    return render_template('checkupfile.html')

@app.route('/unconscious')
def unconscious():
    return render_template('unconscious.html')

@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

@app.route('/predict', methods=['POST'])
def predict():
    Age = float(request.form['age'])
    RestingBP = float(request.form['restingBP'])
    Cholesterol = float(request.form['cholesterol'])
    FastingBS = float(request.form['fastingBS'])
    MaxHR = float(request.form['maxHR'])
    Sex_M = float(request.form['sex'])
    ExerciseAngina_Y = float(request.form['exerciseAngina'])

    threshold = 0.2  # Adjust the threshold as needed
    prediction, user_data = predict_heart_attack(Age, RestingBP, Cholesterol, FastingBS, MaxHR, Sex_M, ExerciseAngina_Y,threshold)

    if prediction == 0:
        result = "The person is not likely to have a heart attack."
    else:
        result = "The person is likely to have a heart attack."

    # user_data_combined = pd.concat([user_data_combined, user_data], ignore_index=True)
    # user_data_combined.to_csv('user.csv', index=False)

    return render_template('result.html', result=result)
def predict_heart_attack(Age, RestingBP, Cholesterol, FastingBS, MaxHR, Sex_M, ExerciseAngina_Y,  threshold=0.5):
    """
    Predict whether a person will have a heart attack or not.
    
    Parameters:
        Age: Age of the person
        RestingBP: Resting blood pressure
        Cholesterol: Cholesterol level
        FastingBS: Fasting blood sugar (1 if > 120 mg/dl, 0 otherwise)
        MaxHR: Maximum heart rate achieved
        Sex_M: Sex of the person (0 for female, 1 for male)
        ExerciseAngina_Y: Exercise induced angina (0 for No, 1 for Yes)
        model: Trained Random Forest model
        threshold: Custom threshold for classification (default is 0.5)
        
    Returns:
        prediction: Predicted class label (0 for no heart attack, 1 for heart attack)
        user_data: DataFrame containing user input
    """
   
    user_data = pd.DataFrame({
        'Age': [Age],
        'RestingBP': [RestingBP],
        'Cholesterol': [Cholesterol],
        'FastingBS': [FastingBS],
        'MaxHR': [MaxHR],
        'Sex_M': [Sex_M], 
        'ExerciseAngina_Y': [ExerciseAngina_Y], 
    })
    csv_filename = 'user_data.csv'

# Check if the file exists
    if not os.path.isfile(csv_filename):
        # Create a new file with header
        with open(csv_filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Sex_M', 'ExerciseAngina_Y'])

# Predict heart attack
# Example threshold value
# prediction, user_data = predict_heart_attack(Age, RestingBP, Cholesterol, FastingBS, MaxHR, Sex_M, ExerciseAngina_Y, RF_model, threshold)

# Write user data to CSV file
    with open(csv_filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([Age, RestingBP, Cholesterol, FastingBS, MaxHR, Sex_M, ExerciseAngina_Y])

# Print prediction result
# if prediction == 0:
#     print("The person is not likely to have a heart attack.")
# else:
#     print("The person is likely to have a heart attack.")
    prediction_proba = model.predict_proba(user_data)
    
    if prediction_proba[0][1] >= threshold:
        prediction = 1
    else:
        prediction = 0
    print(prediction) 
    if  prediction == 0:
        pass
    else:
        
        email='mustang061204@gmail.com'
        receiver_email=['pawaratharav2004@gmail.com','saniya.thigale22@pccoepune.org','sushantkabra2733@gmail.com']
        subject='This is from first aid kit'
        message='This is emergency for the heart attack for MrXYZ.'
        text=f"Subject:{subject}\n\n{message}"
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email,"mcsd nbls iyrx wbzz")
        server.sendmail(email,receiver_email,text)
        print("Email has been sent ")        
    return prediction, user_data
    


if __name__ == '__main__':
    app.run(debug=True)

