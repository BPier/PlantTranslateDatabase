from wikibaseintegrator import WikibaseIntegrator,wbi_helpers,wbi_login
from wikibaseintegrator.wbi_config import config as wbi_config
import csv
from deep_translator import (GoogleTranslator)

wbi = WikibaseIntegrator()
wbi_config['USER_AGENT'] = 'MyWikibaseBot/1.0 (https://www.wikidata.org/wiki/User:PlantName)'

def Translate(text_to_translate):
    if text_to_translate == "None known":
        return "Aucun Connu"
    else:
        return GoogleTranslator(source='en', target='fr').translate(text=text_to_translate)


class PlantWiki:
    def __init__(self, latin_name):
        wiki_item=self.Get_wiki_item(self.Search_wiki(latin_name))
        wiki_item=wiki_item.get_json()
        self.latin_name = latin_name
        self.aliases = self.Get_Aliases(wiki_item)
        self.commun_name = self.Get_CommonName(wiki_item)
        self.description = self.Get_Description(wiki_item)

    def merge_alias(self,new_alias):
        alias_list=[]
        for i in new_alias:
            alias_list.append(i['value'])
        return alias_list
    def Search_wiki(self,string):
        result_list = wbi_helpers.search_entities(string)
        return result_list[0]
    def Get_wiki_item(self,id):
        return wbi.item.get(entity_id=id)
    def Get_CommonName(self,wiki_item):
        Commun_Name = "Inconnu"
        if 'fr' in wiki_item['labels']:
            Commun_Name = wiki_item['labels']['fr']['value']
            if (Commun_Name == self.latin_name):
                if (self.aliases != None):
                    Commun_Name = self.aliases[0]
                else:
                   Commun_Name = None 
        return Commun_Name
    def Get_Description(self,wiki_item):
        if 'fr' in wiki_item['descriptions']:
            return wiki_item['descriptions']['fr']['value']
        else:
            "Inconnu"
    def Get_Aliases(self,wiki_item):
        if 'fr' in wiki_item['aliases']:
            return self.merge_alias(wiki_item['aliases']['fr']) 
        else:
            "Inconnu"
    def __str__(self):
        return f"Nom Latin : {self.latin_name}, Nom Commun : {self.commun_name}, Alias : {self.aliases}"

# CurrentPlantWiki = PlantWiki("Albies Alba")

# print(f"Description : {CurrentPlantWiki.description}")
# print(f"Label : {CurrentPlantWiki.label}")
# print(f"Aliases : {CurrentPlantWiki.aliases}")

with open('data/Database_Temperate_Example.csv',mode='r') as read_obj, \
    open('data/Database_Temperate_Example_FR.csv', 'w',newline='') as write_obj:
    csv_reader = csv.DictReader(read_obj)
    headers=['Latin name',
    'Family',
    'Common name','Common name_fr',
    'Habit',
    'Deciduous Evergreen',
    'Height',
    'Width',
    'UK Hardiness',
    'Medicinal','Medicinal_fr',
    'Range','Range_fr',
    'Habitat','Habitat_fr',
    'Soil',
    'Shade',
    'Moisture',
    'Well drained',
    'Nitrogen fixer',
    'pH',
    'Acid',
    'Alkaline',
    'Saline',
    'Wind',
    'Growth rate',
    'Pollution',
    'Poor soil',
    'Drought',
    'Wildlife',
    'Pollinators','Pollinators_fr',
    'Self fertile',
    'Known hazards','Known hazards_fr',
    'Synonyms','Synonyms_fr',
    'Cultivation details','Cultivation details_fr',
    'Edible uses','Edible uses_fr',
    'Uses notes',
    'Propagation',
    'Heavy clay',
    'EdibilityRating',
    'FrostTender',
    'Scented',
    'MedicinalRating',
    'Author'
]
    csv_writer = csv.DictWriter(write_obj,fieldnames=headers)
    csv_writer.writeheader() 
    for row in csv_reader:
        # print(row['Family'])
        CurrentPlantWiki = PlantWiki(row['Latin name'])
        row['Common name_fr']=CurrentPlantWiki.commun_name
        print(CurrentPlantWiki)
        # Medicinal
        row['Medicinal_fr']=Translate(row['Medicinal'])        
        # Range
        row['Range_fr']=Translate(row['Range'])        
        # Habitat
        row['Habitat_fr']=Translate(row['Habitat']) 
        # Pollinators
        row['Pollinators_fr']=Translate(row['Pollinators']) 
        # Known hazards
        row['Known hazards_fr']=Translate(row['Known hazards']) 
        # Cultivation details
        row['Cultivation details_fr']=Translate(row['Cultivation details'])
        # Edible uses
        row['Edible uses_fr']=Translate(row['Edible uses'])  
        # Range
        row['Range_fr']=Translate(row['Range'])
        # Synonyms
        row["Synonyms_fr"]=CurrentPlantWiki.aliases
        csv_writer.writerow(row)

# csv_en = pd.read_csv('data/Database_Temperate_Example.csv')
# print(csv_en.head()) 
# csv_input['Medicinal_fr'] = csv_input['Name']
# csv_input.to_csv('output.csv', index=False)

