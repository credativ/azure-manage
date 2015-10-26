from . import CliBase


def test_CliBase():
    cli = CliBase(['--option', 'key1=value1', '--option', 'key2=value2', 'section', 'version'])
    assert cli.config_section == {'key1': 'value1', 'key2': 'value2', 'version': 'version' }

def test_CliBase_config_get_expand():
    cli = CliBase(['--option', 'key=value', '--option', 'expand=bla-{key}-{version}', 'section', 'version'])
    assert cli.config_get_expand('version') == 'version'
    assert cli.config_get_expand('key') == 'value'
    assert cli.config_get_expand('expand') == 'bla-value-version'

def test_CliBase_parser():
    parser = CliBase.parser
    options = parser.parse_args(['section', 'version'])
    assert options.section == 'section'

    options = parser.parse_args(['--option', 'key1=value1', '--option', 'key2=value2', 'section', 'version'])
    assert options.options['key1'] == 'value1'
    assert options.options['key2'] == 'value2'
