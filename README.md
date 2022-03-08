# koishow.net Awards Reorder
There's a lot of awards in 1 koi show event. In the most recent koi show I take part of have around 700 awards.
And the process to add and reorder award is too much time consuming.

This project use to make automate those process

## Generate award data
get_awardData.py is use to create json file with every award data I need

Config every type of award I need
```python
#Koi Category
typeBig = ["Gosanke", "Non-Gosanke A", "Non-Gosanke B"]

#Major award
typeAward = ["Mature", "Adult", "Young", "Baby", "Mini"]

#Small award
typeSmall = ["Winner", "1st Runner up", "2nd Runner up"]

#Koi Size avaliable
typeSize = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65].sort(reverse = True)

#Koi species avaliable
typeSpecies = ["Kohaku", "Taisho Sanshoku", "Showa Sanshoku", "Shiro and Bekko", "Tancho", "Goshiki", "Koromo", "Hikari Utsurimono and Hikari Moyomono", "Kawarimono", "Ginrin A (Gosanke)", "Utsurimono", "Asagi", "Shusui", "Hikari Mujimono", "Mujimono", "Doitsugoi", "Ginrin B (All Non-Gosanke)", "Male Kohaku", "Male Sanke", "Male Showa"]
```

## Reorder and create new award if award not exist
After I got awardData.json from get_awardData.py I have to run post_awardReorder.py

This will, first check all awards that have status 'uncheck' if it avaliable or not
If it found, it will mark in json that it has been found
```python
for award in awardData:
        name = award['name']
        status = award['status']
        if status == "uncheck":
            try:
                driver.find_element(By.XPATH, f"//*[contains(text(), '{name}')]")
                award['status'] = "Found"
            except:
                award['status'] = "NotFound"
            saveJson()
```

Now it'll check and skip every award that already 'Done'.
If award status is 'Found' it'll check and reorder the award if needed and mark as 'Done'.
If award status is 'NotFound' it'll add new award, reorder it and mark as 'Done
```python
for award in awardData:
        print("======================")
        name = award['name']
        if award['status'] == "Done":
            continue
        elif award['status'] == "Found":
            # get required element process
            # check if order value matched the data
            if int(elValue) != int(award['id']):
                # reorder and save as 'Done' process
            else:
                # save as 'Done' process
        elif award['status'] == "NotFound":
            # Adding, reorder and save as 'Done' process
```
