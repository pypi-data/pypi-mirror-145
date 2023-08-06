from pybrary.fernet import Fernet


def test_fernet():
    origin = 'Hello world'
    passwd = 'azerty'
    fernet = Fernet(passwd)
    secret = fernet.encrypt(origin)
    result = fernet.decrypt(secret)
    assert result == origin
