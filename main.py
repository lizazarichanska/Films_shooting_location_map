import argparse
import folium 
from folium import plugins
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def file_to_list(file_path: str, year: str) -> list:
    """
    >>> file_to_list('locations1.list', '2016')[:4]
    [['"#ActorsLife"', 'New York City, New York, USA'], ['"#Fuga"', 'Barra da Tijuca, Rio de \\
    Janeiro, Rio de Janeiro, Brazil'], ['"#KillTorrey"', 'Burbank, California, USA'], \\
    ['"#LoveMyRoomie"', 'New York, USA']]
    """
    file_list = []
    with open(file_path) as file:
        for line in file:
            if line.startswith('"'):
                if year in line:
                    if '{' in line:
                        line = line[:line.find('{')] + line[line.rfind('}') + 1:]
                    line = line.strip().split('\t')
                    line = list(filter(lambda x: x != '', line))
                    if line[-1][-1] == ')':
                        line = line[:-1]
                    line[0] = line[0][:line[0].find('(')]
                    line = [item.strip() for item in line]
                    file_list.append(line)
    return file_list


def find_distance(films_list: list, latitude: float, longitude: float) -> dict:
    """
    >>> find_distance(file_to_list('locations1.list', '2016'), 49.817545, 24.023932)
    [('ActorsLife', [(40.7127281, -74.0060152), 7175.627849392481]), ('LoveMyRoomie', [(40.652600\\
        6, -73.9497211), 7176.9924040652395]), ('SmurTv', [(33.7489924, -84.3902644), 8364.990444\\
            96954]), ('MyCurrentSituation: Atlanta', [(35.1490215, -90.0516285), 8564.20727439586\\
                7]), ('VanLifeAttila', [(49.163168, -123.137414), 8571.35172685415]), ('KillTorre\\
                    y', [(34.1816482, -118.3258554), 9965.429964964662]), ('SpongeyLeaks', [(34.2\\
                        345615, -118.5369316), 9967.652164493427]), ('Fuga', [(-22.9979553, -43.3\\
                            7311472822825), 10455.260508910225])]
    """
    locator = Nominatim(user_agent='city')
    for city in films_list:
        city[1] = locator.geocode(city[1])
    films_list = list(filter(lambda x: x[1] != None, films_list))
    films_dict = {}
    for film in films_list:
        if film[0] not in films_dict:
            films_dict[film[0][2:-1]] = film[1][1]
        else:
            films_dict[film[0][2:-1]] = film[1][1]
    home_loc = (latitude, longitude)
    for film in films_dict:
        films_dict[film] = [films_dict[film], geodesic(home_loc, films_dict[film]).km]
    return sorted(films_dict.items(), key=lambda x: x[1][1])


def map(main_list: list, year: str, latitude: float, longitude: float, path_to_dataset: str):
    map = folium.Map(tiles='cartodbdark_matter', location=[latitude, longitude], zoom_start=10)
    feature_group = folium.FeatureGroup(name='Nearest movies locations')
    main_list = find_distance(file_to_list(path_to_dataset, year), latitude, longitude)
    for elem in main_list:
        feature_group.add_child(folium.Marker(location=[elem[1][0][0], elem[1][0][1]],
             popup=elem[0], icon=folium.Icon(icon='movie', color='orange')))
    map.add_child(feature_group)
    map.add_child(plugins.MousePosition(position='bottomleft', separator=' : ',
        empty_string='Unavailable', lng_first=False, num_digits=8, prefix=''))
    plugins.ScrollZoomToggler().add_to(map)
    map.add_child(plugins.MarkerCluster(locations=[x[1][0] for x in main_list], name='Marker Cluster'))
    plugins.Fullscreen(position='bottomright').add_to(map)
    feature_group_2 = folium.FeatureGroup(name='Your location')
    feature_group_2.add_child(folium.Marker(location=[latitude, longitude], popup='Your location',
                                icon=folium.Icon(color='lightgray', icon='blue')))
    map.add_child(feature_group_2)
    map.add_child(folium.LayerControl())
    map.save('Map1.html')


def main():
    parser = argparse.ArgumentParser(description='Change a substring to another one')
    parser.add_argument('year', type=str, help='Year, during which movies were shoot')
    parser.add_argument('latitude', type=float, help='Coordinate"s latitude of your current location')
    parser.add_argument('longitude', type=float, help='Coordinate"s longitude of your current location')
    parser.add_argument('path_to_dataset', type=str, help='The path to a file')
    args = parser.parse_args()
    file_lst = file_to_list(args.path_to_dataset, args.year)
    distance_list = find_distance(file_lst, args.latitude, args.longitude)
    map(distance_list, args.year, args.latitude, args.longitude, args.path_to_dataset)


if __name__ == "__main__":
    main()
