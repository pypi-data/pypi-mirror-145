#!/usr/bin/python3

#----- imports -----

from .__init__ import __version__ as version, __doc__ as description
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from warnings import simplefilter
from shutil import copy2
from sys import argv, stdout, stderr
from time import localtime, sleep
from os.path import join as joinpath, split as splitpath, isfile
from .__init__ import longpath, shortpath, splitpath4, listfiles, getfile, lastfile, localfile
from .__init__ import listdirs, getdir, chdir2, newbackfile, oldbackfile
from .__init__ import hold, chars, upperin, lowerin, letterin, digitin, specialin, split, replace, change
from .__init__ import shrink, expand, findchar, rfindchar, chrs, ords, edit, plural, linterpol
from .__init__ import inform, warning, error
from .__init__ import in2in, in2pt, pt2in, in2cm, cm2in, in2mm, mm2in, in2str, str2in, str2inxin, ratio
from .__init__ import retroenum, find, rfind, shell, get, term, tryfunc, dump, Setdict

#----- global data -----

class Container: pass
arg = Container() # container for arguments and other global data

#----- constants -----

EMPT, CODE, TEXT, PICT, CONT, INDX, CHP1, CHP2, HEA1, HEA2 = range(10) # values for kind
KINDS = 'EMPT CODE TEXT PICT CONT INDX CHP1 CHP2 HEA1 HEA2'.split() # labels for kind
JLIN, KIND, JPAG, LPIC, LINE = range(5) # positions in buf.input[j] and buf.output[j]
PREF, TITL, jout = range(3) # positions in buf.contents[j]
FORMFEED = '\f' # page header, first character of first line
MACRON = '¯' # page header, second line, dashed
QUOTES = "'" + '"' # single and double quotation marks
INDENT = 4 * ' ' # tab indentation
PAPERSIZE = { # names for -S
    'HALF LETTER':  '5.5x8.5in',
    'LETTER':       '8.5x11.0in',
    'LEGAL':        '8.5x14.0in',
    'JUNIOR LEGAL': '5.0x8.0in',
    'LEDGER':       '11.0x17.0in',
    'TABLOID':      '11.0x17.0in',
    'A0':  '841x1189mm',
    'A1':  '594x841mm',
    'A2':  '420x594mm',
    'A3':  '297x420mm',
    'A4':  '210x297mm',
    'A5':  '148x210mm',
    'A6':  '105x148mm',
    'A7':  '74x105mm',
    'A8':  '52x74mm',
    'A9':  '37x52mm',
    'A10': '26x37mm',
    'B0':  '1000x1414mm',
    'B1':  '707x1000mm',
    'B1+': '720x1020mm',
    'B2':  '500x707mm',
    'B2+': '520x720mm',
    'B3':  '353x500mm',
    'B4':  '250x353mm',
    'B5':  '176x250mm',
    'B6':  '125x176mm',
    'B7':  '88x125mm',
    'B8':  '62x88mm',
    'B9':  '44x62mm',
    'B10': '31x44mm'}
# page margin correctors in mm = (portrait_xyxy, landscape_xyxy)
LXYXY = ([(16, 10), (24, 20), (35, 30), (43, 40), (52, 50), (62, 60), (72.5, 70), (83, 80), (92, 90), (101, 100)],
         [(20.5, 10), (29.5, 20), (39, 30), (48, 40), (57, 50), (66.5, 60), (75.5, 70), (84.5, 80), (94, 90), (104, 100)])
RXYXY = ([(15, 10), (25.5, 20), (34.5, 30), (44.5, 40), (54.5, 50), (64.5, 60), (72, 70), (81, 80), (91.5, 90), (100, 100)],
         [(0, 5),  (17, 5),   (22, 10), (30, 20), (40, 30), (49.5, 40), (58, 50), (68, 60), (77.5, 70), (86, 80), (96, 90), (104, 100)])
TXYXY = ([(11.5, 10), (21, 20), (30.5, 30), (39.5, 40), (49, 50), (59, 60), (68, 70), (77.5, 80), (87, 90), (96, 100)],
         [(11, 10), (20.5, 20), (30, 30), (39, 40), (48.5, 50), (57.5, 60), (67, 70), (76, 80), (85, 90), (95, 100)])
BXYXY = ([(24, 10), (34, 20), (43, 30), (52.5, 40), (62, 50), (71, 60), (81, 70), (90, 80), (100, 90), (109.5, 100)],
         [(24, 10), (32, 20), (42, 30), (52, 40), (60, 50), (70.5, 60), (80, 70), (88, 80), (99, 90), (107, 100)])
# char size correctors = (portrait_factor, landscape_factor)
CWF = (100/95, 100/92) # char width factor
CHF = (100/94, 100/93) # char height factor

#----- classes -----

class Paragraph:

    def __init__(par):
        par.string = ''
        par.indent = 0
        
    def append(par, string, indent=0):
        if par.string:
            par.string += ' ' + shrink(string)
        else:
            par.string = shrink(string)
            par.indent = indent

    def flush(par, jlin):
        if not par.string:
            return
        prefix = (par.indent - 2) * ' ' + '• ' if par.indent else ''
        while len(par.string) > arg.chars_per_line - par.indent:
            jchar = rfind(par.string[:arg.chars_per_line-par.indent+1], ' ')
            if jchar <= 0:
                error('Impossible to left-justify', jlin, string)
            string, par.string = par.string[:jchar], par.string[jchar+1:]
            if not arg.left_only:
                try:
                    string = expand(string, arg.chars_per_line - par.indent)
                except ValueError as error_message:
                    error('Impossible to right-justify', jlin, string)
            buf.append(jlin, TEXT, 0, 0, prefix + string)
            prefix = par.indent * ' '
        if  par.string:
            buf.append(jlin, TEXT, 0, 0, prefix + par.string)
            par.string = ''

par = Paragraph()

class Buffer:

    def __init__(buf):
        buf.input = [] # [[jlin, 0, 0, 0, line]] # input buffer
        buf.output = [] # [[jlin, kind, jpag, lpic, line]] # output buffer
        # jlin: line index in buf.input, for error message
        # kind: kind of line: CODE, TEXT, PICT, CONT, INDX, CHP1, CHP2, HEA1, HEA2
        # jpag: page number
        # lpic: lines in picture (in first line of pictures only, else 0)
        # line
        buf.contents = [] # [[pref, titl, jout]]
        # pref: chapter numbering, first word in chapter line as '1.', '1.1.'...
        # titl: rest of chapter line
        # jout: position of chapter line in buf.output
        buf.contents_start, buf.contents_stop = -1, -1 # start and stop of contents in output
        buf.index = [] # [(subject, {jout})][::-1]
        # subject: subject between double quotes in TEXT lines
        # jout: position of subject in buf.output
        buf.index_start, buf.index_stop = -1, -1 # start and stop of index in output

    def __len__(buf):
        return len(buf.output)

    def append(buf, jlin, kind, jpag, lpic, line):
        buf.output.append([jlin, kind, jpag, lpic, line])

    def char(buf, jout, jchar):
        'return buf.output[jout][LINE][jchar], used by redraw_segments() and redraw_arroheads()'
        if jout < 0 or jchar < 0:
            return ' '
        try:
            line = buf.output[jout][LINE]
            return line[jchar] if buf.output[jout][KIND] == PICT else ' '
        except IndexError:
            return ' '

    def dump(buf):
        'for debug only'
        print(f'\n' + '.' * 72)
        print(f'... contents_start = {buf.contents_start}, contents_stop = {buf.contents_stop} ...')
        print(f'... index_start = {buf.index_start}, index_stop = {buf.index_stop} ...')
        for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
            print(jout, ':', (jlin, KINDS[kind], jpag, lpic, line))
        print('\n... contents ...')
        for jout, rec in enumerate(buf.contents):
            print(jout, ':', rec)
        print('\n... index ...')
        for jout, rec in enumerate(buf.index):
            print(jout, ':', rec)
        print('.' * 72)

buf = Buffer()

#----- functions -----

def get_level_title(line):
    'return (level, title) if line is a numbered chapter line else (0, line)'
    status = 0; level = 0
    for jchar, char in enumerate(line):
        if status == 0:
            if '0' <= char <= '9': status = 1
            else: return 0, line
        elif status == 1:
            if '0' <= char <= '9': status = 1
            elif char == '.': level += 1; status = 2
            else: return 0, line
        else: # status == 2
            if '0' <= char <= '9': status = 1
            elif char == ' ': return level, shrink(line[jchar+1:]).upper()
            else: return 0, line
    return (level, '') if status == 2 else (0, line)

def check_gt0(number, argname):
    if number <= 0:
        error(f"Wrong {argname} {number}")

def get_margin_margin2(letter, margin):    
    x = tryfunc(str2in, (margin,), -1.0)
    if x < 0.0:
        error(f'Wrong -{letter} {margin}')
    if x < str2in('2cm'):
        warning(f'-{letter} {margin} < 2cm, you may get unexpected results')
    margin = x
    if arg.calibration:
        return margin, margin
    else:
        xyxy = {'L': LXYXY, 'R': RXYXY, 'T': TXYXY, 'B': BXYXY}[letter][arg.landscape]
        a, b, err = linterpol(xyxy)
        margin2 = max(0.0, mm2in(a * in2mm(margin) + b))
        if arg.verbose: inform(f'Correct: -{letter} {in2str(margin2)}')
        return margin, margin2

#----- actions -----

def get_arguments():
    parser = ArgumentParser(prog='yawp', formatter_class=RawDescriptionHelpFormatter, description=description)
    add = parser.add_argument
    # general arguments
    add('-H','--manual', action='store_true', help='open yawp Manual in PDF format and exit')
    add('-V','--version', action='version', version=f'yawp {version}')
    add('-v','--verbose', action='store_true', help='display information messages on stderr')
    add('-N','--no-format', action='store_true', help="don't format the file")
    add('-U','--undo', action='store_true', help="restore the file from its previous version")
    add('-g','--graphics', action='store_true', help="redraw '`'-segments and '^'-arrowheads")
    add('-p','--print-file', action='store_true', help="at end print file on stdout")
    # formatting arguments
    add('-w','--chars-per-line', default='0', help="line width in characters per line (default: '0' = automatic)")
    add('-l','--left-only', action='store_true', help="justify text lines at left only (default: at left and right)")
    add('-c','--contents-title', default='contents', help="title of contents chapter (default: 'contents')")
    add('-i','--index-title', default='index', help="title of index chapter (default: 'index')")
    add('-m','--max-subject', default='36', help="max length of index subjects (default: '36')")
    # paging arguments
    add('-f','--form-feed', action='store_true', help="insert page headers on full page")
    add('-F','--form-feed-chap', action='store_true', help="insert page headers on full page and before contents index and level-one chapters")
    add('-e','--even-left', default='%n/%N', help="headers of even pages, left (default: '%%n/%%N')")
    add('-E','--even-right', default='%f.%e %Y-%m-%d %H:%M:%S', help="headers of even pages, right (default: '%%f.%%e %%Y-%%m-%%d %%H:%%M:%%S')")
    add('-o','--odd-left', default='%c', help="headers of odd pages, left (default: '%%c')")
    add('-O','--odd-right', default='%n/%N', help="headers of odd pages, right (default: '%%n/%%N')")
    add('-a','--all-pages-E-e', action='store_true', help="all page headers contain -E at left and -e at right")
    # PDF exporting arguments
    add('-P','--file-pdf', default='%P/%f.pdf', help="file name of exported PDF file ('0' = no PDF export, default: '%%P/%%f.pdf')")
    add('-W','--char-width', default='0', help="character width (pt/in/mm/cm, default: '0' = automatic)")
    add('-A','--char-aspect', default='3/5', help="character aspect ratio = char width / char height ('1' = square grid, default: '3/5')")
    add('-S','--paper-size', default='A4', help="portrait paper size (width x height, pt/in/mm/cm, default: 'A4' = '210x297mm'")
    add('-Z','--landscape', action='store_true', help="turn page by 90 degrees (default: portrait)")
    add('-Q','--print-quality', default='2', help="print quality ('0' '1' or '2', default: '2')")
    add('-L','--left-margin', default='2cm', help="left margin (pt/in/mm/cm, default: '2cm')")
    add('-R','--right-margin', default='-L', help="right margin (pt/in/mm/cm, default: '-L')")
    add('-T','--top-margin', default='2cm', help="top margin (pt/in/mm/cm, default: '2cm')")
    add('-B','--bottom-margin', default='-T', help="bottom margin (pt/in/mm/cm, default: '-T')")
    # debugging arguments
    add('-s','--echo-shell', action='store_true', help='debug, display invoked Unix commands')
    add('-k','--calibration', action='store_true', help="debug, don't correct character size and page margins")
    # positional argument
    add('file', nargs='?', help='text file to be processed')
    # arguments --> arg.*
    parser.parse_args(argv[1:], arg)
    
def check_arguments():
    arg.start_time = localtime()[:]
    # -s
    arg.shell_mode = arg.echo_shell * 'co'
    # -H
    if arg.manual:
        yawp_pdf = localfile('docs/yawp.pdf')
        shell(f'xdg-open {yawp_pdf}', arg.shell_mode)
        exit()
    # file
    if not arg.file:
        error("Mandatory positional argument file, not found")
    arg.file = longpath(arg.file)
    arg.PpfeYmdHMS = splitpath4(arg.file) + tuple(('%04d %02d %02d %02d %02d %02d' % arg.start_time[:6]).split())
    # -U -N
    if arg.undo and arg.no_format:
        error("You can't set both -U and -N")
    # -w >= 0
    w = tryfunc(int, (arg.chars_per_line,), -1)
    if w < 0:
        error(f'Wrong -w {arg.chars_per_line}')
    arg.chars_per_line = w
    # -c -i
    if not arg.contents_title:
        error("Wrong -c ''")
    if not arg.index_title:
        error("Wrong -i ''")
    arg.contents_title = shrink(arg.contents_title).upper()
    arg.index_title = shrink(arg.index_title).upper()
    if arg.contents_title == arg.index_title:
        error(f"Wrong -c = -i {arg.contents_title}")
    # -m > 0
    m = tryfunc(int, (arg.max_subject,), -1)
    if m <= 0:
        error(f'Wrong -w {arg.max_subject}')
    arg.max_subject = m
    # -f -F
    if arg.file.endswith('.py'):
        if arg.form_feed:
            inform("Python file, -f turned off")
            arg.form_feed = False
        if arg.form_feed_chap:
            inform("Python file, -F turned off")
            arg.form_feed_chap = False
    arg.form_feed = arg.form_feed or arg.form_feed_chap
    # -e -E -o -O
    for char, argx in zip('eEoO', [arg.even_left, arg.even_right, arg.odd_left, arg.odd_right]):
        try:
            change(argx, 'PpfeYmdHMSnNc', 'PpfeYmdHMSnNc', '%')
        except ValueError as illegal:
            error(f'Wrong -{char} {argx!r}, illegal {str(illegal)!r}')
    # -P
    if tryfunc(float, (arg.file_pdf,), -1) == 0.0:
        arg.file_pdf = ''
    if arg.file_pdf:
        try:
            arg.file_pdf = change(arg.file_pdf, 'PpfeYmdHMS', arg.PpfeYmdHMS, '%')
        except ValueError as illegal:
            error(f'Wrong -P {shortpath(arg.file_pdf)!r}, illegal {str(illegal)!r}')
        arg.file_pdf = longpath(arg.file_pdf)
        if not arg.file_pdf.endswith('.pdf'):
            error(f"Wrong -P {shortpath(arg.file_pdf)!r}, doesn't end with '.pdf'")
    # -Q in {0, 1, 2}
    Q = tryfunc(int, (arg.print_quality,), -1)
    if Q not in {0, 1, 2}:
        error(f'Wrong -Q {arg.print_quality}')
    arg.print_quality = Q
    # -W >= 0
    W = tryfunc(str2in, (arg.char_width,), -1.0)
    if W < 0.0:
        error(f'Wrong -W {arg.char_width}')
    arg.char_width = W
    # -A > 0
    A = tryfunc(ratio, (arg.char_aspect,), -1.0)
    if A <= 0.0:
        error(f'Wrong -A {arg.char_aspect}')
    arg.char_aspect = A
    # -S 0 < Sw <= Sh
    Sw, Sh = tryfunc(str2inxin, (PAPERSIZE.get(arg.paper_size.upper(), arg.paper_size),), (-1.0, -1.0))
    if not 0 < Sw <= Sh:
        error(f'Wrong -S {arg.paper_size}')
    arg.paper_width, arg.paper_height = Sw, Sh
    # -Z
    if arg.landscape:
        arg.paper_width, arg.paper_height = arg.paper_height, arg.paper_width
    # -L -R
    if arg.right_margin == '-L':
        arg.right_margin = arg.left_margin
    arg.left_margin, arg.left_margin2 = get_margin_margin2('L', arg.left_margin)
    arg.right_margin, arg.right_margin2 = get_margin_margin2('R', arg.right_margin)
    arg.free_width = arg.paper_width - arg.left_margin - arg.right_margin
    if arg.free_width <= 0:
        error('-L and -R too big, no horizontal space on paper')
    # -T -B
    if arg.bottom_margin == '-T':
        arg.bottom_margin = arg.top_margin
    arg.top_margin, arg.top_margin2 = get_margin_margin2('T', arg.top_margin)
    arg.bottom_margin, arg.bottom_margin2 = get_margin_margin2('B', arg.bottom_margin)
    arg.free_height = arg.paper_height - arg.top_margin - arg.bottom_margin
    if arg.free_height <= 0:
        error('-T and -B too big, no vertical space on paper')

def restore_file():
    backfile = oldbackfile(arg.file)
    if not backfile:
        error(f'Backup file for file {shortpath(arg.file)!r} not found')
    shell(f'rm -f {arg.file!r}', arg.shell_mode)
    shell(f'mv {backfile!r} {arg.file!r}', arg.shell_mode)
    if arg.verbose: inform(f'Restore: {shortpath(arg.file)!r} <-- {shortpath(backfile)!r}')

def read_file_into(buf_records):
    if not isfile(arg.file):
        error(f'File {shortpath(arg.file)!r} not found')
    header_lines, body_lines, arg.num_pages, max_body_width, max_header_width = 0, 0, 1, 0, 0
    for jlin, line in enumerate(open(arg.file)):
        line = line.replace('\t', INDENT).rstrip()
        if line.startswith(FORMFEED):
            arg.num_pages += 1
            max_header_width = max(max_header_width, len(line) - 1)
            header_lines += 1
            if arg.undo or arg.no_format:
                buf_records.append([jlin + 1, PICT, 1, 0, line])
        elif line.startswith(MACRON):
            max_header_width = max(max_header_width, len(line))
            header_lines += 1
            if arg.undo or arg.no_format:
                buf_records.append([jlin + 1, PICT, 1, 0, line])
        else:
            buf_records.append([jlin + 1, PICT, 1, 0, line])
            max_body_width = max(max_body_width, len(line))
            body_lines += 1
    if arg.verbose: inform(f"Read: yawp <-- {shortpath(arg.file)!r}")
    if arg.verbose: inform(f"    {plural(header_lines, 'header line')}, max {plural(max_header_width, 'char')} per line, {plural(arg.num_pages, 'page')}")
    if arg.verbose: inform(f"    {plural(body_lines, 'body line')}, max {plural(max_body_width, 'char')} per line")
    max_total_width = max(max_header_width, max_body_width)
    if arg.verbose: inform(f"    {plural(header_lines + body_lines, 'total line')}, max {plural(max_total_width, 'char')} per line")
    if not max_body_width:
        error(f'File {shortpath(arg.file)!r}, no printable character found')
    if arg.chars_per_line and not arg.char_width: # -w > 0 and -W == 0
        arg.char_width = arg.free_width / arg.chars_per_line # -W <-- -w
        if arg.verbose: inform(f'Compute: -W {in2str(arg.char_width)}')
        check_gt0(arg.char_width, '-W')
    elif not arg.chars_per_line and arg.char_width: # -w == 0 and -W > 0
        arg.chars_per_line = int(arg.free_width / arg.char_width) # -w <-- -W
        if arg.verbose: inform(f'Compute: -w {arg.chars_per_line}')
        check_gt0(arg.chars_per_line, '-w')
    elif not arg.chars_per_line and not arg.char_width: # -w == 0 and -W == 0
        arg.chars_per_line = max_body_width # -w <-- file
        if arg.verbose: inform(f'Compute: -w {arg.chars_per_line}')
        check_gt0(arg.chars_per_line, '-w')
        arg.char_width = arg.free_width / arg.chars_per_line # -W <-- -w
        if arg.verbose: inform(f'Compute: -W {in2str(arg.char_width)}')
        check_gt0(arg.char_width, '-W')
    if arg.calibration:
        arg.char_width2 = arg.char_width
    else:
        arg.char_width2 = arg.char_width * CWF[arg.landscape]
        if arg.verbose: inform(f'Correct: -W {in2str(arg.char_width2)}')
    arg.chars_per_inch = 1.0 / arg.char_width
    arg.chars_per_margin2 = 1.0 / arg.char_width2
    arg.char_height = arg.char_width / arg.char_aspect
    if arg.verbose: inform(f'Compute: char height {in2str(arg.char_height)}')
    if arg.calibration:
        arg.char_height2 = arg.char_height
    else:
        arg.char_height2 = arg.char_height * CHF[arg.landscape]
        if arg.verbose: inform(f'Correct: char height {in2str(arg.char_height2)}')
    arg.lines_per_inch = 1.0 / arg.char_height
    arg.lines_per_margin2 = 1.0 / arg.char_height2
    arg.lines_per_page = int(arg.lines_per_inch * arg.free_height) - 3
 
def justify_input_into_output():
    is_python_file = arg.file.endswith('.py')
    format = not is_python_file 
    for jlin, x, x, x, line in buf.input: # input --> par --> buf.output
        is_switch_line = is_python_file and "\'\'\'" in line
        if is_switch_line:
            format = not format
        if is_switch_line or not format: # Python code
            par.flush(jlin)
            buf.append(jlin, CODE, 0, 0, line)
        elif not line: # empty-line
            par.flush(jlin)
            buf.append(jlin, EMPT, 0, 0, '')
        else:
            jdot = findchar(line, '[! ]')
            if jdot >= 0 and line[jdot:jdot+2] in ['• ','. ']: # dot-line
                par.flush(jlin)
                par.append(line[jdot+2:], indent=jdot+2)
            elif line[0] == ' ': # indented-line
                if par.string:
                    par.append(line)
                else:
                    if len(line) > arg.chars_per_line:
                        error(f'Length of picture line is {len(line)} > -w {arg.chars_per_line}', jlin, line)
                    buf.append(jlin, PICT, 0, 0, line)
            else: # unindented-line
                par.append(line)
    par.flush(jlin)
    if is_python_file and format:
        error('Python file, odd number of switch lines')

def delete_redundant_empty_lines():
    '''reduce multiple EMPT lines between TEXT line and TEXT line
    (or between TEXT line and EOF) to one EMPT line only'''
    jout, first, last, kind0 = 0, -1, -1, PICT
    while jout < len(buf.output):
        kind = buf.output[jout][KIND]
        if kind0 == TEXT == kind and 0 < first < last:
            del buf.output[first:last]
            jout -= last - first
        if kind == EMPT:
            if first < 0: first = jout
            last = jout
        else: # kind in [TEXT, PICT, CODE]
            kind0 = kind
            first, last, = -1, -1
        jout += 1
    if kind0 == TEXT and 0 < first < last:
        del buf.output[first:last]

def redraw_segments():
    chstr = '`─│┐│┘│┤──┌┬└┴├┼'
    #        0123456789ABCDEF
    chset = frozenset(chstr)
    for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
        if kind == PICT:
            chars = list(line)
            for jchar, char in enumerate(chars):
                if char in chset:
                    chars[jchar] = chstr[1 * (buf.char(jout, jchar - 1) in chset) +
                                         2 * (buf.char(jout + 1, jchar) in chset) +
                                         4 * (buf.char(jout - 1, jchar) in chset) +
                                         8 * (buf.char(jout, jchar + 1) in chset)]
            buf.output[jout][LINE] = ''.join(chars)
    
def redraw_arrowheads():
    chstr = '^▷△^▽^^^◁^^^^^^^'
    #        0123456789ABCDEF
    chset = frozenset(chstr)
    for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
        if kind == PICT:
            chars = list(line)
            for jchar, char in enumerate(chars):
                if char in chset:
                    chars[jchar] = chstr[1 * (buf.char(jout, jchar - 1) == '─') +
                                         2 * (buf.char(jout + 1, jchar) == '│') +
                                         4 * (buf.char(jout - 1, jchar) == '│') +
                                         8 * (buf.char(jout, jchar + 1) == '─')]
            buf.output[jout][LINE] = ''.join(chars)
            
def renumber_chapters():
    levels = []
    nout = len(buf.output)
    for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
        prev_line = buf.output[jout-1][LINE] if jout > 0 else ''
        next_line = buf.output[jout+1][LINE] if jout + 1 < nout else ''
        if kind == TEXT and line and not prev_line and not next_line:
            level, title = get_level_title(line)
            if level > 0: # numbered chapter line
                if level > len(levels) + 1:
                    error(f'chapter-line level > {len(levels)+1}', jlin, line)
                elif level == len(levels) + 1:
                    levels.append(1)
                else:
                    levels = levels[:level]
                    levels[-1] += 1
                prefix = '.'.join(str(level) for level in levels) + '.'
                buf.output[jout][KIND] = CHP1 if level == 1 else CHP2
                buf.output[jout][LINE] = prefix + ' ' + title
            elif shrink(line).upper() == arg.contents_title: # contents line
                buf.output[jout][KIND] = CONT
                buf.output[jout][LINE] = arg.contents_title
            elif shrink(line).upper() == arg.index_title: # index line
                buf.output[jout][KIND] = INDX
                buf.output[jout][LINE] = arg.index_title

def fill_contents():
    for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
        if kind == CONT:
            if buf.contents_start > -1:
                error('More than one contents line in file', jlin, line)
            buf.contents_start = jout
            if buf.index_stop == -1 < buf.index_start:
                buf.index_stop = jout
        elif kind == INDX:
            if buf.index_start > -1:
                error('More than one index line in file', jlin, line)
            buf.index_start = jout
            if buf.contents_stop == -1 < buf.contents_start:
                buf.contents_stop = jout
            buf.contents.append(['', arg.index_title.title(), jout])
            # index is listed in contents, while contents doesn't
        elif kind in [CHP1, CHP2]:
            prefix, title = (line.split(None, 1) + [''])[:2]
            if buf.contents_stop == -1 < buf.contents_start:
                buf.contents_stop = jout
            if buf.index_stop == -1 < buf.index_start:
                buf.index_stop = jout
            buf.contents.append([prefix, title.title(), jout])
    if buf.contents_start > -1 == buf.contents_stop:
        buf.contents_stop = len(buf.output)
    elif buf.index_start > -1 == buf.index_stop:
        buf.index_stop = len(buf.output)

def fill_index():
    quote = False; subject = ''; in_contents_or_index = False; index = Setdict()
    for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
        if kind in [CONT, INDX]:
            in_contents_or_index = True
        elif kind in [CHP1, CHP2]:
            in_contents_or_index = False
        if kind in [TEXT, PICT] and not in_contents_or_index:
            for jchar, char in enumerate(line + ' '):
                if quote:
                    if (char == '"' and
                        get(line, jchar-1, ' ') not in QUOTES and
                        get(line, jchar+1, ' ') not in QUOTES):
                        index.add(shrink(subject), jout)
                        quote = False
                    else:
                        subject += char
                        if len(subject) > arg.max_subject:
                            error(f'Length of subject "{subject}..." > -s {arg.max_subject}')
                elif (char == '"' and
                      get(line, jchar-1, ' ') not in QUOTES and
                      get(line, jchar+1, ' ') not in QUOTES):
                    subject = ''
                    quote = True
        else:
            if quote:
                error('Unpaired \'"\' found while filling the index')
    if quote:
        error('Unpaired \'"\' found while filling the index')
    buf.index = sorted(index.items())

def insert_contents():
    jlin = buf.output[buf.contents_start][JLIN]
    del buf.output[buf.contents_start + 1:buf.contents_stop] # delete old contents
    buf.output.insert(buf.contents_start + 1, [jlin, TEXT, 0, 0, '']) # insert new contents
    fmt_prefix = max((len(prefix) for prefix, titl, jpag in buf.contents), default=0)
    fmt_title = max((len(titl) for prefix, titl, jpag in buf.contents), default=0)
    for prefix, title, jpag in buf.contents[::-1]:
        buf.output.insert(buf.contents_start+1,
            [jlin, TEXT, 0, 0, f'{INDENT}• {edit(prefix, fmt_prefix)} {edit(title, fmt_title)}'])
    buf.output.insert(buf.contents_start+1, [jlin, TEXT, 0, 0, ''])

def insert_index():
    jlin = buf.output[buf.index_start][JLIN]
    del buf.output[buf.index_start + 1:buf.index_stop] # delete old index
    buf.output.insert(buf.index_start + 1, [jlin, TEXT, 0, 0, '']) # insert new index
    fmt_subject = max((len(subject) for subject, jouts in buf.index), default=0)
    for subject, jouts in buf.index[::-1]:
        buf.output.insert(buf.index_start+1,
            [jlin, TEXT, 0, 0, f'{INDENT}• {edit(subject, fmt_subject)}'])
    buf.output.insert(buf.index_start+1, [jlin, TEXT, 0, 0, ''])

def insert_contents_and_index():
    if -1 < buf.contents_start < buf.index_start: 
        insert_contents()
        index_shift = (len(buf.contents) + 2) - (buf.contents_stop - buf.contents_start - 1)
        buf.index_start += index_shift
        buf.index_stop += index_shift
        insert_index()
    elif -1 < buf.index_start < buf.contents_start:
        insert_index()
        contents_shift = (len(buf.index) + 2) - (buf.index_stop - buf.index_start - 1)
        buf.contents_start += contents_shift
        buf.contents_stop += contents_shift
        insert_contents()
    elif -1 < buf.contents_start:
        insert_contents()
    elif -1 < buf.index_start:
        insert_index()

def count_picture_lines():
    jpic = 0
    for jout, (jlin, kind, jpag, lpic, line) in retroenum(buf.output):
        if kind == PICT:
            jpic += 1
            if jout == 0 or buf.output[jout-1][KIND] != PICT:
                buf.output[jout][LPIC] = jpic
        else:
            jpic = 0

def count_pages():
    jpag, jpagline = 1, 0
    for jout, (jlin, kind, zero, lpic, line) in enumerate(buf.output):
        if (jpagline + lpic * (lpic < arg.lines_per_page) >= arg.lines_per_page or
            arg.form_feed_chap and kind in [CONT, INDX, CHP1] and not
            (jout >= 2 and not buf.output[jout-1][LINE] and buf.output[jout-1][JPAG] > buf.output[jout-2][JPAG])):
            jpag += 1
            jpagline = 0
        else:
            jpagline += 1
        buf.output[jout][JPAG] = jpag
    arg.tot_pages = jpag

def add_page_numbers_to_contents():
    if buf.contents_start > -1:
        fmt_jpag = len(str(buf.output[-1][JPAG])) + 1
        for jcontents, (prefix, titl, jout) in enumerate(buf.contents):
            buf.output[buf.contents_start + 2 + jcontents][LINE] += edit(buf.output[jout][JPAG], fmt_jpag)

def add_page_numbers_to_index():
    if buf.index_start > -1:
        for jindex, (subject, jouts) in enumerate(buf.index):
            for strjpag in [(', ' if jjpag else ' ') + str(jpag) for jjpag, jpag in
                            enumerate(sorted(set(buf.output[jout][JPAG] for jout in jouts)))]:
                if len(buf.output[buf.index_start + 2 + jindex][LINE]) + len(strjpag) > arg.chars_per_line:
                    error('No more space to add page numbers to index')
                buf.output[buf.index_start + 2 + jindex][LINE] += strjpag
    
def insert_page_headers():
    jout = 0; jpag0 = 1; chapter = ''; npag = buf.output[-1][JPAG]
    header2 = arg.chars_per_line * MACRON
    while jout < len(buf.output):
        jlin, kind, jpag, lpic, line = buf.output[jout]
        if kind in [CONT, INDX, CHP1]:
            chapter = line.title()
        if jpag > jpag0:
            left, right = ((arg.even_right, arg.even_left) if arg.all_pages_E_e else
                           (arg.odd_left, arg.odd_right) if jpag % 2 else
                           (arg.even_left, arg.even_right))
            PpfeYmdHMSnNc = arg.PpfeYmdHMS + (str(jpag), str(npag), chapter)
            left = change(left, 'PpfeYmdHMSnNc', PpfeYmdHMSnNc, '%')
            right = change(right, 'PpfeYmdHMSnNc', PpfeYmdHMSnNc, '%')
            blanks = ' ' * (arg.chars_per_line - len(left) - len(right))
            if not blanks:
                header1 = f'{left} {right}' 
                error(f"Length of header {header1!r} is {len(header1)} > -w {arg.chars_per_line}")
            header1 = f'{FORMFEED}{left}{blanks}{right}'
            buf.output.insert(jout, [0, HEA2, jpag, 0, header2])
            buf.output.insert(jout, [0, HEA1, jpag, 0, header1])
            jout += 2
            jpag0 = jpag
        elif jout >= 3 and not buf.output[jout-1][LINE] and buf.output[jout-3][LINE].startswith(FORMFEED):
            left, right = ((arg.even_right, arg.even_left) if arg.all_pages_E_e else
                           (arg.odd_left, arg.odd_right) if jpag % 2 else
                           (arg.even_left, arg.even_right))
            PpfeYmdHMSnNc = arg.PpfeYmdHMS + (str(jpag), str(npag), chapter)
            left = change(left, 'PpfeYmdHMSnNc', PpfeYmdHMSnNc, '%')
            right = change(right, 'PpfeYmdHMSnNc', PpfeYmdHMSnNc, '%')
            blanks = ' ' * (arg.chars_per_line - len(left) - len(right))
            if not blanks:
                header1 = f'{left} {right}' 
                error(f"Length of header {header1!r} is {len(header1)} > -w {arg.chars_per_line}")
            buf.output[jout-3][LINE] = f'{FORMFEED}{left}{blanks}{right}'
        jout += 1

def backup_file():
    backfile = newbackfile(arg.file, arg.start_time)
    shell(f'mv {arg.file!r} {backfile}', arg.shell_mode)
    if arg.verbose: inform(f'Backup: {shortpath(arg.file)!r} --> {shortpath(backfile)!r}')

def rewrite_file():
    header_lines, body_lines, arg.num_pages, max_body_width, max_header_width = 0, 0, 1, 0, 0
    with open(arg.file, 'w') as output:
        for jlin, kind, jpag, lpic, line in buf.output:
            print(line, file=output)
            if line.startswith(FORMFEED):
                arg.num_pages += 1
                max_header_width = max(max_header_width, len(line) - 1)
                header_lines += 1
            elif line.startswith(MACRON):
                max_header_width = max(max_header_width, len(line))
                header_lines += 1
            else:
                max_body_width = max(max_body_width, len(line))
                body_lines += 1
    if arg.verbose: inform(f"Rewrite: yawp --> {shortpath(arg.file)!r}")
    if arg.verbose: inform(f"    {plural(header_lines, 'header line')}, max {plural(max_header_width, 'char')} per line, {plural(arg.num_pages, 'page')}")
    if arg.verbose: inform(f"    {plural(body_lines, 'body line')}, max {plural(max_body_width, 'char')} per line")
    max_total_width = max(max_header_width, max_body_width)
    if arg.verbose: inform(f"    {plural(header_lines + body_lines, 'total line')}, max {plural(max_total_width, 'char')} per line")

def print_output_into_stdout():
    if arg.verbose: inform(f'Print: {shortpath(arg.file)!r} --> stdout')
    for rec in buf.output:
        print(rec[LINE])

def export_output_into_file_pdf():
    shell(f'lp -d PDF '
          f'-o print-quality={arg.print_quality+3} '
          f'-o media=Custom.{in2pt(arg.paper_width)}x{in2pt(arg.paper_height)} '
          f'-o cpi={arg.chars_per_margin2} '
          f'-o lpi={arg.lines_per_margin2} '
          f'-o page-top={in2pt(arg.top_margin2)} '
          f'-o page-left={in2pt(arg.left_margin2)} '
          f'-o page-right={0 if arg.num_pages > 1 else in2pt(arg.right_margin2)} '
          f'-o page-bottom={0 if arg.num_pages > 1 else in2pt(arg.bottom_margin2)} '
          f'{arg.file!r}', arg.shell_mode)
    file = splitpath(arg.file)[-1]
    while shell(f'lpq -P PDF | grep {file}', arg.shell_mode):
        sleep(0.1) # wait lp completion
    file_pdf = lastfile('~/PDF/*.pdf')
    if not file_pdf:
        error('Exported PDF file not found')
    shell(f'rm -f {arg.file_pdf!r}', arg.shell_mode)
    shell(f'mv {file_pdf!r} {arg.file_pdf!r}', arg.shell_mode)
    if arg.verbose: inform(f'Export: {shortpath(arg.file)!r} --> {shortpath(arg.file_pdf)!r}')

def open_file_pdf():
    shell(f'xdg-open {arg.file_pdf}', arg.shell_mode)

#-----main -----

def main():
    try:
        simplefilter('ignore')
        get_arguments()
        check_arguments()
        if arg.undo: # -U ?
            restore_file()
            read_file_into(buf.output)
        elif arg.no_format: # -N ?
            read_file_into(buf.output)
            if arg.graphics: # -g ?
                redraw_segments()
                redraw_arrowheads()
            backup_file()
            rewrite_file()
        else: # not -U and not -N ?
            read_file_into(buf.input)
            justify_input_into_output()
            delete_redundant_empty_lines()
            if arg.graphics: # -g ?
                redraw_segments()
                redraw_arrowheads()
            renumber_chapters()
            fill_contents()
            fill_index()
            insert_contents_and_index()
            if arg.form_feed: # -f or -F ?
                count_picture_lines()
                count_pages()
                add_page_numbers_to_contents()
                add_page_numbers_to_index()
                insert_page_headers()
            backup_file()
            rewrite_file()
        if arg.print_file: # -p ?
            print_output_into_stdout()
        if arg.file_pdf: # -P ?
            export_output_into_file_pdf()
            open_file_pdf()
    except KeyboardInterrupt:
        print()

if __name__ == '__main__':
    main()

#----- end -----
