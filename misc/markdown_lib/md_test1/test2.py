# -*- coding: utf-8 -*-
###############################################################################
import sys
import argparse
from os.path import expanduser
from pathlib import Path
from string import Template

import markdown


def filenames(folder, extension):
    if extension.startswith('*.'):
        ext = extension
    else:
        ext = '*.' + extension
    p = Path(folder)
    return [str(path.resolve()) for path in p.glob(ext)]

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('folder',
                        help="Name of folder with markdown files")
    parser.add_argument('-e', '--extension',
                        default='*.md',
                        required=False,
                        help="Extension of markdown files")
    arguments = parser.parse_args(args)
    fn = filenames(arguments.folder, arguments.extension)
    mdc = markdown.Markdown(output_format='html5')
    content = Template(
        """
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        $body
    </body>
</html>
        """
    )
    # paths
    home = Path(expanduser('~'))
    html_folder = home / 'html-from-markdown'
    if not html_folder.is_dir(): html_folder.mkdir()
    for name in fn:
        text = ''
        mdfile = Path(name)
        with mdfile.open(mode='r', encoding='utf-8') as f:
            text = f.read()
        html_body = mdc.convert(text)
        html_file = html_folder / '.'.join([mdfile.stem, 'html'])
        with html_file.open(mode='w', encoding='utf-8') as outfile:
            outfile.write(content.safe_substitute(body=html_body))

if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)
