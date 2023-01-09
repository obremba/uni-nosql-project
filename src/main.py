from magic_store.database import Database
from magic_store.models.user import User

if __name__ == '__main__':
    db = Database()

    # db.add_user(User('Sergiusz Morga', 'smorga', 'sergiusz.morga@gmail.com'))
    print(db.delete_user('smorga'))
