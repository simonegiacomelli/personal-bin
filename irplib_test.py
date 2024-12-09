import shlex

from irplib import Line, text_parse, SmartSeparator


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


def test_text_parse():
    assert text_parse('cd $(mktemp -d demo-XXX)') == 'cd $(mktemp -d demo-XXX)'
    assert text_parse('ls\\n') == 'ls\n'


class TestSmartSeparator:

    def test_initial(self):
        target = SmartSeparator()
        target.process('mm')
        assert ('', '') == target.tuple

    def test_add(self):
        target = SmartSeparator()
        target.process('mm')
        target.process('mm')
        assert ('\t', '') == target.tuple

    def test_add2(self):
        target = SmartSeparator()
        target.process('mm')
        target.process('mc')
        assert ('\n', '') == target.tuple
