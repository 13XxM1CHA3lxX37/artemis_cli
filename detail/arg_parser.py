import argparse

class ArgParser(argparse.ArgumentParser):
    def __init__(self):
        super(ArgParser, self).__init__(
            description='A command-line application for tutors to more productively grade programming excises on ArTEMiS')

        sub_parsers = self.add_subparsers(
            title='actions',
            dest='command',
            description='List of valid actions',
            help='Additional help',
            parser_class=argparse.ArgumentParser)

        repos_parser = sub_parsers.add_parser('repos',
            help='Download student exercise repositories')

        repos_parser.add_argument('-a', '--assignment',
            metavar='assignment',
            nargs=None,
            help='The assignment to be processed (e.g. w01h01)')

        repos_parser.add_argument('-s', '--students',
            metavar='tumId',
            nargs='+',
            help='The students TUM ids to be processed (e.g. ge36feg ba12sup, ...)')

        scores_parser = sub_parsers.add_parser('scores',
            help='Get scores for students\' assignments [not yet implemented]')

        scores_parser.add_argument('-a', '--assignment',
            metavar='assignment',
            nargs=None,
            help='The assignment to be processed (e.g. w01h01)')

        scores_parser.add_argument('-s', '--students',
            metavar='tumId',
            nargs='+',
            help='The students TUM ids to be processed (e.g. ge36feg ba12sup, ...)')

        # newresult
        # sytax:
        # -a w01h01 -s ab43cde
        # -score 80 -text "Gut gemacht "
        #   -positive "Kommentare" "Gute Dokumentation"
        #   -negative "Formatierung" "Bitte nutze Autoformat"
        result_parser = sub_parsers.add_parser('newresult',
            help='Post a new result for a student\'s assignment [not yet implemented]')

        result_parser.add_argument('-a', '--assignment',
            metavar='assignment',
            required=True,
            nargs=None,
            help='The assignment to be processed (e.g. w01h01)')

        result_parser.add_argument('-s', '--student',
            required=True,
            metavar='tum_id',
            nargs=None,
            help='The students TUM id to be processed (e.g. ge36feg)')

        result_parser.add_argument('-score',
            metavar='score',
            required=True,
            type=int,
            nargs=None,
            help='The Score of the assignment (e.g. 80)')

        result_parser.add_argument('-text',
            required=True,
            metavar='result_text',
            nargs=None,
            help='The Result Text of the assignment (e.g. "Gut gemacht")')

        result_parser.add_argument('-pos', '--positive',
           metavar=('text', 'detail_text'),
           nargs=2,
           action='append',
           help='A positive feedback consisting of Text and Detail Text (e.g. "Dokumentation" "Gute und akkurate Kommentare")')

        result_parser.add_argument('-neg', '--negative',
           metavar=('text', 'detail_text'),
           nargs=2,
           action='append',
           help='A negative feedback consisting of Text and Detail Text (e.g."Formatierung" "Bitte Autoformatierung benutzen")')

        # allows only one of the specified arguments
        group = self.add_mutually_exclusive_group()
        group.add_argument('-q', '--quiet', action='store_true', help='Print quiet')
        group.add_argument('-v', '--verbose', action='store_true', help='Print verbose')