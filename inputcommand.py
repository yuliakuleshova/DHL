""" Import command"""



import sys
import argparse


parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='Uses one of parameters',
                    epilog='Text at the bottom of help')

parser.add_argument('-c', '--count', help="Number of news to print")
parser.add_argument('-sd', '--search_by_date', help="Search by date")
parser.add_argument('-st', '--search_by_title', help="Search by title")
args = parser.parse_args()


if args.count:
    if 1 <= int(args.count) <= 50:
        print("print count news from url without DB update")
    elif int(args.count) > 50:
        print("print 50 news from url and count-50 from DB without DB update")
    else:
        print(f"{args.count} is unacceptable value. Should be positive value")
    sys.exit(0)

if args.search_by_date:
    print("Search in DB by date")
    sys.exit(0)

if args.search_by_title:
    print("Search in DB by title")
    sys.exit(0)

print("If news is not existed in DB add it")
