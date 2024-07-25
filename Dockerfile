FROM python:3.12.2

# Install Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN poetry install --no-interaction --no-ansi --without dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

# Run the server
CMD [ "poetry", "run", "python", "flask_app.py", "--host=0.0.0.0", "--port=5000" ]
