# import libraries
import pickle 
import streamlit as st 
import pandas as pd
from pathlib import Path

# load some of our saved models using pickle

# label-encoder model pre-trained with feature names
le_path = Path(__file__).parents[0] / "Models/label_encoder.sav"
le = pickle.load(open(le_path,"rb"))

# random forest model pre-trained
forest_path = Path(__file__).parents[0] / "Models/model.sav"
forest_model = pickle.load(open(forest_path,"rb"))

# our functions

# prediction function
def satisfaction_prediction(input_data):
  prediction = forest_model.predict(input_data)
  
  if (prediction[0] == 0):
    return "The passenger is neutral or dissatisfied with their flight!"
  else:
    return "The passenger was satisfied with their flight!"
  
  
# label encode function  
def label_encode(data):
  # label encode our categorical variables 
  cat = ['Type of Travel', 'Class', 'Customer Type']

  for name in cat:
    data = data.copy()
    data[name] = le.fit_transform(data[name])
  return data
  
  
  
def main():

  # giving a title
  st.title("Airline Passenger Satisfaction ")
  # subheader
  st.subheader("Web App - Survey",)
  st.write("""This app predicts if a passenger was satisfied with their flight or not. Just fill in the following 
            information and click on the result button.""")
  
  
  st.write("""## Passenger Information:""")

  customer_type = st.selectbox("Are you a New Customer for this airline?",
                      ['Disloyal Customer','Loyal Customer'], index = 1)   
  st.write('You selected:', customer_type)
            
  type_travel = st.selectbox("What was the purpose of your flight?",
                      ["Personal Travel", "Business Travel"]) 
  st.write('You selected:', type_travel)
                      
  class1 = st.selectbox("What was the Class of your flight?",
                      ['Eco','Business','Eco Plus']) 
  st.write('You selected:', class1)
  
  st.write("""## Rate your Satisfaction Level (0-5) for the below Categories:""")
  st.write("""#### Where 0 represents least satisfactory and 5 being the most satisfactory""")
  
  st.write("""### Online Boarding""")
  online_boarding = st.radio("Satisfaction level for Online Boarding?", 
                      [0,1,2,3,4,5], horizontal=True)

  st.write("""### Inflight WIFI Service""")
  inflight_wifi = st.radio("Satisfaction level of the Inflight Wifi Service?",
                      [0,1,2,3,4,5], horizontal=True) 
  
  st.write("""### Inflight Entertainment""")
  entertainment = st.radio("Satisfaction level of the Inflight Entertainment?",
                      [0,1,2,3,4,5], horizontal=True) 

  st.write("""### Seat Comfort""")                   
  seat_comfort = st.radio("Satisfaction level of the Seat Comfort?",
                      [0,1,2,3,4,5], horizontal=True) 
  
  st.write("""### Ease of Online Booking""")                    
  online_booking = st.radio("Satisfaction level of Ease of making an Online Booking?",
                      [0,1,2,3,4,5], horizontal=True) 
  
  st.write("""### Leg Room Service""")                  
  leg_room = st.radio("How would you rate the Leg Room Service?",
                      [0,1,2,3,4,5], horizontal=True)    



  df_dict = {'Online boarding':online_boarding, 'Inflight wifi service':inflight_wifi, 
              'Type of Travel':type_travel, 'Class':class1, 'Inflight entertainment':entertainment,
            'Seat comfort':seat_comfort, 'Ease of Online booking':online_booking,
            'Leg room service': leg_room, 'Customer Type':customer_type}

  user_data = pd.DataFrame([df_dict])
  
  user_data = label_encode(user_data)
  
  Satisfaction = ''
  
  if st.button("Passenger Satisfaction Result"):
    Satisfaction = satisfaction_prediction(user_data)
    
    if Satisfaction == "The passenger is neutral or dissatisfied with their flight!":
      st.error(Satisfaction,icon="🚨")
    else:
      st.success(Satisfaction)
      st.balloons()
  
  

if __name__ == "__main__":
  main()