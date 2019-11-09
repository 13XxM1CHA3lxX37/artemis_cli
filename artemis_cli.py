#!/usr/bin/env python

# pip install pyyaml argparse requests json typing
import yaml
import os
import sys

from detail.artemis_api import ArtemisAPI
from detail.arg_parser import ArgParser

from detail.artemis_api_payloads import NewResultBody

# parse arguments
parser = ArgParser()
args = parser.parse_args()

# load config
with open('config.yml', 'r') as config_file:
    cfg = yaml.safe_load(config_file)

# alias commonly used config fields
artemis     = cfg['artemis']
bitbucket   = cfg['bitbucket']['base_url']
course_name = artemis['course']['name']

# instantiate the artemis api client
api = ArtemisAPI(artemis)

def action_repos(quiet=False, verbose=False):
    print('Fetching %s assignment %s for students...\n' % (course_name, assignment))

    students = args.students
    students.extend(['exercise', 'solution', 'tests'])

    assignment = args.assignment

    for student in students:
        # TODO unflatten project structure, add option to flatten it
        # TODO add option to customize path to root folder

        # example repo url: https://bitbucket.ase.in.tum.de/scm/PGDP1920W01P01/pgdp1920w01p01-ab42cde.git
        print('Fetching assigment for %s...' % (assignment, student))

        course_assignment = course_name + assignment
        remote_repo = course_name + '-' + student + '.git'

        local_repo = os.path.join('..', course_assignment + '-' + student)

        if not os.path.exists(local_repo):
            os.mkdir(local_repo)

        os.chdir(local_repo)

        repo_url = os.path.join(bitbucket, 'scm', course_assignment, remote_repo)
        clone_cmd = 'git clone ' + repo_url
        print(clone_cmd)
        os.system(clone_cmd)
        # TODO: no access to repo ('The requested repository does not exist, or you do
        #  not have permission to access it.')


def action_get_scores(quiet=False, verbose=False):
    print('Chosen command: getscores not implemented yet.')
    sys.exit(1)

def action_new_result(quiet=False, verbose=False):

    positive_feedback_entries = [] # type: List[Dict[str, str]]
    if args.positive is not None:
        for pos_feedback in args.positive:
            positive_feedback_entries.append(dict(text=pos_feedback[0], detail_text=pos_feedback[1]))
    negative_feedback_entries = [] # type: List[Dict[str, str]]
    if args.negative is not None:
        for neg_feedback in args.negative:
            negative_feedback_entries.append(dict(text=neg_feedback[0], detail_text=neg_feedback[1]))

    new_result_body = NewResultBody(
        score=args.score,
        result_text=args.text,
        positive_feedback_entries=positive_feedback_entries,
        negative_feedback_entries=negative_feedback_entries
    )

    print('Chosen command: newresult not implemented yet but here\'s the data that would be sent to ArTEMiS:')

    api.post_new_result(new_result_body=new_result_body,
                        assignment=args.assignment,
                        student=args.student)
    sys.exit(1)

# MAIN
command_dispatch = {
    'repos': action_repos,
    'getscores': action_get_scores,
    'newresult': action_new_result,
}

command_dispatch[args.command](quiet=args.quiet, verbose=args.verbose)


# TODO finish implementing API in detail/artemis_api.py
# TODO port backup/artemis-cli.sh to python
# TODO create symlink to tests repository for every student's submission to
#      make testing a lot easier
# TODO add feature to upload grades
# TODO create an eclipse/intellij project containing all student's submissions)
