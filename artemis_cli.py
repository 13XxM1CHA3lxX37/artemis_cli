#!/usr/bin/env python

# pip install pyyaml argparse requests json typing
import yaml
import os
import sys
import re
import subprocess

from detail.artemis_api import ArtemisAPI
from detail.arg_parser import ArgParser

from detail.artemis_api_payloads import NewResultBody

def run_git(params, cwd=None):
    params = ['git'] + params

    if args.verbose:
        return subprocess.call(params, cwd=cwd)

    p = subprocess.Popen(params, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, _ = p.communicate()
    return p.returncode

def generate_gradebook(students):
    pass # TODO

def command_repos():
    # TODO apply sanizization in main function
    assignment = args.assignment

    if course_name == "pgdp1920":
        regex = "^w[0-9][0-9]%s[hp][0-9][0-9]%s$"

        if not re.match(regex % ('?', '?'), assignment):
            raise RuntimeError('Assignment name doesn\'t match the shortName convention of PGdP course')

        if not re.match(regex % ('', ''), assignment):
            print('Warning: Usually shortNames for exercises follow the convention "w01h01", find the shortName on ArTEMiS if pulling the repos fails')

    students = args.students
    # remove whitespaces, commas and duplicates
    students = list(set(filter(lambda s: s, [s.replace(' ', '').replace(',', '') for s in students])))

    exercise = api.get_exercise(assignment)
    deadline = None if exercise is None else api.get_deadline(exercise)

    num_students = len(students)

    if num_students == 0:
        raise RuntimeError('No valid student name in args.students')

    students.extend(['exercise', 'solution', 'tests'])

    script_dir = os.path.dirname(os.path.realpath(__file__))

    print('Fetching %s assignment %s for student%s.' % (course_name, assignment, '' if num_students == 1 else 's'))

    for student in students:
        sys.stdout.write('Fetching assigment for %s... ' % student)
        sys.stdout.flush()

        repo_name = "%s%s-%s" % (course_name, assignment, student)
        repo_url = os.path.join(bitbucket, 'scm', course_name + assignment, repo_name + '.git')

        # TODO create a folder structure unless flatten option in config is set
        repo_dir = os.path.join(script_dir, repo_name)

        if os.path.exists(repo_dir):
            # directory for repo already exists
            if not os.path.exists(os.path.join(repo_dir, '.git')):
                print('failed! Directory for student\'s repository already existed but wasn\'t a git repository.')
                continue

            run_git(['checkout', 'master'], cwd=repo_dir)

            status = run_git(['pull'], cwd=repo_dir)

        else:
            os.mkdir(repo_dir)

            status = run_git(['clone', repo_url, repo_dir], cwd=repo_dir)
            if status != 0:
                os.rmdir(repo_dir)
                print('failed! `git clone` returned %d.' % status)
                continue

            if not any(student in s for s in ['exercise', 'solution', 'tests']):
                # TODO checkout master@deadline
                # git checkout `git rev-list -1 --before="$due_date" master`
                pass

            # set push url to `forbidden` to avoid accidental pushes into student repository
            run_git(['remote', 'set-url', '--push', 'origin', 'forbidden'], cwd=repo_dir)

        print("ok!")
        pass

def command_get_scores():
    print('Chosen command: getscores not implemented yet.')
    sys.exit(1)

def command_new_result():
    # TODO feedback not required

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


def main():
    global parser, args, api, bitbucket, course_name, course_id

    # disable stdout if --quiet

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
    course_id   = artemis['course']['id']

    # instantiate the artemis api client
    api = ArtemisAPI(artemis)

    # dispatch command
    dispatch = {
        'repos': command_repos,
        'getscores': command_get_scores,
        'newresult': command_new_result
    }

    dispatch[args.command]()

if __name__=="__main__":
    main()

# TODO finish implementing API in detail/artemis_api.py
# TODO port backup/artemis-cli.sh to python
# TODO create symlink to tests repository for every student's submission to
#      make testing a lot easier
# TODO add feature to upload grades
# TODO create an eclipse/intellij project containing all student's submissions)
