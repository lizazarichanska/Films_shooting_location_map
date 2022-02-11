# Films_shooting_location_map
This module creates an HTML map which shows closest to you lokations, where films were shot (in the specific year).
## It uses these libraries:
+ **argparse**
+ **folium**
+ **geopy**
## This map has three layers:
+ your given current location
+ all closest to you locations 
+ Marker Cluster (shows how many points are in some area)

We call [main.py](https://github.com/lizazarichanska/Films_shooting_location_map/blob/main/main.py) in the command line:
```python
python3 main.py 2016 49.817545 24.023932 locations1.list
```

were 1st positional argument is **year**(str); 
     2nd - **latitude**(float);
     3rd - **longitude**(float);
     4th - **path to data set**(str).

## Output
As a result, [map](https://github.com/lizazarichanska/Films_shooting_location_map/blob/main/Map1.html) looks like this:

<img width="590" alt="Screenshot 2022-02-11 at 21 59 49" src="https://user-images.githubusercontent.com/92580910/153661841-36c3bc3f-bc6b-49fc-be41-a8f69d13469b.png">

## Also, this map contains other features such as:
+ **Zoom Toggler**: is used to change the scale of the map;
+ **FullScreen Button**: is used to enter FullScreen mode;
+ **LayerControl Button**: is used to switch layers;
+ **MousePosition Button**: is used to show coordinates of your mouse while moving it.

Beside this, if you click on any spot, it will show you **the name of the film** that was shot there.
