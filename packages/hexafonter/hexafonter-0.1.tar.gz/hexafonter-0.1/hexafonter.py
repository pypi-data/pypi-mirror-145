"""Generate a C font file for a small LCD from a PNG image
"""
import unicodedata
import contextlib
import itertools
import argparse
import ast
import sys
import re

import png

__version__ = '0.1'

SEXTANT_WIDTH = 3
ROW_HEIGHT = 8
REV_ROW_WIDTH = 0x20

def get_sextants():
    sextants = {
        0b000000: ' ',
        0b101010: '\N{LEFT HALF BLOCK}',
        0b010101: '\N{RIGHT HALF BLOCK}',
        0b111111: '\N{FULL BLOCK}',
    }
    sx_names = '214365'
    for p in range(1, 0b111111):
        if p not in sextants:
            nums = ''.join(
                sorted(sx_names[i] if 1<<i & p else '' for i in range(6)))
            sextants[p] = unicodedata.lookup('BLOCK SEXTANT-'+nums)
    return ''.join(sextants[i] for i in range(2**6))

# Hardcode the result of get_sextants(), because the function
# needs Python 3.9+ (first one that includes data for Unicode 13)
SEXTANTS = ' 🬁🬀🬂🬇🬉🬈🬊🬃🬅🬄🬆🬋🬍🬌🬎🬞🬠🬟🬡🬦▐🬧🬨🬢🬤🬣🬥🬩🬫🬪🬬🬏🬑🬐🬒🬖🬘🬗🬙🬓🬔▌🬕🬚🬜🬛🬝🬭🬯🬮🬰🬵🬷🬶🬸🬱🬳🬲🬴🬹🬻🬺█'

escapes = {i: f' \\{c}' for i, c in enumerate('abtnvfr', start=7)}

DEFAULT_PREAMBLE = """\
#include "progmem.h"
const unsigned char font[] PROGMEM =\
"""


def gen_font(img_data, preamble=DEFAULT_PREAMBLE, width=6):
    yield preamble
    yield ' {\n'

    ch = 0
    def end_col():
        yield '// ['
        for px_row in reversed(range(4)):
            bits = sum(
                (0b11 & (val >> (px_row*2))) << (px_col*2)
                for px_col, val in enumerate(vals)
            )
            yield SEXTANTS[bits]
        vals.clear()
        yield ']'
        yield ''.join(char_starts)
        yield '\n'
        char_starts.clear()
    for line in range(len(img_data) // ROW_HEIGHT):
        yield f'////////////////////////////////////\n'
        line_nums = range(line * ROW_HEIGHT, (line+1) * ROW_HEIGHT)
        vals = []
        char_starts = []
        lines = (img_data[line_num][::4] for line_num in line_nums)
        for col, pixels in enumerate(zip(*lines)):
            if col % SEXTANT_WIDTH == 0:
                yield '  '
            if col % width == 0:
                if ord(' ') <= ch <= ord('~'):
                    printable = f' {chr(ch)}'
                else:
                    printable = escapes.get(ch, '')
                char_starts.append(f' \\x{ch:02x}{printable}')
                ch += 1
            value = sum((px < 128) << i for i, px in enumerate(pixels))
            yield f'0x{value:02X}, '
            vals.append(value)
            if col % SEXTANT_WIDTH == SEXTANT_WIDTH - 1:
                yield from end_col()
        if col % SEXTANT_WIDTH != SEXTANT_WIDTH - 1:
            while col % SEXTANT_WIDTH != SEXTANT_WIDTH - 1:
                yield '      '
                col += 1
            yield from end_col()

    yield '};\n'


def ungen_font(data, outfile, width=6):
    data = re.sub(r'//.*', '', data)
    struct_data = re.search(r'\{[^}]+\}', data, re.MULTILINE)
    if not struct_data:
        raise ValueError('Data not found in input file.')
    struct_data = struct_data[0].replace(*'{[') .replace(*'}]')
    remaining_values = ast.literal_eval(struct_data)
    data_rows = []
    while remaining_values:
        data_rows.append(remaining_values[:width * REV_ROW_WIDTH])
        remaining_values = remaining_values[width * REV_ROW_WIDTH:]

    while len(data_rows[-1]) < len(data_rows[0]):
        data_rows[-1].append(0)

    palette=[(255,255,255), (0, 0, 0), (0xc8, 255, 255)]
    writer = png.Writer(
        width=len(data_rows[0]),
        height=len(data_rows) * 8,
        palette=palette, bitdepth=2,
    )
    pixel_rows = []
    for data_row in data_rows:
        for row_px_idx in range(8):
            mask = 1 << row_px_idx
            pixel_row = []
            pixel_rows.append(pixel_row)
            for col_idx, col in enumerate(data_row):
                if col & mask:
                    pixel_row.append(1)
                elif row_px_idx == ROW_HEIGHT-1 or (col_idx+1) % width == 0:
                    pixel_row.append(2)
                else:
                    pixel_row.append(0)
    writer.write(outfile, pixel_rows);


def main(argv=None):
    if argv is None:
        argv = ays.argv
    parser = argparse.ArgumentParser(argv[0], description=__doc__)
    parser.add_argument(
        'file',
        help='Input file. Use - for standard input.')
    parser.add_argument(
        'width', type=int, nargs='?', default=6,
        help='Width of each character (default: 6)')
    parser.add_argument(
        '-p', '--preamble',
        help='File with a custom preamble text. Use - to disable preamble.')
    parser.add_argument(
        '-o', '--outfile', default='-',
        help='Output file. Use - (default) for standard output.')
    parser.add_argument(
        '-r', '--reverse', action='store_true',
        help='Reverse operation: convert a C file to a PNG file instead.'
        + ' Might not work with C files generated by other tools.')

    args = parser.parse_args(argv[1:])

    if not args.reverse:
        # Read the input file
        with contextlib.ExitStack() as stack:
            if args.file == '-':
                infile = sys.stdin.buffer
            else:
                infile = stack.enter_context(open(args.file, 'rb'))
            reader = png.Reader(infile)
            w, h, img_data, info = reader.asRGBA8()
            img_data = list(img_data)

        # Read the preamble
        if args.preamble == None:
            preamble = DEFAULT_PREAMBLE
        elif args.preamble == '-':
            preamble = ''
        else:
            with open(args.preamble, encoding='utf-8') as f:
                preamble = f.read()
                if preamble.endswith('\n'):
                    preamble = preamble[:-1]

        # Generate and output
        with contextlib.ExitStack() as stack:
            if args.outfile == '-':
                outfile = sys.stdout
            else:
                outfile = stack.enter_context(open(args.outfile, 'w'))

            for chunk in gen_font(
                img_data, preamble=preamble, width=args.width,
            ):
                outfile.write(chunk)

    else:
        # Read the input file
        with contextlib.ExitStack() as stack:
            if args.file == '-':
                infile = sys.stdin
            else:
                infile = stack.enter_context(open(args.file, 'r'))
            data = infile.read()

        # Generate and output
        with contextlib.ExitStack() as stack:
            if args.outfile == '-':
                outfile = sys.stdout.buffer
            else:
                outfile = stack.enter_context(open(args.outfile, 'wb'))

            ungen_font(data, outfile, args.width)


if __name__ == '__main__':
    main(sys.argv)
