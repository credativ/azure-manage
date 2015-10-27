import pytest

from . import CliBase


def test_CliBase():
    cli = CliBase(['--option', 'key1=value1', '--option', 'key2=value2', 'section'])
    assert cli.config_section == {'key1': 'value1', 'key2': 'value2' }

def test_CliBase_config_get():
    cli = CliBase(['section'])
    cli.config_section = {
        'bool': True,
        'str': 'value',
        'expand-str': 'bla-{str}',
        'expand-list': ['bla-{str}'],
        'expand-dict': {'key': 'bla-{str}'},
    }
    assert cli.config_get('bool') is True
    assert cli.config_get('str') == 'value'
    assert cli.config_get('expand-str') == 'bla-value'
    assert cli.config_get('expand-list') == ['bla-value']
    assert cli.config_get('expand-dict') == {'key': 'bla-value'}

    with pytest.raises(KeyError):
        cli.config_get('nonexistant')

    assert cli.config_get('nonexistant', None) is None
    assert cli.config_get('nonexistant', 'default') == 'default'

def test_CliBase_parser():
    parser = CliBase.parser
    options = parser.parse_args(['section'])
    assert options.section == 'section'

    options = parser.parse_args(['--option', 'key1=value1', '--option', 'key2=value2', 'section'])
    assert options.options['key1'] == 'value1'
    assert options.options['key2'] == 'value2'
