# User storyt
## tapaus 1
Käyttäjä on lisäämässä tietokantaan uusia ainesosia. Käyttäjä kirjoittaa ainesosan nimen ja painaa lisäysnappia.

Kysely:

```
insert into ingredient (name) values (?)
```

## tapaus 2
Käyttäjä voi lisää tietokantaan uuden teetyypin. Teetyyppi kirjoitetaan lomakkeeseen ja tiedot tallennetaan tallennusnapilla.

Kysely: ```
insert into tea_type (name)
 values (?)`
 ```

## tapaus 3
Käyttäjä on lisäämässä uutta teetä tietokantaan. Käyttäjä valitsee ainesosat kuten teelehdet ja mausteet valikosta ja määrittää teen nimen ja haudutustiedot. Käyttäjä syöttää teen nimen ja haudutustiedot lomakkeeseen ja valitsee teen tyypin. Tämän jälkeen käyttäjä lisää teen tietoihin ainesosia yksi kerrallaan listan sisältävästä lomakkeesta. 
Käyttäjä (mahdollisesti vain järjestelmän ylläpitäjä) voi muokata teen tietoja klikkaamalla teetä listassa ja tämän jälkeen näkyvällä tarkempia tietoja tarjoavalla sivulla muokkausnappia. Muokkauslomake toimii samalla tavalla kuin lisäyslomake.

Kyselyt:

```
insert into tea (temperature, brewtime, boiled, name, type)
  values (?, ?, ?, ?, ?)`
insert into tea_ingredient (tea, ingredient)
  values (?, ?)
```
## tapaus 4
Käyttäjä haluaa kirjoittaa arvostelun teestä tai haudukkeesta. Käyttäjä kirjautuu sisään käyttäjätunnuksellaan, kirjoittaa arvostelutekstin ja antaa arvosanan. Käytetyn haudutuksen yksityiskohdat ovat toivottuja tilastoja muiden käyttöä varten.

Kyselyt:
```
insert into review (temperature, brewtime, boiled, user, tea, score, content)
  values (?, ?, ?, ?, ?, ?)
```
