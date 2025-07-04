# Select virtual environment and run main file
activate venv
`.\.venv\Scripts\activate`

run main
`python -m src.main`


# base-lambda-scraper
[claude multi docker chat](https://claude.ai/chat/dbda571c-85f3-421f-a1c3-b854627d12e5)


Build the container
`docker build -t base-lambda-scraper .`

docker run base-lambda-scraper