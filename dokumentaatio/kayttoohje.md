### Käyttöohjeet
- Luo käyttäjätunnus painamalla ylhäältä linkkiä "Luo käyttäjä".
- Voit lisätä teetyyppejä ja ainesosia teetyyppisivulla ja ainesosasivulla vastaavasti.
- Teelajikkeita voidaan lisätä teet-sivulta. Teen tietosivulla voidaan muokata teen tietoja ja edetä arvostelun antamiseen.
  - Tee luodaan antamalla teelle ensin nimi ja sitten lisäämällä sille sopivat tiedot.
- (Tulossa:) Arvostelusivulla voidaan listata omat arviot teelajikkeista lisäysjärjestyksessä. Arvostelut näkyvät myös listana otsikoita yksittäisten teelajikkeiden sivuilla.

### Järjestelmänvalvojan toiminnot
- Järjestelmänvalvoja voi korjata ja poistaa tietokannan tietoja vapaasti.
- Käyttäjätilin korottaminen järjestelmänvalvojaksi tapahtuu toistaiseksi tietokannan kautta:
  - avaa application-alihakemistossa tiedostoon `tea.db` tallennettu tietokanta suoraan komennolla `sqlite3 tea.db` ja
  - aja kysely `update account set role=1 where name=foo`, missä `foo` on korottettavan käyttäjän nimi.
