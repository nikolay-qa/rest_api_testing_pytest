from models.user import UserModel


def test_crud(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app_context():
        user = UserModel('test_user', 'qwerty')
        assert UserModel.find_by_username('test_user') is None
        assert UserModel.find_by_id(1) is None
        user.save_to_db()
        assert UserModel.find_by_username('test_user') is not None
        assert UserModel.find_by_id(1) is not None

