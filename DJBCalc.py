import argparse
from typing import Optional, Sequence
def parseArgs(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    
    parser = argparse.ArgumentParser(description="A tool to help idenitfy bias in debate judges' records\nBy Lev Shuster\nFor Lisence and more information go to https://github.com/levshuster/Debate-Judge-Bias-Calculator")
    
    #ANALYSIS
    
    
    # CREATE
    parser.add_argument('--create', type=int, help='create a new judge from a tabroom judge id')
    parser.add_argument('--search', '-s', type=str, action='store', help='save a judge from their first and last name')
    
    # SAVING
    parser.add_argument("--load", '-l', type=str, help="load a saved judge, requres a file location specified with -f")
    parser.add_argument("--save", action="store_false", default=True, help="save a judge, requires a file location specified with -f, true by default, to disable enter --save=False")
    parser.add_argument("--autocache", action="store_false", default=True, help="auto updates cach, is tru by default, to disable enter --auto-cache=False")
    
    # FILTER
    parser.add_argument("--filterByDate", type=str, help="filter a list of rounds by dates, given as two dates seperated by a colon in the format of YYYY-MM-DD (2018-1-1:2022-1-1)")
    parser.add_argument("--filterByDivision", type=str, choices=("JV", "Varcity", "Novice"), help="filter a list of rounds by division")
    parser.add_argument("--filterByFormat", type=str, choices=("Policy", "Lincon-Douglas", "Public-Forum"), help="filter a list of rounds by format")

    
    # SYSTEM
    parser.add_argument("--file", '-f', type=str, action='append', required=True, default=[], help="specify a file location")
    parser.add_argument('--verbose', '-v', action='store_true', help='Print more information')
    parser.add_argument('--debug', '-d', action='store_true', help='Print debug information')
    parser.add_argument('--quiet', '-q', action='store_true', help='Print less information')
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.0')
    parser.add_argument('--config', '-c', type=str, default="config.txt", help='Load a config file')
    args = parser.parse_args(argv)
    
def actOn(args: argparse.Namespace) -> None:
    print(args)
    
def main(argv: Optional[Sequence[str]] = None) -> int:
    actOn(parseArgs(argv))
    return 0
    
if __name__ == '__main__':
    exit(main(None))
