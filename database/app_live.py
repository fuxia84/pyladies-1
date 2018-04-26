from datetime import date

import peewee

# Utworzenie połączenia z bazą danych
db = peewee.SqliteDatabase('database.db')


# Definicja modeli (tabel w bazie)
class Author(peewee.Model):
    first_name = peewee.CharField()
    last_name = peewee.CharField()
    age = peewee.IntegerField(null=True)

    class Meta:
        database = db

    def __str__(self):
        return '{} {} ({})'.format(
            self.first_name,
            self.last_name,
            self.age,
        )


class Book(peewee.Model):
    title = peewee.CharField()
    published_at = peewee.DateField()
    author = peewee.ForeignKeyField(Author, backref='books')

    class Meta:
        database = db

    def __str__(self):
        return self.title


# Usunięcie i stworzenie na nowo naszych tabel
db.drop_tables([Author, Book])
db.create_tables([Author, Book])

# Utworzenie 3 autorów i zapisanie ich w bazie
Author.create(first_name='Jan', last_name='Kowalski', age=20)
Author.create(first_name='Ryszard', last_name='Kalisz', age=30)
Author.create(first_name='Simba', last_name='Petru')

# Wybranie autorów z bazy
authors = Author.select()

# Utworzenie 3 książek
Book.create(
    title='W pustyni i w puszczy',
    published_at=date(2016, 1, 1),
    author=authors[1],
)
Book.create(
    title='Janko Muzykant',
    published_at=date(2050, 12, 15),
    author=authors[1],
)
Book.create(
    title='Nasza Szkapa',
    published_at=date(2040, 12, 15),
    author=authors[2],
)

for author in authors:
    print(author)

    # Pobierz powiązane książki poprzez backref (linia 27)
    for book in author.books:
        print("--->", book)

    # Identyczne zapytanie wyciągające książki danego autora
    for book in Book.select().where(Book.author == author):
        print("--->", book)


print('Authors count: {}'.format(
    Author.select().count(),
))

# Usuwanie obiektu z bazy (oba podejścia są poprawne)
# Usuwanie obiektu który już mamy wyciągnięty do pamięci programu
# authors[0].delete_instance()

# Usuwanie obiektu jeśli znamy jego identyfikator w bazie
Author.delete_by_id(1)

print('Authors count: {}'.format(
    Author.select().count(),
))


# Aktualizacja obiektu w bazie
author = Author.select().where(Author.id == 3)[0]
print(author)
author.first_name = 'Bob'
author.last_name = 'Marley'
# Nie zapomnij zapisać obiektu w bazie. Bez wywołania tej metody obiekt nie
# zostanie zaktualizowany na poziomie bazy
author.save()

author = Author.select().where(Author.id == 3)[0]
print(author)
