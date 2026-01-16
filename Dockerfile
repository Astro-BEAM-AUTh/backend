FROM ghcr.io/astral-sh/uv:bookworm-slim

# Setup a non-root user
# RUN groupadd --system --gid 999 nonroot \
#  && useradd --system --gid 999 --uid 999 --create-home nonroot

# Install the project into `/app`
WORKDIR /app

COPY . /app

RUN uv sync


# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# USER nonroot

CMD ["uv", "run", "backend"]