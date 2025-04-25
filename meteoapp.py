from tkinter import *
import customtkinter 
import requests
from PIL import Image, ImageSequence
customtkinter.set_appearance_mode('dark')
def get_weather(city):
    API_KEY = "Your api key"  #Your Api Key
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',  
            'lang': 'it'       
        }
        
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description'].capitalize()
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            
            return f"Temperatura: {temp}°C\nCondizioni: {description}\nUmidità: {humidity}%\nVento: {wind} km/h"
        elif response.status_code == 401:
            return "Errore: API Key non valida o scaduta"
        elif response.status_code == 404:
            return "Errore: Città non trovata"
        else:
            return f"Errore API: {data.get('message', 'Codice errore ' + str(response.status_code))}"
    
    except requests.exceptions.RequestException as e:
        return f"Errore di rete: {str(e)}"
    except Exception as e:
        return f"Errore imprevisto: {str(e)}"
window = customtkinter.CTk()
window.geometry("600x650")
window.resizable(False,False)
window.columnconfigure(0,weight=1)
window.config(bg="black")


gif_path = "C:\\Users\\salva\\Downloads\\sakrim.gif"
gif = Image.open(gif_path)
numeri = "1234567890?^'|!£$%€&/()=?^-.,;:_"

frames = []
for frame in ImageSequence.Iterator(gif):
    frames.append(customtkinter.CTkImage(light_image=frame.copy(),size=(400, 400)))
def invio(event):
    utente = entry.get().strip()  
    if utente == "":
        libel.configure(text="Inserire il nome di una città", text_color="red")
    elif any(i in numeri for i in utente):
        libel.configure(text="Non usare numeri o caratteri speciali", text_color="red")
    else:
        libel.configure(text="Caricamento...", text_color="white")  
        window.update()  
        weather_info = get_weather(utente)
        libel.configure(text=weather_info, 
                       text_color=("red" if "Errore" in weather_info else "white"))
    
        

label = customtkinter.CTkLabel(window, text="",bg_color="black",fg_color="black")
label.pack()
frame = customtkinter.CTkFrame(master=window,bg_color="black",fg_color="black",width=400,height=400)
frame.pack(padx=40,pady=10)
lobel = customtkinter.CTkLabel(master=frame,text="Inserire una citta : ",font=("Arial",30))
lobel.pack(padx=45,pady=2)
entry = customtkinter.CTkEntry(master=frame,placeholder_text="Inserire la citta",font=("Arial",15),width=250)
entry.pack(padx=45,pady=10)
libel = customtkinter.CTkLabel(master=frame,text="",fg_color="black",bg_color="black")
libel.pack(padx=45,pady=10)
button = customtkinter.CTkButton(master=frame,text="Cerca",fg_color="red",command=invio)
button.pack(padx=45,pady=12)
window.bind("<Return>",invio)

def animate(frame_num=0):
    frame_num = (frame_num + 1) % len(frames)
    label.configure(image=frames[frame_num])
    window.after(10, animate, frame_num)  

animate()  
window.mainloop()
