from main import print_hi


def test_print_hi(capfd):
    print_hi("python")
    out, err = capfd.readouterr()
    assert out == 'Hi, python\n'
