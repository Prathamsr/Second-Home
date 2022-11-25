import json
with open('static\javascript/insname.json','w') as f:
    json.dump(['Pratham','Neelam','Muskan','Jodhpur','jaipur','bikaner','delhi','indore'],f)
with open('static\javascript/insname.json','r') as f:
    l=json.load(f)
l.append('love')
