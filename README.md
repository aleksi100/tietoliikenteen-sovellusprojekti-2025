# Tietoliikenteen sovellusprojekti 2025

Projektin tarkoituksena on siirtää kiihtyvyysanturidataa Nordic-mikrokontrollerilta Linux-palvelimella sijaitsevaan tietokantaan käyttäen välikappaleena Raspberry Pi -alustaa, johon data siirtyy BLE-teknologian avulla. Raspberry Pi välittää datan edelleen TCP-yhteyden kautta palvelimelle, jossa se tallennetaan MySQL-tietokantaan. Tietokannassa säilytettävä data käytetään  koneoppimismallin koulutukseen joka mahdollistaa Nordic-mikrokontrollerin oman asennon tunnistamisen.


### Arkkitehtuurikaava
<img width="1116" height="468" alt="kuva" src="https://github.com/user-attachments/assets/793420a6-4a7e-47b3-901c-4fab77f75f63" />


## Järjestelmän komponentit ja roolit

### Nordic-mikrokontrolleri
Nordic nRF5340-DK vastaa kiihtyvyysanturidatan mittaamisesta ja esikäsittelystä. Anturi tuottaa kiihtyvyysdataa kolmessa ulottuvuudessa (X, Y ja Z), joka kuvastaa laitteen asentoa ja liikettä. Data käsitellään BLE-yhteyteen sopivaan muotoon ja lähetetään Raspberry Pi:lle.

### Kiihtyvyysanturi
GY-61 ADXL335 on kolmiakselinen kiihtyvyysanturi, jota käytetään laitteen asennon mittaamiseen. Anturi mittaa kiihtyvyyttä X-, Y- ja Z-akselien suunnissa, ja tämä tieto luetaan Nordic-mikrokontrollerin analogia–digitaalimuuntimen (ADC) avulla.

### Raspberry Pi
Raspberry Pi 3 Model B toimii yhdyskäytävänä laitteen ja palvelimen välillä. Se vastaanottaa kiihtyvyysdatan BLE-yhteyden kautta, käsittelee datan sekä välittää sen TCP-yhteyden avulla Linux-palvelimella olevaan MySQL-tietokantaan.

### Linux-palvelin
Palvelin vastaanottaa Raspberry Pi:n lähettämän datan ja tallentaa sen MySQL-tietokantaan. Tietokantaa käytetään sekä tietojen säilyttämiseen että koneoppimismallin koulutus- ja testidatan lähteenä. Tallennettua dataa voi myös tarkastella palvelimelle perustetun verkkosivun kautta, joka hakee mittausdatan suoraan tietokannasta.

### Kehitystietokone
Kehitystietokonetta käytetään Nordic-mikrokontrollerin ohjelmointiin sekä koneoppimismallin kouluttamiseen. Mallin koulutuksessa MySQL-tietokantaan tallennettu kiihtyvyysdata haetaan kehitystietokoneelle, jossa K-means-algoritmi suoritetaan. Koulutuksen tuloksena saadaan klusterikeskipisteet, jotka vastaavat laitteen eri asentoja.

---

## Tiedonsiirtoteknologiat

### Bluetooth Low Energy (BLE)
BLE valitaan tiedonsiirtotekniikaksi Nordic-mikrokontrollerin ja Raspberry Pi:n välille. Se soveltuu erityisesti anturidatan lähettämiseen sulautetuissa järjestelmissä, joissa energiatehokkuus on tärkeä vaatimus.

### TCP-yhteys
Raspberry Pi:n ja palvelimen välinen tiedonsiirto toteutetaan TCP-protokollalla, jonka yli käsitelty mittausdata kirjoitetaan suoraan MySQL-tietokantaan. TCP takaa luotettavan ja järjestyksessä tapahtuvan datansiirron, mikä on tärkeää mittausdatan eheydelle.

---

## Asennon tunnistus ja K-means-klusterointi

K-means-koulutuksessa MySQL-tietokantaan tallennettua kiihtyvyysdataa hyödynnetään laitteen asennon tunnistamiseen. Data kerätään tunnetuissa asennoissa, minkä jälkeen K-means-algoritmi ryhmittelee mittauspisteet klustereihin niiden keskinäisen läheisyyden perusteella. Jokainen klusteri vastaa tiettyä laitteen asentoa, ja klusterien keskipisteitä käytetään jatkossa uuden mittausdatan perusteella laitteen asennon määrittämiseen.



### Tekijät: 
Aleksi Eskola
<br>
Oskari Kovanen
