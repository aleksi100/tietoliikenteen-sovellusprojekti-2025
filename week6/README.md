# 🧩 TL_Project_Week6

## 🎯 Viikon perustavoite
Tämän viikon päätavoitteena on toteuttaa **K-means-luokittelija-algoritmi NRF5340DK-alustalle**.  
Lisätehtävänä voit toteuttaa **konvoluutioneuroverkon (CNN)** mikrokontrollerissa C-kielellä.

---

## ⚙️ 0. Ohjeet Scrum-tiimille (= 6 työparia)

### Viikon vastuullisen työparin tehtävät
- Järjestää **daily-palaverit keskiviikkoisin ja torstaisin**  
- Raportoi Scrum-tiimin **Discord-kanavalle**:
  - Ketkä olivat paikalla  
  - Missä vaiheessa kukin työpari on menossa  
  - Mahdolliset ongelmat  
- Järjestää **sprint review -palaverin perjantaina**  
- Laatii **Discordiin raportin viikon tuloksista** (mukaan lukien seuraavan viikon vastuullinen työpari)

### Kanban-suunnitelma
Laadi GitHubin **projektin Kanban-tauluun** suunnitelma, miten aiotte toteuttaa ja testata viikon tehtävät.  
Pilkkoa tarvittaessa tehtävät pienempiin osiin, kuten:
- 1️⃣ Etäisyyden laskenta-aliohjelma (3D-pisteiden välinen etäisyys)
- 2️⃣ Confusion matrixin laskenta ja visualisointi

---

## 🧠 1. K-means-luokittelijan toteutus NRF5340DK-alustalla

### Tavoite
Toteuta K-means-luokittelija-algoritmi, joka mittaa kiihtyvyysanturilla **x, y, z -arvot** ja laskee tämän 3D-pisteen etäisyyden kaikkiin kuuteen keskipisteeseen, jotka opetettiin Pythonilla edellisellä viikolla.  
Keskipisteet tuodaan ohjelmaan `keskipisteet.h`-tiedostona.

### Vaiheet
1. Kloonaa GitHub-repositorio:  
   🔗 [https://github.com/kajyrkka/TL_Project_Week6](https://github.com/kajyrkka/TL_Project_Week6)
2. Käännä repositoryn mukana tullut NRF5340DK-ohjelma ja tutustu koodin rakenteeseen.  
3. Täydennä `confusion.c`-tiedoston puuttuvat aliohjelmat.  
4. Suorita mittaukset omalla NRF5340DK-laitteellasi ja kiihtyvyysanturilla (sama anturi kuin viikoilla 2 ja 3).  
   Tee **noin 100 mittausta jokaiseen 6 suuntaan**.  

### Lopputulos
- Laske ja piirrä **confusion matrix**, joka kuvaa K-means-luokittelijan tarkkuutta.  
- Lisää confusion matrix -kuva omaan GitHub-repositoriosi `README.md`-tiedostoon.

📺 Jos et pääse alkuun, katso ohjevideolta selitys koodin toiminnasta ja tehtävästä:  
🔗 [https://youtu.be/O2OIN-gJeo4](https://youtu.be/O2OIN-gJeo4)

---

## 🚀 Viikon 6 – Ylimääräiset tehtävät (valinnaiset)

### 🧩 1️⃣ CNN:n toteutus NRF5340DK-mikrokontrollerissa

Tässä lisätehtävässä toteutetaan aiemmin opetettu konvoluutioneuroverkko (CNN) **C-kielellä** Nordic Semiconductorin NRF5340DK-alustalle.

---

### 🔍 Vaihe 1 – Muistin ja suoritusajan analyysi
Laadi **Excel-dokumentti**, jossa arvioit opettamasi CNN-mallin:
- Muistin tarpeen (parametrit, aktivointien määrä)
- Suoritusajan (arvio mikrokontrollerilla)

---

### 🧠 Vaihe 2 – CNN:n toteutus Pythonilla (testidatan generointi)
Toteuta opettamasi CNN Pythonilla kerros kerrokselta (samaa tyyliä kuin "Koneoppimisen perusteet" -projektissa).  
Python-ohjelma voi generoida seuraavat tiedostot:

- **`input.h`** → sisältää testattavan kerroksen syötteen ja mallin parametrit  
- **`output.h`** → sisältää testattavan kerroksen oikean tuloksen  

Näitä tiedostoja käytetään C-kielisessä toteutuksessa tulosten vertailuun.  


---

### ⚙️ Vaihe 3 – CNN:n toteutus C-kielellä
Toteuta CNN-mallisi **C-kielellä**, kerros kerrokselta, alkaen luokittelukerroksista.  

Tee jokaisesta kerroksesta aliohjelma, jolle:
- Syötetään `input.h`-tiedoston data  
- Verrataan tulosta `output.h`-tiedoston oikeaan arvoon  

Tämä varmistaa, että C-toteutuksen laskenta vastaa Python-mallin tuloksia.

---

## 📋 Yhteenveto

| Osa | Tavoite | Tuotos |
|------|----------|---------|
| **1. K-means-luokittelija** | Toteuta ja testaa NRF5340DK-alustalla | Confusion matrix |
| **2. (Valinnainen)** CNN | Arvioi ja toteuta CNN C-kielellä mikrokontrollerissa | CNN C-toteutus + vertailutiedostot |

---

**💡 Muista:**  
Dokumentoi eteneminen Scrum-raporteissa, päivitä Kanban-taulu ja lisää tulokset omaan GitHub-repositorioon.

**Tsemppiä viikon 6 projektiin! 🚀**
