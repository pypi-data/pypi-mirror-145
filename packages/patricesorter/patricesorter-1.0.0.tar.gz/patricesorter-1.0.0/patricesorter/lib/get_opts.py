import argparse
from patricesorter.lib.defaults import VERSION

parser = argparse.ArgumentParser(prog="patricesorter")
parser.add_argument('-v', '--version', action='version', version=VERSION)
parser.add_argument('-q', '--quiet', help='suppress output', action='store_true')
# patricesorter 212 334 55454 4545 53
parser.add_argument('--nargs', nargs='+')
# subparsers

# patricesorter help
subparsers = parser.add_subparsers(help='sub command help', dest='command')
