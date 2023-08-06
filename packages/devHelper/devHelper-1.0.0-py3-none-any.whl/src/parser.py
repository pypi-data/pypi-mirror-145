from argparse import ArgumentParser
from .search import Search


def main():

    search = Search()

    program_name = "devHelper - your friendly neighborhood CLI helper."
    description = "We help you find answers to your coding problems right from the command line."

    parser = ArgumentParser(
        prog=program_name, description=description, allow_abbrev=False)

    parser.add_argument('question', type=str)

    parser.add_argument('-open', type=int)

    parser.add_argument('-page', type=int)

    args = parser.parse_args()

    if args.question and args.open is None and args.page is None:

        search.search(args.question)

    elif args.question and args.open is not None and args.page is None:

        search.searchAndOpen(args.question, args.open)

    elif args.question and args.page is not None and args.open is None:

        search.search(args.question, args.page)


main()
