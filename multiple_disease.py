import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from db import *
import hashlib


if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
    st.session_state.logged_in_username = None


def logout():
    st.session_state.is_logged_in = False
    st.session_state.logged_in_username = None
    st.session_state.page = "Login"




# loading the saved models

diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open('heart_disease_model.sav','rb'))

parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))


# Define the different sections or pages as functions
def homepage():
    st.title('Home Page')
    st.write('Welcome to the Home Page.')
    st.write('Click the buttons below to navigate.')

def about_page():
    st.title('About Page')
    st.write('This is the About Page.')
    st.write('Click the buttons below to navigate.')



def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
        return False


# DB Management
conn = sqlite3.connect('test.db')
c = conn.cursor()


def add_userdata(username,password):
  c.execute('INSERT INTO users(username,password) VALUES (?,?)',(username,password))
  conn.commit()

def login_user(username,password):
  c.execute('SELECT * FROM users WHERE username =? AND password = ?',(username,password))
  data = c.fetchall()
  return data


def view_all_users():
  c.execute('SELECT * FROM users')
  data = c.fetchall()
  return data




def login():
    st.subheader("Login")
    if st.session_state.is_logged_in:
        st.image("images/icon.png", width=50)        
        st.write(f"Welcome {st.session_state.logged_in_username}")
        if st.button('Logout'):
            logout()
    else:
        username = st.text_input("User Name")
        password = st.text_input("Password", type='password')
        hashed_pswd = make_hashes(password)
        if st.button('LOGIN'):
            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.session_state.is_logged_in = True
                st.session_state.logged_in_username = username
                st.success("Logged In Successfully")
                st.subheader("User Profiles")
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result, columns=["ID", "Username", "Password"])
                st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")

        if st.button('Create an Account'):
            st.session_state.page = "SignUp"







# def login():
#     st.subheader("Login")
#     username = st.text_input("User Name")
#     password = st.text_input("Password",type='password')
#     if st.button('LOGIN'):
      
#         # if password == '12345':
#         login_user(username,password)
#         hashed_pswd = make_hashes(password)

#         result = login_user(username,check_hashes(password,hashed_pswd))
#         if result:
#             st.session_state.is_logged_in = True
#             st.session_state.logged_in_username = username  # Store the logged-in username
#             st.success("Logged In Successfully")

#             if st.session_state.is_logged_in:
#                 st.write(f"Logged In as {st.session_state.logged_in_username}")

#             st.subheader("User Profiles")
#             user_result = view_all_users()
#             clean_db = pd.DataFrame(user_result,columns=["ID","Username","Password"])
#             st.dataframe(clean_db)
#         else:
#             st.warning("Incorrect Username/Password")\
    
#     if st.button('Create an Account'):
#         st.session_state.page = "SignUp"  

     
    

def signup():
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password",type='password')

    if st.button("Signup"):
        if not new_user or not new_password:
            st.error("Both username and password are required.")
        else:      
            # add_userdata(username,password)
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

    if st.button("Already have account"):
        st.session_state.page = "Login"  




def contact_page():
    st.write('You can reach us at contact@example.com.')
    st.write('Click the buttons below to navigate.')

def prediction_page():
    st.title('Test Page')
    st.write('You can reach us at contact@example.com.')
    st.write('Click the buttons below to navigate.')








# sidebar for navigation
with st.sidebar:

    if st.session_state.is_logged_in:
            st.image("images/icon1.png", width=40) 
            st.write(f"Hey {st.session_state.logged_in_username}") 

    selected = option_menu('Multiple Disease Prediction System',
                          
                          ['Home', 
                           'About Us',
                           'User Login',
                            'Contact Us', 
                            'Prediction'],
                          icons=['house','info','phone','lightbulb'],
                          default_index=0)
    
    







# Create links to switch between pages based on the selected_page
if (selected == 'Home'):
    
    if st.session_state.is_logged_in:
            st.image("images/icon.png", width=50) 
            st.write(f"Hey {st.session_state.logged_in_username}") 
    # Explanation    
    st.header("Multiple Diseases Prediction:")
    st.image("images/image1.jpg", use_column_width=True)
    st.write("Multiple diseases prediction is the process of using machine learning models to predict the likelihood of various health conditions or diseases based on input data and patient information.")
    
    st.write("Our app is designed to demonstrate the concept of multiple diseases prediction using machine learning models.")
    st.header("Diabetes Prediction:")
    st.image("images/diabetes.jpg", width=300)
    st.write("Diabetes prediction involves using machine learning models to assess the likelihood of an individual developing diabetes based on various factors, such as their medical history, lifestyle, and genetic predisposition. By analyzing relevant data, these models can provide early detection and risk assessment, leading to better management and prevention strategies for diabetes.")


    st.header("Heart Disease Prediction:")
    st.image("images/heart.jpg", width=300)
    st.write("Heart disease prediction employs machine learning to estimate the probability of an individual experiencing heart-related conditions. Factors like cholesterol levels, blood pressure, and family history are considered in these predictions. Early detection through machine learning can aid in timely interventions and lifestyle changes to reduce the risk of heart disease.")


    st.header("Parkinson's Disease Prediction:")
    st.image("images/parkinsons.jpg")
    st.write("Parkinson's disease prediction utilizes advanced algorithms to evaluate the probability of an individual developing Parkinson's disease. These algorithms analyze factors such as age, tremors, and other neurological symptoms. Early prediction allows for better patient care, medication management, and potential disease-modifying treatments.")

    st.image("images/doc.jpg", width=200)
    st.write("So,")
    st.write("In each of these prediction scenarios, machine learning models play a crucial role in leveraging data to provide insights into health conditions. These predictions can contribute to more effective healthcare management and improved patient outcomes.")

elif (selected == 'About Us'):

    if st.session_state.is_logged_in:
            st.image("images/icon.png", width=50) 
            st.write(f"Hey {st.session_state.logged_in_username}") 
    st.title("ABOUT US")
    st.image("images/group.jpg", use_column_width=True)
    st.write("Contact:") 
    st.write("Aayush: pokharelaayush2@gmail.com")
    st.write("Sagar : dbijay1234@gmail.com")
    st.write("Roshan: shrestharoshan308@gmail.com")
    # Title and Description
    st.header("Multiple Diseases Prediction")

    st.header("Our app Work:")
    st.write("1. Data Collection: Relevant data, such as patient medical history and test results, is collected and prepared for analysis.")
    st.write("2. Feature Engineering: Features (variables) are selected and engineered to represent key information for disease prediction.")
    st.write("3. Model Training: Machine learning models are trained on historical data to learn patterns and relationships between features and disease outcomes.")
    st.write("4. Prediction: The trained models are used to make predictions for new, unseen data.")
    st.write("5. Interpretation: Predictions are interpreted to assess the likelihood of each disease.")

    st.header("This is important because:")
    st.write("Multiple diseases prediction has various applications in healthcare, including:")
    st.markdown("- Early disease detection and diagnosis.")
    st.markdown("- Personalized treatment recommendations.")
    st.markdown("- Disease risk assessment for patients.")
    st.markdown("- Healthcare resource allocation.")
    st.markdown("- Medical research and epidemiology.")

    st.header("About This App")
    st.write("This Streamlit app serves as a simple demonstration of multiple diseases prediction. It includes a basic user interface for selecting a prediction task (e.g., Diabetes, Heart Disease, or Parkinson's) and provides explanations for each task.")









elif (selected == 'User Login'):
    if "page" not in st.session_state:
        st.session_state.page = "Login"
    
    if st.session_state.page == "SignUp":
        signup()
    elif st.session_state.page == "Login":
        login()






elif (selected == 'Contact Us'):

    if st.session_state.is_logged_in:
            st.image("images/icon.png", width=50) 
            st.write(f"Hey {st.session_state.logged_in_username}")

    st.title("Contact Us")
    # Create form inputs
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    submitted = st.button("Submit")

    contacts = ''

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # Handle form submission
    if submitted:
        if name and email and phone and subject and message:
           
            cursor.execute('''
                INSERT INTO feedback(name, email, phone, subject, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, phone, subject, message))
            conn.commit()
            conn.close()
            st.success("Message sent successfully!")
        else:
            st.error("Please fill out all required fields before submitting.")






elif selected == "Prediction":

    if st.session_state.is_logged_in:
            st.image("images/icon.png", width=50) 
            st.write(f"Hey {st.session_state.logged_in_username}") 

    selected = st.selectbox("Medical Condition Prediction",
                          
                          ['Choose Option', 
                           'Diabetes Prediction',
                           'Heart Disease Prediction',
                           'Parkinsons Prediction',])


    if st.session_state.is_logged_in:
        # if st.session_state.is_logged_in:
        #     st.image("images/icon.png", width=50) 
        #     st.write(f"Hey {st.session_state.logged_in_username}")    
        # Diabetes Prediction Page
        if (selected == 'Diabetes Prediction'):

            # if st.session_state.is_logged_in:
            #     st.write(f"Logged In as {st.session_state.logged_in_username}")
            
            # page title
            st.title('Diabetes Prediction using ML')
            
            
            # getting the input data from the user
            col1, col2, col3 = st.columns(3)
            
            with col1:
                max_value=20
                Pregnancies = st.number_input('Number of Pregnancies',value=0,  placeholder="number only", min_value=0, max_value=None, step=1, format='%d')
                # Check if the input exceeds the maximum value
                if Pregnancies > max_value:
                    st.error(f"Input value exceeds the maximum value of {max_value}. Please enter a smaller value.")
            
            
            
            with col2:
                Glucose = st.number_input('Glucose Level',value=None,  placeholder="number only", min_value=0, step=1, format='%d')
                


            with col3:
                BloodPressure = st.number_input('Blood Pressure value',value=None,  placeholder="number only", min_value=0, step=1, format='%d')
            
            with col1:
                SkinThickness = st.number_input('Skin Thickness value',value=None,  placeholder="number only", min_value=0, step=1, format='%d')
            
            with col2:
                Insulin = st.number_input('Insulin Level',value=None,  placeholder="number only", min_value=0, step=1, format='%d')
            
            with col3:
                BMI = st.number_input('BMI value',value=None,  placeholder="number only", min_value=0.0, step=0.1)
            
            with col1:
                DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function value',value=None,  placeholder="number only", min_value=0.0, step=0.1)
            
            with col2:
                Age = st.number_input('Age of the Person',value=None,  placeholder="number only", min_value=0, step=1, format='%d')
            
            
            # code for Prediction
            diab_diagnosis = ''
            
            # creating a button for Prediction
            
            if st.button('Diabetes Test Result'):
                if (
                    Pregnancies is not None and
                    Glucose is not None and
                    BloodPressure is not None and
                    SkinThickness is not None and
                    Insulin is not None and
                    BMI is not None and
                    DiabetesPedigreeFunction is not None and
                    Age is not None
                ):
                    diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
                    
                    if (diab_prediction[0] == 1):
                    
                        diab_diagnosis = 'The person is diabetic'
                    else:
                        diab_diagnosis = 'The person is not diabetic'
                # After getting the prediction result
                    # Insert the data into the database
                    conn = sqlite3.connect('test.db')
                    cursor = conn.cursor()

                    cursor.execute('''
                        INSERT INTO Diabetes (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Prediction)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, diab_diagnosis))

                    conn.commit()
                    conn.close()   
                    st.success(diab_diagnosis)
                else:
                    st.warning('All Fields are Required.')



        # Heart Disease Prediction Page
        if (selected == 'Heart Disease Prediction'):
           
            
            # page title
            st.title('Heart Disease Prediction using ML')
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                age = st.number_input('Age',value=None,  placeholder="number only", min_value=0, step=1, format='%d')
                
                
                
            with col2:
                # Define a list of valid sex options
                valid_sex_options = ['',0, 1]
                
            
                # Create a selectbox widget for the 'sex' input
                sex = st.selectbox("Select Sex", valid_sex_options)
                # Validate the selected sex
                if sex not in valid_sex_options:
                    st.error("Please select a valid sex option.")
                else:
                    st.empty()
                        


            with col3:
                valid_cp_options = ['',0, 1,2,3]
                cp = st.selectbox("Chest Pain Type", valid_cp_options)
                    # Validate the selected sex
                if cp not in valid_cp_options:
                    st.error("Please select a valid cp option.")
                else:
                    st.empty()
                        


                
                
            with col1:
                trestbps = st.number_input('Resting Blood Pressure',value=None,  placeholder="number only", min_value=0, step=1, format='%d')
                
                
            with col2:
                chol = st.number_input('Serum Cholestoral in mg/dl',value=None,  placeholder="number only", min_value=0, step=1, format='%d')
                

            with col3:
                valid_fbs_options = ['',0, 1]
                fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", valid_fbs_options)
                    # Validate the selected sex
                if fbs not in valid_fbs_options:
                    st.error("Please select a valid fbs option.")
                else:
                    st.empty()
                        
                
            with col1:
                valid_restecg_options = ['',0, 1]
                restecg = st.selectbox("Resting Electrocardiographic results", valid_restecg_options)
                    # Validate the selected sex
                if restecg not in valid_restecg_options:
                    st.error("Please select a valid restecg option.")
                else:
                    st.empty()


            with col2:
                thalach = st.number_input('Maximum Heart Rate achieved',value=None,  placeholder="number only", min_value=0, step=1, format='%d')
                
            with col3:
                
                valid_exang_options = ['',0, 1]
                exang = st.selectbox("Exercise Induced Angina", valid_exang_options)
                    # Validate the selected sex
                if exang not in valid_exang_options:
                    st.error("Please select a valid exang option.")
                else:
                    st.empty()
                
            with col1:
                oldpeak = st.number_input('ST depression induced by exercise',value=None,  placeholder="number only", min_value=0.0, step=0.1)
                
            with col2:
                valid_slope_options = ['',0, 1, 2]
                slope = st.selectbox("Slope of the peak exercise ST segment", valid_slope_options)
                    # Validate the selected sex
                if slope not in valid_slope_options:
                    st.error("Please select a valid slope option.")
                else:
                    st.empty()
                
                
            with col3:
                valid_ca_options = ['',0, 1, 2]
                ca = st.selectbox("Major vessels colored by flourosopy", valid_ca_options)
                    # Validate the selected sex
                if ca not in valid_ca_options:
                    st.error("Please select a valid ca option.")
                else:
                    st.empty()
                
            with col1:
                valid_thal_options = ['',0, 1, 2, 3]
                thal = st.selectbox("thal: 0 = normal; 1 = fixed defect; 2 = reversable defect", valid_thal_options)
                    # Validate the selected sex
                if thal not in valid_thal_options:
                    st.error("Please select a valid thal option.")
                else:
                    st.empty()


                


            if st.button('Heart Disease Test Result'): 
                
                if (
                    age is not None and
                    sex is not None and
                    cp is not None and
                    trestbps is not None and
                    chol is not None and
                    fbs is not None and
                    restecg is not None and
                    thalach is not None and
                    exang is not None and
                    oldpeak is not None and
                    slope is not None and
                    ca is not None and
                    thal is not None 
                ):
                        
                    
                    # code for Prediction
                    heart_diagnosis = ''
                    
                    # creating a button for Prediction
                    
                    # if st.button('Heart Disease Test Result'):
                        # heart_prediction = heart_disease_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg,thalach,exang,oldpeak,slope,ca,thal]])                          
                        # input_data_as_numpy_array=np.array(heart_prediction, dtype=np.float64)
                    
                        # Convert input values to a NumPy array with a specific data type (e.g., float64)
                    heart_prediction = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]], dtype=np.float64)

                        # Now, you can use input_data for prediction
                    heart_prediction = heart_disease_model.predict(heart_prediction)

                    if (heart_prediction[0] == 1):
                        heart_diagnosis = 'The person is having heart disease'
                    else:
                        heart_diagnosis = 'The person does not have any heart disease'


                    
                        #   if (selected == 'Heart Disease Prediction'):
                    # ... (your existing code for input and prediction)

                    # After getting the prediction result
                    # Insert the data into the database
                    conn = sqlite3.connect('test.db')
                    cursor = conn.cursor()

                    cursor.execute('''
                        INSERT INTO Heart (Age, Sex, ChestPainTypes, RestingBloodPressure, SerumCholestoral, FastingBloodSugar, RestingECG,
                        MaxHeartRateAchieved, ExerciseInducedAngina, STDepression, Slope, MajorVesselsColored, Thal, Prediction)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, heart_diagnosis))

                    conn.commit()
                    conn.close()
                        
                    st.success(heart_diagnosis)
                else:
                    st.warning('All Fields are Required.')
                
                    
                # Clear input values
                    age = None
                    sex = ''
                    cp = ''
                    trestbps = None
                    chol = None
                    fbs = ''
                    restecg = ''
                    thalach = None
                    exang = ''
                    oldpeak = None
                    slope = ''
                    ca = ''
                    thal = ''    
                




            

        # Parkinson's Prediction Page
        if (selected == "Parkinsons Prediction"):


            
            # page title
            st.title("Parkinson's Disease Prediction using ML")
            
            col1, col2, col3, col4, col5 = st.columns(5)  
            
            with col1:
                fo = st.number_input('MDVP:Fo(Hz)',value=None,  placeholder="number only", min_value=0.0, step=0.0001,format='%0.4f')
                
                

            with col2:
                fhi = st.number_input('MDVP:Fhi(Hz)',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col3:
                flo = st.number_input('MDVP:Flo(Hz)',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col4:
                Jitter_percent = st.number_input('MDVP:Jitter(%)',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col5:
                Jitter_Abs = st.number_input('MDVP:Jitter(Abs)',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col1:
                RAP = st.number_input('MDVP:RAP',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col2:
                PPQ = st.number_input('MDVP:PPQ',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col3:
                DDP = st.number_input('Jitter:DDP',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col4:
                Shimmer = st.number_input('MDVP:Shimmer',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col5:
                Shimmer_dB = st.number_input('MDVP:Shimmer(dB)',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col1:
                APQ3 = st.number_input('Shimmer:APQ3',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col2:
                APQ5 = st.number_input('Shimmer:APQ5',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col3:
                APQ = st.number_input('MDVP:APQ',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col4:
                DDA = st.number_input('Shimmer:DDA',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col5:
                NHR = st.number_input('NHR',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col1:
                HNR = st.number_input('HNR',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col2:
                RPDE = st.number_input('RPDE',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col3:
                DFA = st.number_input('DFA',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col4:
                spread1 = st.number_input('spread1',value=None,  placeholder="number only", min_value=-1000.0, step=0.1,format='%0.4f')
                
            with col5:
                spread2 = st.number_input('spread2',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col1:
                D2 = st.number_input('D2',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                
            with col2:
                PPE = st.number_input('PPE',value=None,  placeholder="number only", min_value=0.0, step=0.1,format='%0.4f')
                






            
            
            # code for Prediction
            parkinsons_diagnosis = ''
            
            # creating a button for Prediction    
            if st.button("Parkinson's Test Result"):

                if (
                    fo is not None and
                    fhi is not None and
                    flo is not None and
                    Jitter_percent is not None and
                    Jitter_Abs is not None and
                    RAP is not None and
                    PPQ is not None and
                    DDP is not None and
                    Shimmer is not None and
                    Shimmer_dB is not None and
                    APQ3 is not None and
                    APQ5 is not None and
                    APQ is not None and
                    DDA is not None and
                    NHR is not None and
                    HNR is not None and
                    RPDE is not None and
                    DFA is not None and
                    spread1 is not None and
                    spread2 is not None and
                    D2 is not None and
                    PPE is not None




                    
                ):
                    parkinsons_prediction = parkinsons_model.predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ,DDP,Shimmer,Shimmer_dB,APQ3,APQ5,APQ,DDA,NHR,HNR,RPDE,DFA,spread1,spread2,D2,PPE]])                          
                    
                    if (parkinsons_prediction[0] == 1):
                        parkinsons_diagnosis = "The person has Parkinson's disease"
                    else:
                        parkinsons_diagnosis = "The person does not have Parkinson's disease"
                    

                    # After getting the prediction result
                    # Insert the data into the database
                    conn = sqlite3.connect('test.db')
                    cursor = conn.cursor()

                    cursor.execute('''
                        INSERT INTO parkinson (
                            MDVP_Fo_Hz,
                            MDVP_Fhi_Hz,
                            MDVP_Flo_Hz,
                            MDVP_Jitter_percent,
                            MDVP_Jitter_Abs,
                            MDVP_RAP,
                            MDVP_PPQ,
                            Jitter_DDP,
                            MDVP_Shimmer,
                            MDVP_Shimmer_dB,
                            Shimmer_APQ3,
                            Shimmer_APQ5,
                            MDVP_APQ,
                            Shimmer_DDA,
                            NHR,
                            HNR,
                            RPDE,
                            DFA,
                            spread1,
                            spread2,
                            D2,
                            PPE,
                            Prediction
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
                    ''', (fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE, parkinsons_diagnosis))

                    conn.commit()
                    conn.close()
                    st.success(parkinsons_diagnosis)
                else:
                    st.warning('All Fields are Required.')




        if st.session_state.is_logged_in:
            if st.button("Logout"):
                logout()



    else:
        st.warning('Please Login First!!!')


