#!/usr/bin/env bash
FULL_IMAGE_NAME="ifrn/ege.utils"
PROJECT_NAME="ege_utils"
ROOT_DIR=$( pwd )
time source $ROOT_DIR/release-base.sh


if [ $# -eq 0 ]; then
  echo ''
  echo 'NAME '
  echo '       release'
  echo 'SYNOPSIS'
  echo '       ./release.sh [-l|-g|-p|-a] <version>'
  echo 'DESCRIPTION'
  echo '       Create a new release $PROJECT_NAME image.'
  echo 'OPTIONS'
  echo '       -l         Build only locally'
  echo '       -g         Push to Github'
  echo '       -p         Registry on PyPi'
  echo '       -a         Push and registry on Github'
  echo '       <version>  Release version number'
  echo 'EXAMPLES'
  echo '       o   Build a image to local usage only:'
  echo '                  ./release.sh -l 1.0'
  echo '       o   Build and push to GitHub:'
  echo '                  ./release.sh -g 1.0'
  echo '       o   Build and registry on PyPi:'
  echo '                  ./release.sh -p 1.0'
  echo '       o   Build, push to Guthub and registry on PyPi:'
  echo '                  ./release.sh -a 1.0'
  echo "LAST TAG: $(git tag | tail -1 )"
  exit
fi

OPTION=$1
VERSION=$2

create_setup_cfg_file() {
  printf "\n\nCREATE setup.cfg file\n"
  sed "s/lib_version/$VERSION/g" $ROOT_DIR/setup.pytemplate > $ROOT_DIR/setup.py 
}

build_docker() {
  printf "\n\nBUILD local version $FULL_IMAGE_NAME:latest\n"
  docker build -t $FULL_IMAGE_NAME:latest --force-rm .
}

lint_project() {
  printf "\n\nLINT project $PROJECT_NAME $VERSION\n"
  docker run --rm -it  -v `pwd`:/src $FULL_IMAGE_NAME:latest sh -c 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && flake8 . --exclude=test_ege_utils/settings.py --count --max-complexity=10 --max-line-length=127 --statistics'
}

test_project() {
  printf "\n\nTEST project $PROJECT_NAME $VERSION\n"
  docker run --rm -it --env-file=test_ege_utils/.env  -v `pwd`:/src $FULL_IMAGE_NAME:latest sh -c 'pip install /src && cd test_ege_utils && coverage run --source="..,test_ege_utils" manage.py test . test_me && coverage report -m' 
  # ./test_ege_utils/settings.py:1:1:
}

build_project() {
  printf "\n\nBUILD project $PROJECT_NAME $VERSION\n"
  docker run --rm -it  -v `pwd`:/src $FULL_IMAGE_NAME:latest sh -c 'python setup.py sdist' 
}


push_to_github() {
  if [[ "$OPTION" == "-g" || "$OPTION" == "-a" ]]
  then
    printf "\n\n\GITHUB: Pushing\n"
    git add setup.py \
    && git commit -m "Release $PROJECT_NAME $VERSION" \
    && git tag $VERSION \
    && git push --tags origin master
  fi
}

send_to_pypi() {
  if [[ "$OPTION" == "-p" || "$OPTION" == "-a" ]]
  then
    printf "\n\n\PYPI: Uploading\n"
    docker run --rm -it -v `pwd`:/src $FULL_IMAGE_NAME:latest twine upload dist/$PROJECT_NAME-$VERSION.tar.gz
  fi
}

create_setup_cfg_file \
&& build_docker \
&& lint_project \
&& build_project \
&& test_project \
&& push_to_github \
&& send_to_pypi

echo $?
echo ""
echo "Done."
