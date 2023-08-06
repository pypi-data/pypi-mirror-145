from pybrary import shell


def test_s_shell():
    ret, out, err = shell('ls -l')
    assert isinstance(ret, int)
    assert ret==0
    assert isinstance(out, str)
    assert out
    assert isinstance(err, str)
    assert not err


def test_n_shell_err_arg():
    ret, out, err = shell('ls -l not_there')
    assert isinstance(ret, int)
    assert ret==2
    assert isinstance(out, str)
    assert not out
    assert isinstance(err, str)
    assert err


def test_n_shell_err_cmd():
    ret, out, err = shell('dum')
    assert isinstance(ret, int)
    assert ret==127
    assert isinstance(out, str)
    assert not out
    assert isinstance(err, str)
    assert err


def test_s_shell_script():
    ret, out, err = shell('''
        pwd
        ls -l
        cd /tmp
        pwd
        ls -l
        cd -
        pwd
        ls -l
    ''')
    assert isinstance(ret, int)
    assert ret==0
    assert isinstance(out, str)
    assert out
    assert isinstance(err, str)
    assert not err


def test_s_shell_script_err():
    ret, out, err = shell('''
        pwd
        ls -l
        cd /dum
        pwd
        dum
        cd -
        pwd
        ls -l
    ''')
    assert isinstance(ret, int)
    assert ret==0
    assert isinstance(out, str)
    assert out
    assert isinstance(err, str)
    assert err


if __name__=='__main__': test_s_shell_script_err()
