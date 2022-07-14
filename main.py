from tkinter import *
import PIL
from PIL import ImageTk,Image
import math
import requests

window=Tk()

MAP_WIDTH=1200
MAP_HEIGHT=1200

MY_LAT=19.076090   #mumbai
MY_LONG=72.877426

response_iss=requests.get(url="http://api.open-notify.org/iss-now.json")
response_iss.raise_for_status()
iss_long=longitude=float(response_iss.json()["iss_position"]["longitude"])
iss_lat=latitude=float(response_iss.json()["iss_position"]["latitude"])



def degreesToRadians(degrees):
    return (degrees * math.pi) / 180;


def latLonToOffsets(latitude, longitude, mapWidth, mapHeight):
    FE = 180; # false easting
    radius = mapWidth / (2 * math.pi);
    latRad = degreesToRadians(latitude);
    lonRad = degreesToRadians(longitude + FE);

    x = lonRad * radius;

    yFromEquator = radius * math.log(math.tan(math.pi / 4 + latRad / 2));
    y = mapHeight / 2 - yFromEquator;

    return [x,y];


x_y=latLonToOffsets(MY_LAT,MY_LONG,MAP_WIDTH,MAP_HEIGHT)
iss_x_y=latLonToOffsets(iss_lat,iss_long,MAP_WIDTH,MAP_HEIGHT)

x=x_y[0]
y=x_y[1]

iss_x=iss_x_y[0]
iss_y=iss_x_y[1]

BACKGROUND_COLOR = "#B1DDC6"


window.title("ISS LOCATION")


map=PhotoImage(file="images/Mercator_projection.png")


canvas=Canvas(width=MAP_WIDTH,height=MAP_HEIGHT,bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.create_image(MAP_WIDTH/2,MAP_HEIGHT/2,image=map)
me=canvas.create_text(x,y,text="*",fill="yellow",font=("Ariel", 15, "bold"))
iss=canvas.create_text(iss_x,iss_y,text="*",fill="red",font=("Ariel", 15, "bold"))

rocket=Image.open("images/rocket.png")
rocket_resized=rocket.resize((40,40),Image.ANTIALIAS)
rocket_pic=ImageTk.PhotoImage(rocket_resized)

me=Image.open("images/me.png")
me_resized=me.resize((25,25),Image.ANTIALIAS)
me_pic=ImageTk.PhotoImage(me_resized)


canvas.create_image(iss_x,iss_y,image=rocket_pic)
canvas.create_image(x,y,image=me_pic)
canvas.pack()

window.mainloop()