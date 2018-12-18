if [ $# -eq 0 ]
  then
    echo "Informe apenas a versão para gerar apenas localmente:"
    echo "  release 1.1"
    echo "ou informe -d e a versão para enviar para o Docker Hub:"
    echo "  release -d 1.1"
fi

if [ $# -eq 1 ]
  then
    echo "Generating local version $1"
    echo ""
    docker build -t ifrn/ege.django_base:$1 --force-rm .
fi

if [ $# -eq 2 ] && [[ "$1" == "-d" || "$1" == "-gh" || "$1" == "-dh" ]]
  then
    echo "Generating and deploy version $2"
    echo ""

    if [[ "$1" == "-d" || "$1" == "-dh" ]]
      then
        echo ""
        echo "Docker Hub: Building and sending"
        echo ""
        docker build -t ifrn/ege.django_base:$2 --force-rm .
        docker login
        docker push ifrn/ege.django_base:$2
    fi

    if [[ "$1" == "-d" || "$1" == "-gh" ]]
      then
        echo ""
        echo "GitHub: Committing and pushing"
        echo ""
        git commit -m 'Release $2'
        git tag $2
        git push --tags origin master
    fi
fi

echo ""
echo "Done."
