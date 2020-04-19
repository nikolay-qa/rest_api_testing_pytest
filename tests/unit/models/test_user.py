from models.user import UserModel


def test_create_user():
    user = UserModel('test_username', 'qwerty')
    assert user.username == 'test_username' and user.password == 'qwerty'\
        , "Username or password is not corresponding to the passed data."
