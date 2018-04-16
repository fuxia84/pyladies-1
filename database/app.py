from datetime import date

import peewee

db = peewee.SqliteDatabase('database.db')


class Author(peewee.Model):
    first_name = peewee.CharField()
    last_name = peewee.CharField()
    age = peewee.IntegerField(default=0)

    class Meta:
        database = db


class Publisher(peewee.Model):
    name = peewee.CharField()

    class Meta:
        database = db


class Book(peewee.Model):
    title = peewee.CharField()
    published_at = peewee.DateField()
    author = peewee.ForeignKeyField(Author, backref='books')
    publisher = peewee.ForeignKeyField(Publisher, backref='books', null=True)

    class Meta:
        database = db

    def __str__(self):
        return self.title


db.drop_tables([Author, Publisher, Book])
db.create_tables([Author, Publisher, Book])


Author.create(first_name='Bob', last_name='Kowalski', age=20)
Author.create(first_name='Sam', last_name='Nowak', age=60)
Author.create(first_name='Clara', last_name='Smith')

authors = Author.select()
for author in authors:
    print(author.id, author.first_name, author.last_name, author.age)

publisher = Publisher.create(name='swiat ksiazki')

Book.create(
    title='W pustyni i w puszczy',
    published_at=date(1980, 4, 20),
    author=authors[1],
    publisher=publisher,
)

Book.create(
    title='Janko Muzykant',
    published_at=date(2025, 1, 1),
    author=authors[1],
)

for book in authors[1].books:
    print(book)
