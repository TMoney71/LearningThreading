'''
Requirements
1. Write a multithreaded program that calls a local web server. The web server is 
   provided to you. It will return data about the Star Wars movies.
2. You will make 94 calls to the web server, using 94 threads to get the data.
3. Using a new thread each time, obtain a list of the characters, planets, 
   starships, vehicles, and species of the sixth Star War movie.
3. Use the provided print_film_details function to print out the data 
   (should look exactly like the "sample_output.txt file).
   
Questions:
1. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
    >
2. Review dictionaries (see https://isaaccomputerscience.org/concepts/dsa_datastruct_dictionary). How could a dictionary be used on this assignment to improve performance?
    >
'''


from datetime import datetime, timedelta
import time
import requests
import json
import threading


# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0

# class to get the datat from the api
class request_thread(threading.Thread):
    global call_count
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.response = {}

    def run(self):
        global call_count
        direct = requests.get(self.url)
        direct = direct.json()
        self.response = direct
        call_count += 1 

        
        # print(self.response)
# this is to get the dict form the api for each of the variables
def fech(data):
    fech_list = []
    # print(data)
    for i in data:
        # print(i)
        new_data = request_thread(i)
        # print(new_data)
        fech_list.append(new_data)
    for i in fech_list:
        i.start()
    # print(fech_list)

    # for i in fech_list:
    #     i.join()
        
    return fech_list
    



# def collections():





# fuction to print all the thing that are in the api I could not find char so that is why it is comited out
def print_film_details(film, chars, planets, starships, vehicles, species):
    '''
    Print out the film details in a formatted way
    '''
    
    def display_names(char, name_list):
        print('')
        print(f'{char}: {len(name_list)}')
        names = sorted([item for item in name_list])
        print(str(names)[1:-1].replace("'", ""))


    print('-' * 40)
    # print(f'char   : {film["char"]}')
    print(f'Director: {film["director"]}')
    print(f'Producer: {film["producer"]}')
    print(f'Released: {film["release_date"]}')

    display_names('Characters', chars)
    display_names('Planets', planets)
    display_names('Starships', starships)
    display_names('Vehicles', vehicles)
    display_names('Species', species)


def main():
    global call_count
    begin_time = time.perf_counter()


    # calling the api
    t1 = request_thread(TOP_API_URL+f'/films/6/')
    # getting the first bit of information
    t1.start()
    t1.join()

    data = t1.response
    # fech(data)

    # print(data)
   
    # seperating this info
    for i in data:
        if i == 'characters':
            characters = data.get(i)
        if i == 'planets':
            Planets = data.get(i)
        if i == 'starships':
            starships= data.get(i)
        if i == 'vehicles':
            Vehicles = data.get(i)
        if i == 'species':
            Species = data.get(i)

    # other = fech(data)
    # for t in film:
    #     t.join()
    # print(other)
    # print(chara)
    
    # finding the infromation for each thing 
    chara = []
    charas = fech(characters)
    for t in charas:
        t.join()
    
    for t in charas:
        charas = t.response['name']
        chara.append(charas)

    # characters = {'Characters' : chara}
    # print(characters)
        
    # finding the infromation for each thing 
    planets = []
    plan = fech(Planets)
    for t in plan:
        t.join()
    
    for t in plan:
        plan = t.response['name']
        planets.append(plan)
    # planet = {'Planets' : planets}
# finding the infromation for each thing 
    starship = []
    star = fech(starships)
    for t in star:
        t.join()

    for t in star:
        star = t.response['name']
        starship.append(star)
    # starsh = {'Starship' : starship}
# finding the infromation for each thing 
    vehicles = []
    vehi = fech(Vehicles)
    for t in vehi:
        t.join()

    for t in vehi:
        # print(t.response['name'])
        vehi = t.response['name']
        vehicles.append(vehi)
    # vehi = {'Vehicles' : vehicles}
# finding the infromation for each thing 
    species = [] 
    spec = fech(Species)
    for t in spec:
        t.join()
    for t in spec:
        spec = t.response['name']
        species.append(spec)
    # spec = {'Species' : species}
    



    print_film_details(data, chara, planets, starship, vehicles, species)


    # url_list = []
    # for character in data['characters']:
    #     url_list.append(character)
    # for planet in data['planets']:
    #     url_list.append(planet)
    # for starship in data['starships']:
    #     url_list.append(starship)
    # for vehicle in data['vehicles']:
    #     url_list.append(vehicle)
    # for species in data['species']:
    #     url_list.append(species)
    # print(url_list)
    
   
    


    
    

    print(f'There were {call_count} calls to the server')
    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)
    print(f'Total time = {total_time_str} sec')
    
    # If you do have a slow computer, then put a comment in your code about why you are changing
    # the total_time limit. Note: 90+ seconds means that you are not doing multithreading
    assert total_time < 15, "Unless you have a super slow computer, it should not take more than 15 seconds to get all the data."
    
    assert call_count == 93, "It should take exactly 94 threads to get all the data"
    # he said that this works because I did the call all at once
    

if __name__ == "__main__":
    main()
