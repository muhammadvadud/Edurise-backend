FROM jscorptech/edutop:v0.1

WORKDIR /code

COPY pyproject.toml pyproject.toml

RUN poetry lock && poetry install

CMD ["sh", "entrypoint.sh"]