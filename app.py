import streamlit as st
import pandas as pd

# Title
st.markdown("<h1 style='text-align: center; color: grey;'>Energy Consumption in Colombia</h1>", unsafe_allow_html=True)
st.write("This is an analysis of the energy consumption in Colombia. The data was extracted from the Colombian National Administrative Department of Statistics (DANE). And the participation of each energy plant can be found in this link: https://informeanual.xm.com.co/informe/pages/xm/21-generacion-por-recurso.html. I created a function using openai API to find the coordinates of each plant as ploted in the map below.")
code = '''def plant_coordinates(client, plant):
    # Prompt for the chat model
    prompt = 'Dame la ciudad y coordenadas de la siguiente planta de energía colombiana como un diccionario python de llaves city y coords (tebsa queda en Soledad):'
    # Add the vision response to the prompt
    message_content = str(prompt) + ' : "' + str(plant) + '"'
    # Send the request to the chat model
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
    {"role": "user", "content": message_content},
     ]
    )
    print(response)
    
    # Get the breeds and tokens used
    classification = response.choices[0].message.content
    
    return classification'''
st.code(code, language='python')

code_2 = '''for index, row in df_plants.iterrows():
    plant = row['Recurso Generación']
    errors = 0
    while True and errors <= 3:
        try:
            # Make the API call to get plant coordinates
            plant_json = plant_coordinates(client, plant)
            
            # Load JSON object into a dictionary  
            data_dict = json.loads(plant_json)

            # Extract latitude and longitude
            coordinates = data_dict['coords']
            city = data_dict['city']
            print(city, coordinates)

            # Update DataFrame with extracted data
            df_plants.at[index, 'City'] = city
            df_plants.at[index, 'Coordinates'] = coordinates
            
            # Exit the loop if JSON decoding succeeds
            break
        
        except json.JSONDecodeError as e:
            print(f"JSON decoding error for plant {plant}: {e}")
            errors += 1
            # Retry the API call after a delay
            time.sleep(1)
            
        except KeyError as e:
            print(f"KeyError for plant {plant}: {e}")
            errors += 1
            # Retry the API call after a delay
            time.sleep(1)
            
        except Exception as e:
            print(f"An unexpected error occurred for plant {plant}: {e}")
            errors += 1
            # Retry the API call after a delay
            time.sleep(1)
    
    # Add a delay between API calls to avoid overwhelming the server
    time.sleep(1)
'''
st.code(code_2, language='python')
# File uploader
st.write("The size of the circle represents the energy consumption of each plant. The green dots correspond to energy plants and their size to their contribution to the total energy, the purple dots are the nearest metereological stations")
map_df = pd.read_csv('data/map_df.csv')
st.map(map_df,
    latitude='latitude',
    longitude='longitude',
    size='size',
    color='color',
    zoom = 1)

st.write("By locating the nearest metereological stations to the energy plants, we can analyze the correlation between the energy consumption and the weather conditions. We take this data from the meteostat library, and create a weighted average of all the climate conditions available. The data per station looks like this ")
hourly_df = pd.read_csv('data/hourly_data_test.csv')
st.dataframe(hourly_df.head())
