from pathlib import Path
import io

import png
import pytest

import hexafonter

TESTS_THERE = {
    'generic': ('font.png', 'sample-output.c', []),
    'keeb': ('examples/keeb-font.png', 'examples/keeb-font.c', []),
    'atascii': (
        'examples/atascii.png', 'examples/atascii.c',
        ['8', '-p', 'examples/custom-preamble.inc'],
    ),
}

@pytest.mark.parametrize('test_name', TESTS_THERE)
def test_there(test_name, capsys):
    source, dest, extra_args = TESTS_THERE[test_name]
    hexafonter.main(['hf', source, *extra_args])
    captured = capsys.readouterr()
    got = captured.out
    expected = Path(dest).read_text()
    assert expected == got


TESTS_BACK = {
    'generic': ('sample-output.c', 'examples/font-generated.png', []),
    'keeb': ('examples/keeb-font.c', 'examples/keeb-font.png', []),
    'atascii': ('examples/atascii.c', 'examples/atascii-generated.png', ['8']),
}
@pytest.mark.parametrize('test_name', TESTS_BACK)
def test_back(test_name, capsysbinary):
    source, dest, extra_args = TESTS_BACK[test_name]
    hexafonter.main(['hf', '-r', source, *extra_args])
    captured = capsysbinary.readouterr()
    with io.BytesIO(captured.out) as f:
        *got_size, got_data, got_info = png.Reader(f).asRGBA8()
        got_data = list(got_data)
    with Path(dest).open('rb') as f:
        *expected_size, expected_data, expected_info = png.Reader(f).asRGBA8()
        expected_data = list(expected_data)
    assert expected_size == got_size
    assert expected_data == got_data
