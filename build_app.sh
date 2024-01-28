git add .
git commit -m "$1"
git push origin -u main:main
docker build -t palondomus/caesaraiyoutube:finest .
docker push palondomus/caesaraiyoutube:finest
docker run -it -p 8080:8080 palondomus/caesaraiyoutube:finest