from . import CliBase


def test_CliBase():
    cli = CliBase(['--option', 'key1=value1', '--option', 'key2=value2', 'section'])
    assert cli.config_section == {'key1': 'value1', 'key2': 'value2' }

def test_CliBase_config_get_expand():
    cli = CliBase(['section'])
    cli.config_section = {
        'bool': True,
        'str': 'value',
        'expand-str': 'bla-{str}',
        'expand-list': ['bla-{str}'],
        'expand-dict': {'key': 'bla-{str}'},
    }
    assert cli.config_get_expand('bool') is True
    assert cli.config_get_expand('str') == 'value'
    assert cli.config_get_expand('expand-str') == 'bla-value'
    assert cli.config_get_expand('expand-list') == ['bla-value']
    assert cli.config_get_expand('expand-dict') == {'key': 'bla-value'}

def test_CliBase_parser():
    parser = CliBase.parser
    options = parser.parse_args(['section'])
    assert options.section == 'section'

    options = parser.parse_args(['--option', 'key1=value1', '--option', 'key2=value2', 'section'])
    assert options.options['key1'] == 'value1'
    assert options.options['key2'] == 'value2'
