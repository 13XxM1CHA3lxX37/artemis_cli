#!/bin/bash

# TODO
# - refactor
# - make artemis-cli the main interface for all operations but split operation into
#  different bash scripts/aliases:
#   ./repos
#   ./grade w02h03 
#   ./grades scores

# For a more pleasant experience save credentials by enabling the credentials storage in git
# $ git config --global credential.helper store

# Import settings
. artemis-cli.config

bitbucket=$bitbucket
course_name=$course_name
course_id=$course_id

username=$username
password=$password

if [ -z "${username}" ] || [ -z "${password}" ]; then
  echo 'Artemis credentials needed: Enter your username and password into `artemis-cli.config`'
  exit 1
fi

# tum ids of students
declare -a students=(
  'solution' 'tests' 'exercise'
  # You can insert TUM IDs here or pass them seperated with spaces via the command line (commas are removed)
)

if [[ ! ($# -gt 0) ]]; then
  echo 'Usage: ./artemis-cli.sh assignment [tum_id1, ..., tum_idN] (e.g.: ./artemis-cli.sh w01h01 ge36moy, ge37moy, ge38moy)'
  exit 1
fi

if [[ $course_name -eq 'pgdp1920' && ! ($1 =~ ^w[0-9]+[hp][0-9]+$) ]]; then
  echo 'Assignment names in the PGdP course have to match w[0-9]+[hp][0-9]+'
  exit 1
fi

due_date=$(detail/artemis_cli.py deadline $course_id $1 $username $password)

if [[ $? -ne 0 ]]; then
  exit 1
else
  echo "Checking out 'master@{deadline="$due_date"}'"
fi

for ((i = 2; i <= $#; i++ )); do
  student=$(echo ${!i} | sed 's/,//g')
  students+=("$student")
done

mkdir -p $1
cd $1

if [[ $? -ne 0 ]]; then
  printf "\e[91mFailed to create parent folder, check your permissions.\e[39m"
fi

touch scores
printf "#exercise:\"$1\"\n" > scores

cwd=$(pwd)

for i in "${students[@]}"
do
  printf "Fetching $i... \c"

  repo_local="$i"
  repo_remote="$course_name$1-$i"
  repo_url="https://$bitbucket/scm/$course_name$1/$repo_remote.git"

  {
    cd "$repo_local"
    git checkout master 1>/dev/null
    cd "$cwd"

    if ! git -C "$repo_local" pull --quiet && ! git clone --quiet "$repo_url" "$repo_local"; then
      printf "\e[91mfailed (1).\e[39m\n"
      continue
    fi

    cd "$repo_local"

    if [[ $? -eq 0 ]]; then
      printf "\e[92mok.\e[39m\n"
    else
      printf "\e[91mfailed.\e[39m\n"
      continue
    fi

    if [ "$i" != "exercise" ] && [ "$i" != "solution" ] && [ "$i" != "tests" ]; then
      git checkout `git rev-list -1 --before="$due_date" master`
    fi

    git remote set-url --push origin forbidden
    cd "$cwd"
  } 2>/dev/null
done