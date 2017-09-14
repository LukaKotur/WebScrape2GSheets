import pygsheets
from urllib.request import urlopen as uReq
import sys
import msvcrt
from bs4 import BeautifulSoup as soup
from time import sleep
import logging
import traceback

logging.basicConfig(filename='errorLog.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

igrice = ["Until Dawn", "Uncharted Collection", "Uncharted 4", "Crash Bandicoot", "Horizon Zero Dawn", "Last Of Us Remaster", "God Of War PS4", "Ni No Kuni", "Digimon", "Nioh", "Bloodborne", "Ratchet And Clank", "Kingdom Hearts", "Persona PS4", "Yakuza PS4" ]

def GetEurVrednost():
    nbs_kursna_lista = "https://www.nbs.rs/kursnaListaModul/srednjiKurs.faces?lang=lat"

    uKursna = uReq(nbs_kursna_lista)

    page_kursna = uKursna.read()

    uKursna.close()

    kursna_soup = soup(page_kursna, "html.parser")

    kursna_lista = kursna_soup.find_all("tbody", {"id": "index:srednjiKursList:tbody_element"})

    eur_row = kursna_lista[0].tr

    eur_td = eur_row.find_all('td')[4::5]

    eur_vrednost = eur_td[0].text

    eur_vrednost = eur_vrednost.split(".")[0]

    return eur_vrednost

#Creating Worksheets
# for igrica in igrice:
#     worksheet = sheet.add_worksheet(igrica)

# Clearing the slected worksheet and inserting into it

try:
    client = pygsheets.authorize(service_file='service_creds.json', no_cache=True)

    sheet = client.open('PS4 Igrice KupujemProdajem')

    for igrica in igrice:

        my_url = "https://www.kupujemprodajem.com/search.php?action=list&data[page]=1&data[ad_kind]=goods&data[category_id]=1036&data[group_id]=1039&data[order]=posted%20desc&submit[search]=Trazi&dummy=name&data[keywords]="+igrica.replace(" ", "%20")

        uClient = uReq(my_url)

        page_html = uClient.read()

        uClient.close()

        page_soup = soup(page_html, "html.parser")

        containers = page_soup.find_all("div", {"class": "item clearfix"})



        sortirana_lsita = []

        worksheet = sheet.worksheet_by_title(igrica)
        worksheet.clear()

        for container in containers:
            title_container = container.find_all("a",{"class":"adName"})
            ad_title = title_container[0].text.strip()
            url = 'www.kupujemprodajem.com/'+title_container[0]['href']
            price_container = container.find_all("span",{"class":"adPrice"})
            ad_price = price_container[0].text.strip().replace("€", "").replace("din", "").replace(".", "")
            ad_price = ad_price + "RSD"
            if "," in ad_price:
                ad_price = ad_price.split(',')[0]
                ad_price = str(int(ad_price) * int(GetEurVrednost())) + " RSD"
            if "Kontakt" in ad_price or "Kupujem" in ad_price or "Dogovor" in ad_price:
                ad_price = ad_price.replace("RSD", "")

            sortirana_lsita.append([ad_title,ad_price.strip(),url])

        fully_sorted = sorted(sortirana_lsita, key=lambda x: x[1])

        for item in fully_sorted:
            worksheet.append_table(values=[item[0], item[1], item[2]])
            print("Done " + item[0])
            sleep(1)

    print("Insert was successful!")

    print("Press any key to end the program.")
    while(True):
        if msvcrt.kbhit():
            sys.exit(0)
except BaseException as ex:
    logger.error(ex)