from magic_store.database import Database
from magic_store.models.user import User
from magic_store.models.file import File

if __name__ == '__main__':
    db = Database()
    db.drop_database()  # dla powtarzalności testów

    print(db.add_user(User('Sergiusz Morga', 'smorga', 'sergiusz.morga@gmail.com')))
    print(db.add_file('smorga', File('file1.txt', '/src/file1.txt'), tags=['tag1', 'tag2']))
    print(db.get_file('smorga', 'file1.txt', tag='tag1'))
    print(db.get_tag('smorga', 'tag1'))
    print(db.delete_file('smorga', 'file1.txt'))
    print(db.delete_tag('smorga', 'tag1'))
