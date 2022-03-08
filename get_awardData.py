import os
import json

#Clear console
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

#setup json file
jsonFile = open("awardData.json", "w")

#create lists
awardData = []
typeBig = ["Gosanke", "Non-Gosanke A", "Non-Gosanke B"]
typeSmall = ["Winner", "1st Runner up", "2nd Runner up"]
typeAward = ["Mature", "Adult", "Young", "Baby", "Mini"]
typeSize = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
typeSize.sort(reverse = True)
typeSpecies = ["Kohaku", "Taisho Sanshoku", "Showa Sanshoku", "Shiro and Bekko", "Tancho", "Goshiki", "Koromo", "Hikari Utsurimono and Hikari Moyomono", "Kawarimono", "Ginrin A (Gosanke)", "Utsurimono", "Asagi", "Shusui", "Hikari Mujimono", "Mujimono", "Doitsugoi", "Ginrin B (All Non-Gosanke)", "Male Kohaku", "Male Sanke", "Male Showa"]

#Declare misc var

#Functioins
def addAward(name, aType, size, cType, kType = 0):
    awJson = {
    'id': len(awardData)+1,
    'name': name,
    'awardType': aType,
    'koiSize': size,
    'koiType': kType,
    'cerType': cType,
    'status': 'uncheck'
    }
    print(awJson)
    awardData.append(awJson)
    return

#Adding award
cerType = 1

##Champion
addAward("Grand Champion", "Grand Champion", "", cerType)
for i in range(len(typeBig)):
    name = "%s Champion"%(typeBig[i])
    addAward(name, name, "", cerType)
addAward("Male Champion", "Male Champion", "", cerType)
addAward("Local Breed Champion", "Local Breed Champion", "", cerType)

##Mature Adult Young Baby Mini Champion
for i in range(len(typeAward)):
    for j in range(len(typeBig)):
        name = "%s %s Champion"%(typeAward[i], typeBig[j])
        addAward(name, name, "", cerType)
    if i < 2:
        name = "%s Male Champion"%(typeAward[i])
        addAward(name, name, "", cerType)

##ETC
addAward("The Most Unique Koi", "The Most Unique Koi", "", cerType)
addAward("TKKG Chiangmai Award", "TKKG Chiangmai Award", "", cerType)

##Best in size
for i in range(len(typeBig)):
    for size in typeSize:
        name = "Best in Size %s %s Bu"%(typeBig[i], size)
        addAward(name, name, size, cerType)
    for size in typeSize:
        name = "Best in Size Male %s Bu"%(size)
        addAward(name, name, size, cerType)
for i in range(8):
    addAward("Best Local Breed", "Best Local Breed", "", cerType)

##Small award
cerType = 0
for award in typeSmall:
    for specie in typeSpecies:
        for size in typeSize:
            kType = typeSpecies.index(specie)+1
            name = f"{award} {specie} {size} Bu"
            addAward(name, award, size, cerType, kType)

#save to json file
jsonString = json.dumps(awardData)
jsonFile.write(jsonString)
jsonFile.close()

#exit
print("Exiting..")
os._exit(0)