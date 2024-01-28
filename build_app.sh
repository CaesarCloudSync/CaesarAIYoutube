git add .
git commit -m "$1"
git push origin 
docker build -t palondomus/caesaraiyoutube:latest .
docker push palondomus/caesaraiyoutube:latest
docker run -it -p 8080:8080 palondomus/caesaraiyoutube:latest