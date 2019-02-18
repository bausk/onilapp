nodist 10
docker container prune -f
docker run --name redis -p 6379:6379 -d redis:alpine
pipenv run python application.py
