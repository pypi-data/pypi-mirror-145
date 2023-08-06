from ._logging import get_logger
from ._options import get_options, print_option
from .main import UKBSearch


def cli():
    opt = get_options()
    print_option(opt)
    opt['log'] = get_logger(silence=False, debug=False, logfile='')
    bs = UKBSearch(opt)
    bs.run()
