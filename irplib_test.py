import shlex

from irplib import Line


def test_comment1():
    line = Line('# comment')
    assert line.ignore is True


def test_comment2():
    line = Line(' # comment')
    assert line.ignore is True


def test_empty_line():
    line = Line('')
    assert line.ignore is True


def test_empty_line2():
    line = Line(' ')
    assert line.ignore is True


def test_simple_command():
    line = Line('cmd1')
    assert line.ignore is False
    assert line.command == 'cmd1'


def test_generic_command():
    line = Line('cmd1')
    assert line.ignore is False
    assert line.command == 'cmd1'


def test_kc_single_quote():
    line = Line("""kc 0.9799   ''"'"''""")
    assert line.ignore is False
    assert line.command == 'kc'
    assert line.args == ['0.9799', "'"]


def test_kc_double_quote():
    line = Line("""kc 0.2238   '"'""")
    assert line.ignore is False
    assert line.command == 'kc'
    assert line.args == ['0.2238', '"']


def test_kp_altgr():
    line = Line("""kp 0.1881   '<65312>'""")
    assert line.ignore is False
    assert line.command == 'kp'
    assert line.args == ['0.1881', '<65312>']
