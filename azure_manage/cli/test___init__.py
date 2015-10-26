from . import CliBase


def test_CliBase():
    cli = CliBase(['--option', 'key1=value1', '--option', 'key2=value2', 'section', 'version'])
    assert cli.config_section == {'key1': 'value1', 'key2': 'value2' }

def test_CliBase_parser():
    parser = CliBase.parser
    options = parser.parse_args(['section', 'version'])
    assert options.section == 'section'

    options = parser.parse_args(['--option', 'key1=value1', '--option', 'key2=value2', 'section', 'version'])
    assert options.options['key1'] == 'value1'
    assert options.options['key2'] == 'value2'
