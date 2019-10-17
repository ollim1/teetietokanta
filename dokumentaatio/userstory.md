# User storyt
- Rekisteröimätön käyttäjä voi luoda uuden käyttäjätilin.

```
insert into account (id, date_created, date_modified, name, username, password_hash
  values (?, ?, ?, ?, ?, ?) 
```

- Rekisteröimätön käyttäjä voi kirjautua sisään.

```
select id, password_hash from account
  where name = ?
```

- Käyttäjä voi lisätä tietokantaan ainesosia.

```
insert into ingredient (name)
  values (?)
```

- Järjestelmänvalvoja voi poistaa ainesosia.

```
delete from tea_ingredient
  where ingredient = ?
delete from ingredient
  where id = ?
```

- Järjestelmänvalvoja voi muuttaa ainesosan nimeä.

```
update ingredient set name = ?
  where id = ?
```

- Käyttäjä voi lisätä tietokantaan teetyyppejä.

```
insert into tea_type (name)
  values (?)
```

- Järjestelmänvalvoja voi poistaa teetyyppejä.

```
update tea set type = NULL
  where type = ?
delete from tea_type
  where id = ?
```

- Järjestelmänvalvoja voi muuttaa teetyypin nimeä.

```
update tea_type set name = ?
  where id = ?
```

- Käyttäjä voi lisätä uuden teen tietokantaan.
  - Käyttäjä valitsee teetyypin valikosta ja määrittää haudutustiedot.

```
insert into tea (temperature, brewtime, boiled, name, type)
  values (?, ?, ?, ?, ?)`
```

- Käyttäjä voi lisätä teehen ainesosia.

```
insert into tea_ingredient (tea, ingredient)
  values (?, ?)
```

- Käyttäjä voi muokata teelajikkeen tietoja.

```
update tea set
  name = ?,
  temperature = ?,
  brewtime = ?,
  boiled = ?,
  type = ?
  where tea.id = ?
```

- Käyttäjä voi kirjoittaa arvostelun teestä.

```
insert into review (temperature, brewtime, boiled, user, tea, score, content)
  values (?, ?, ?, ?, ?, ?)
```

- Käyttäjä voi nähdä kirjoittamansa arvostelut omalla sivullaan.

```
select tea.name, review.title, review.score from review
  join tea on tea.id = review.tea
  where review.user = ?
  order by score desc
```

- Käyttäjä voi nähdä teelajikkeeseen liittyvät arvostelut teelajikkeen sivulla.

```
select tea.name, review.title, review.score from review
  join tea on tea.id = review.tea
  where review.tea = ?
  order by score desc
```

- Käyttäjä voi lukea arvosteluja.

```
select tea.id, tea.name from tea
  where tea.id = ?
select * from review
  where review.id = ?
```

- Käyttäjä voi muokata omia arvostelujaan.

```
update review set
  date_modified = ?,
  title = ?,
  score = ?,
  content = ?,
  temperature = ?,
  brewtime = ?,
  boiled = ?
  where id = ?
```
