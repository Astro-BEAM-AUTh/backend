FROM ghcr.io/astral-sh/uv:bookworm-slim

# Install the project into `/app`
WORKDIR /app

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

CMD ["uv", "run", "backend"]