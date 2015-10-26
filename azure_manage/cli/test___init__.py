from . import CliBase


def test_CliBase():
    cli = CliBase(['--option', 'key1=value1', '--option', 'key2=value2', 'section'])
    assert cli.config_section == {'key1': 'value1', 'key2': 'value2' }

def test_CliBase_config_get_expand():
    cli = CliBase(['--option', 'key=value', '--option', 'expand=bla-{key}', 'section'])
    assert cli.config_get_expand('key') == 'value'
    assert cli.config_get_expand('expand') == 'bla-value'

def test_CliBase_parser():
    parser = CliBase.parser
    options = parser.parse_args(['section'])
    assert options.section == 'section'

    options = parser.parse_args(['--option', 'key1=value1', '--option', 'key2=value2', 'section'])
    assert options.options['key1'] == 'value1'
    assert options.options['key2'] == 'value2'
