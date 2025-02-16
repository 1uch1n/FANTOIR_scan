# Author: 1uch1n (1uch1n@protonmail.com)
# Creation date: 04/11/2021
# Last update: 14/02/2022
# Description: Python script counting the number of occurences for each street names in France
# Objective: Revealing how many Neruda streets there are
# Source: France Open Data plaform data.gouv.fr, "FANTOIR" file
# https://www.data.gouv.fr/fr/datasets/fichier-fantoir-des-voies-et-lieux-dits/
# The FANTOIR file is an ASCII file, with approximately 120 characters per line
# Each line may be either: a city, a street, a county
# Documentation about FANTOIR file: https://www.data.gouv.fr/fr/datasets/r/7c52d813-1e98-4772-8a7a-6a01f9d30c6e

import nltk
import csv
import time
import os

# Fetch updated data on street names and population in France
print('Download latest data at:'
'FANTOIR ("Fichier national FANTOIR (situation """MONTH YEAR""").zip"):\nhttps://www.data.gouv.fr/fr/datasets/fichier-fantoir-des-voies-et-lieux-dits/'
'INSEE ("""ensemble.zip""" / """donnees_communes.csv"""):\nhttps://www.insee.fr/fr/statistiques/6011070?sommaire=6011075#consulter')

# specify the location of the FANTOIR and file
repertory = input('Copy/paste the path to FANTOIR and INSEE files:\n->')
https://www.data.gouv.fr/fr/datasets/fichier-fantoir-des-voies-et-lieux-dits/
os.chdir(repertory)
file_name = "FANTOIR0721" # ASCII file
INSEE_file = "PopCommunesINSEE.csv" # CSV file


# French public administration sometime use the so-called "Rivoli code" to identity cities
# Cf. FANTOIR documentation at https://data.economie.gouv.fr/api/datasets/1.0/fichier-fantoir-des-voies-et-lieux-dits/attachments/descriptif_du_fichier_national_fantoir_pdf

class Rivoli:
    '''detect whether the Rivoli code is corresponding to a region, a city or a street and return the appropriate output'''

    def __init__(self, line):
        # ignore the "Rivoli key" at line[11]
        self.rivoli_code = line[:10].strip()

        # extract the INSEE city codifiction
        # that is, the county key (2 firts characters) and the city key (4th/5th/6th characters)
        # the 3rd character ("direction key") at line[2] must be ignored
        self.city_code = line[:2] + line[3:6]

        # extract the complete street name
        # relevant only if it's a street line
        self.complete_name = line[11:33].strip()

        # extract the shortened street name
        # which starts at the 122nd character and ends at the end of the line regardless of its size
        # relevant only if it's a street line
        self.short_name = line[112:].strip()

        # extract the city name
        # relevant only if it's a city line
        self.city_name = line[11:42].strip()


class Population:
    '''open INSEE csv file with all city codes and respective populations'''

    def __init__(self, line):

        self.sep_line = line.split(sep=";", maxsplit=4)
        self.city_code = self.sep_line[0]
        self.city_name = self.sep_line[1]
        self.pop_count = self.sep_line[4]



def add_population():
    '''create a dictionnary {city name: city population} for all cities in France'''

    cityNpop = {}
    with open(INSEE_file, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            line = Population(row[0])
            cityNpop[line.city_code] = line.pop_count
    return cityNpop




def write_file(itr):
    '''write a csv file adding INSEE population data to selected FANTOIR street names data'''
    file_name = input(f"Choose a file name\n ->") + ".csv"
    try:
        iter(itr)
    except TypeError as te:
        print(f"{itr} is not iterable")
        return None
    else:
        print(f"{itr} is iterable")
        # checking if input is a list, that can be added with write row
        with open(file_name, "w", newline='') as file:
            writer = csv.writer(file)
            # For the output Neruda_list, which is a list of dictionnaries
            if isinstance(itr,list):
                first_row = ["City code", "City name", "Population", "Short name", "Complete name"]
                writer.writerow(first_row)
                for elem in itr:
                    if isinstance(elem,dict):
                        writer.writerow([elem["City code"], elem["City name"], elem["Population"], elem["Short name"], elem["Complete name"]])
            # For the output Street_list, which is a dictionnary
            elif isinstance(itr, dict):
                for elemt in itr.items():
                    writer.writerow(elemt)
            else:
                print(f"{itr} is not a list nor a dict")
        return print(f"The csv file {file_name} has been created in the repertory {repertory}")



# Set empty variables to create future outputs
city_nb = 0
city_dict = {}
street_nb = 0
street_dict = {}
neruda_list = []


def fantoir_scan(file):
    '''open FANTOIR file and sort all lines through a loop:
        - identify if the line corresponds to a city or a street
        - put them in their respective dictionnaries (city_dict or street_dict)
        - check if there's some Neruda in there to put it in a separate list'''

    start_time = time.time()
    with open(file, "r", encoding="ASCII") as f:

        for line in iter(lambda: f.readline(), ""):

            new_line = Rivoli(line)

            # CITY LINE
            if len(new_line.rivoli_code) == 6 and new_line.rivoli_code.isalnum():  # then it's a city line
                print("\nit's a CITY line")
                global city_nb
                city_nb += 1

                # list of the names of city by their INSEE code
                if new_line.city_code not in city_dict:
                    city_dict[new_line.city_code] = new_line.city_name
                    print(f"\nNouvelle entrée CITY:{new_line.city_name}, code {new_line.city_code}\n\n\n\n")


            # STREET LINE
            elif len(new_line.rivoli_code) == 10 and new_line.rivoli_code.isalnum():  # then it's a street line
                print("\nit's a STREET line")
                global street_nb
                street_nb += 1

                # count the number of streets with the same shortened name
                if new_line.short_name not in street_dict:
                    street_dict[new_line.short_name] = 1
                    print(f"\nNouvelle entrée STREET: {new_line.short_name}\n\n\n\n")
                else:
                    street_dict[new_line.short_name] += 1
                    print(f"\nOccurences pour {new_line.short_name} > +1\nTotal: {street_dict[new_line.short_name]}\n\n\n\n")

            # OTHER LINES
            else: # then it's probably a county line or something else
                print("\nIt's another kind of line.\nPASS!\n\n\n\n")
                pass

            # If Neruda is the line, store the result in a separate list
            if new_line.short_name == "NERUDA":
                neruda_line = {"City code": new_line.city_code, "City name": "NA", "Population": 0, "Short name": new_line.short_name, "Complete name": new_line.complete_name}
                global neruda_list
                neruda_list.append(neruda_line)
        end_time = time.time() - start_time
        print(f"\nFANTOIR Scan complete.\nTime taken: {end_time} seconds\n")
        f.close()











# List of questions to sets options to whether applying or not the options of the program

q = input("\nDo you want to launch Fantoir Scan?\n->")
if q.capitalize() == "Yes":
    fantoir_scan(file_name)

q2 = input("\nDo you want to know the number of cities and streets?\n->")
if q2.capitalize() == "Yes":
    print(f"\nNumber of cities: {city_nb}\nNumber of streets: {street_nb}")

q3 = input("\nDo you want to add city names in Neruda_list?\n->")
if q3.capitalize() == "Yes":
    for i in neruda_list:
        if i["City code"] in city_dict.keys():
            i["City name"] = city_dict[i["City code"]]

q4 = input("\nDo you want to add the population of cities to Neruda_list?\n->")
if q4.capitalize() == "Yes":
    ct_cnt = add_population()
    for i in neruda_list:
        if i["City code"] in ct_cnt.keys():
            i["Population"] = ct_cnt[i["City code"]]

q5 = input("\nDo you want to write a csv file with Neruda streets?\n->")
if q5.capitalize() == "Yes":
    write_file(neruda_list)
    print("Neruda file written")

q6 = input("\nDo you want to write a file with the number of occurences of each street\n->")
if q6.capitalize() == "Yes":
    q6bis = input("\nDo you want to delete streets that appear less than a number of times\n->")
    if q6bis.capitalize() == "Yes":
        number = int(input("Which number?"))
        for k in street_dict.copy():
            if street_dict[k] < number:
                del street_dict[k]
    # Sort dictionnary according to the number of streets
    sorted(street_dict.items(), key=lambda x: x[1], reverse=True)
    print(f"Street_dict is now type:  {type(street_dict)}")
    write_file(street_dict)
    print("Street file writen")
