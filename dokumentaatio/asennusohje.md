### Asennusohjeet
Pura sovellus haluamaasi hakemistoon. Aja sovelluksen hakemistossa komennot `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`.

Sovelluksen voi jatkossa ajaa komennoilla `source venv/bin/activate && python3 run.py`.

#### Heroku
Sovelluksesta voidaan saada oma kopio Herokuun kopioimalla repositorio ja luomalla uusi Heroku-sovellus Postgres-tietokantaliitännäisellä. Ylimääräistä konfigurointia ei pitäisi tarvita.

Käyttäjä voidaan korottaa järjestelmänvalvojaksi ottamalla yhteys tietokantaan komennolla `heroku pg:psql -a <sovelluksen nimi>` ja ajamalla kysely `update account set role=1 where username=foo`, jossa foo on käyttäjätunnus.
