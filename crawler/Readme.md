
# Scrapy is use to download data from Itra.run end Enduhub

Content-Type application/x-www-form-urlencoded

1. Brute force by id Itra page this find an event
https://itra.run/calend.php
raw Post  
mode=getEvt&id=124&annee=2019&opendirect=1  
**Create Event only Name is neaded**

2. Find div id="calevt_lst" end a elements with showEvt('124', '2019', '2533')  
    Third Params is id of race
3. Post for  race with a aditional param idc
https://itra.run/calend.php  
mode=getEvt&id=124&annee=2019&idc=2533&opendirect=1

4. Parce Response and get All Info about race  
**Create Race inside Event**
