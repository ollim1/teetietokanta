### Käyttöohjeet
- Luo käyttäjätunnus painamalla ylhäältä linkkiä "Luo käyttäjä".
- Teetyyppejä ja ainesosia voidaan lisätä teetyyppisivulla ja ainesosasivulla vastaavasti.
- Teelajikkeita voidaan lisätä teet-sivulta. Teen tietosivulta voidaan siirtyä muokkaamaan teen tietoja, lisäämään teehen ainesosia tai arvostelun antamiseen.
  - Tee luodaan antamalla teelle ensin nimi ja sitten lisäämällä sille sopivat tiedot.
- Arvostelusivulla on lista omista arvosteluista. Sivulta voidaan edetä haluttuun teelajikkeeseen.

### Järjestelmänvalvojan toiminnot
- Järjestelmänvalvoja voi korjata ja poistaa tietokannan tietoja. Toistaiseksi mahdollista on poistaa teelajikkeita ja muokata ja poistaa teetyyppejä ja ainesosia. Nämä toiminnot löytyvät vastaavilta sivuilta.
- Käyttäjätilin korottaminen järjestelmänvalvojaksi tapahtuu toistaiseksi tietokannan kautta:
  - avaa application-alihakemistossa tiedostoon `tea.db` tallennettu tietokanta suoraan komennolla `sqlite3 tea.db` ja
  - aja kysely `update account set role=1 where username=foo`, jossa `foo` on korotettavan käyttäjän käyttäjätunnus.
- Vastaava Herokussa:
  - `heroku pg:psql foo`, jossa foo on käyttäjänimi
  - `update account set role=1 where username=foo`, jossa foo on käyttäjänimi
