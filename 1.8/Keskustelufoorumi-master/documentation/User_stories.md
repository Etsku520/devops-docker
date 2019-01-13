Tähän mennessä:
Käyttäjänä voin lisätä viestejä.

Käyttäjänö voin muokata viestejä.

Viestini tallentuvat tietokantaan.

Käyttäjänä ei tarvitse arvata sivujen osoitteita.

Käyttäjänä pystyn päättäämään mihin ketjuun laitan viestin

Käyttäjänä muut kuin ylläpitäjät eivät voi vaikuttaa omiin viesteihini

Admin pystyy lisäämään admineita ja tekemään kategorioita

Ryhmiin voi lisätä kategorioita

Kategorian avulla voi etsiä ryhmiä

Ryhmistä voi poistaa kategorioita

Ryhmän poistuessa myös sen avaimeen liitetyt kategoriat poistuvat

Kategoriat näkyvät kun ryhmä on avattu

Tulevaa:

Saa nähä ehtiikö oikeesti tehä mitään erityisiä kirja ominaisuuksia et saattaa vaan jäädä keskusteluille kirjoista :)

Käyttäjänä pystyn laittamaan kirjan sivulle ja sen osat voidaan löytää yhdessä (paloittain kirjan lisääminen).

Varmaa jotai vielä mut ei tuu mitää mielee, enkä ees tiiä pitikö laittaa muutaku ne jotka on jo tehty.

## Jotai SQL ku niitäki pyydettiin (vaikka en ymmärrä missä maailmassa jokaiseen user storyyn voi lisätä järkevän sql kyselyn)
SQL kyselyt tekee pääosin SQLalchemy, muutta täs on muutama

Kaikki viestit ryhmästä: "SELECT DISTINCT Message.text, Message.account_id, Message.group_id, Message.id, Message.date_created, Message.date_modified FROM Groups, Message WHERE Message.group_id = :id ORDER BY message.date_created"

Ryhmän categoriat: "SELECT DISTINCT Category.id, Category.name FROM Groups, Group_category, Category WHERE Category.id = Group_category.category_id AND Group_category.group_id = :id"

Categoriat jotka eivät ole ryhmässä: "SELECT * FROM Category WHERE category.id NOT IN (SELECT category.id FROM Category, group_category WHERE category.id = Group_category.category_id AND Group_category.group_id = :id"
