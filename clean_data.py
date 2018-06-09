import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE_sample = "izmir_turkey.osm"
regex = re.compile(r'\b\S+\.?', re.IGNORECASE)

expected = [ "Izmir" , "Izkent" , "Sirinkapi", "Istikbal" , "Gaziosmanpasa", "University" ,"Coast" ,"Road", "Avenue","Airport","Street","Port","Boulevard", "Neighborhood" ,"Campus", "Square", "Shopping Center" ,"Highway"]  # expected names in the dataset

mapping = {"izmir" : "Izmir",
           "İzmir" : "Izmir",
           "sk." : "Street",
           "Sk." : "Street",
           "Sk" : "Street",
           "sk" : "Street",
           "Sokak" : "Street",
           "Sok." : "Street",
           "sokak" : "Street",
           "Sokağı" : "Street",
           "Sokak," : "Street",
           "Cd" : "Avenue",
           "Cd,": "Avenue",
           "cd" : "Avenue",
           "Cd." : "Avenue",
           "cd." : "Avenue",
           "Cad." : "Avenue",
           "Cad" : "Avenue",
           "Caddesi" : "Avenue",
           "caddesi" : "Avenue",
           "İ" : "I",
           "ı" : "i",
           "Ş" : "S",
           "ş" : "s",
           "ğ" : "g",
           "Havalimanı" : "Airport",
           "Havalımanı" : "Airport",
           "havalimanı" : "Airport",
           "Liman" : "Port",
           "liman": "Port",
           "Şirinyer" : "Sirinyer",
           "Bulvar" : "Boulevard",
           "Blv." : "Boulevard",
           "Bulv.": "Boulevard",
           "Bulvari" : "Boulevard",
           "bulvarı": "Boulevard",
           "Bulvarı": "Boulevard",
           "Mh" : "Neighborhood",
           "mh": "Neighborhood",
           "mahallesi": "Neighborhood",
           "Mahallesi": "Neighborhood",
           "Mah," : "Neighborhood",
           "Mah.": "Neighborhood",
           "Mh.," : "Neighborhood",
           "Kâhya" : "Kahya",
           "Yerleşkesi" : "Campus",
           "İzkent" : "Izkent",
           "İzkent," : "Izkent",
           "Meydanı" : "Square",
           "Meydan" : "Square",
           "Şirinkapı" : "Sirinkapi",
           "İstikbal" : "Istikbal",
           "Gaziosmanpaşa" : "Gaziosmanpasa",
           "sahil" : "Coast",
           "NilüferSokak" : "Nilufer Street",
           "Alışveriş Merkezi": "Shopping Center",
           "Paşa" : "Pasa" ,
           "Şehitleri" : "Sehitleri",
           "Çevre Yolu" : "Highway",
           "Üniversite" : "University"
           }

# Search string for the regex. If it is matched and not in the expected list then add this as a key to the set.
def audit_street(street_types, street_name):
    m = regex.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):  # Check if it is a street name
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):  # return the list that satify the above two functions
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street(street_types, tag.attrib['v'])

    return street_types


pprint.pprint(dict(audit(OSMFILE_sample)))  # print the existing names


def string_case(s):  # change string into titleCase except for UpperCase
    if s.isupper():
        return s
    else:
        return s.title()


# return the updated names
def update_name(name, mapping):
    name = name.split(' ')
    for i in range(len(name)):
        if name[i] in mapping:
            name[i] = mapping[name[i]]
            name[i] = string_case(name[i])
        else:
            name[i] = string_case(name[i])

    name = ' '.join(name)

    return name


update_street = audit(OSMFILE_sample)

# print the updated names
for street_type, ways in update_street.items():
    for name in ways:
        better_name = update_name(name, mapping)
        print (name, "=>", better_name)
