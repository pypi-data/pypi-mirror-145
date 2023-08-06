import logging
import sys

from patricesorter.lib.get_opts import parser
from patricesorter.lib.pricing import sort_prices

__author__ = "PatriceJada"
__copyright__ = "PatriceJada"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from patricesorter.skeleton import fib`,
# when using this Python module as a library.


def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for _i in range(n - 1):
        a, b = b, a + b
    return a


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


# def parse_args(args):
#     """Parse command line parameters

#     Args:
#       args (List[str]): command line parameters as list of strings
#           (for example  ``["--help"]``).

#     Returns:
#       :obj:`argparse.Namespace`: command line parameters namespace
#     """
#     parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
#     parser.add_argument(
#         "--version",
#         action="version",
#         version="patricesorter {ver}".format(ver=__version__),
#     )
#     parser.add_argument(dest="n", help="n-th Fibonacci number", type=int, metavar="INT")
#     parser.add_argument(
#         "-v",
#         "--verbose",
#         dest="loglevel",
#         help="set loglevel to INFO",
#         action="store_const",
#         const=logging.INFO,
#     )
#     parser.add_argument(
#         "-vv",
#         "--very-verbose",
#         dest="loglevel",
#         help="set loglevel to DEBUG",
#         action="store_const",
#         const=logging.DEBUG,
#     )
#     return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main():
    """This function launches the patricesorter."""
    if len(sys.argv) == 1:
        # if no command line args are passed, show the help options
        parser.parse_args(['-h'])

    else:

        # parse them
        args = parser.parse_args()
        # fib(int(args.nargs[0]))
        sorted_data, price_object = sort_prices(args.nargs)
        print("The {} sorted to  {}  , the first price is {} last price {}".format(args.nargs, sorted_data,
                                                                                   price_object.first,
                                                                                   price_object.last))

    # print (args)
    exit()
    # args = parse_args(sys.argv)
    # setup_logging(args.loglevel)
    # _logger.debug("Starting crazy calculations...")
    # print("The {}-th Fibonacci number is {}".format(args.n, fib(args.n)))
    # _logger.info("Script ends here")


if __name__ == "__main__":
    main()
