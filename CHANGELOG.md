# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->

## v0.7.0 (2026-05-17)

### Bug Fixes

- Add Copilot suggestions
  ([`96c235a`](https://github.com/Astro-BEAM-AUTh/backend/commit/96c235ade79b744045bd2fa39ca5b23e2eabab20))

- Add copilot suggestions from #45
  ([`6e375a4`](https://github.com/Astro-BEAM-AUTh/backend/commit/6e375a499d74e0453d7ae3a44cf8bbc5b609132f))

- Guest users can now send requests to emails already existing
  ([`5f96bd6`](https://github.com/Astro-BEAM-AUTh/backend/commit/5f96bd696b18575107cf6d364cf7f0e7771ac032))

- Normalize existing database string values when migrating to the newest version
  ([`5755ef8`](https://github.com/Astro-BEAM-AUTh/backend/commit/5755ef8946f189ea95587deb6dbf4a2c1b1cad70))

- **alembic**: Terminal commands for `current` and `history` now work as expected
  ([`4bd00df`](https://github.com/Astro-BEAM-AUTh/backend/commit/4bd00df381e247f076a035a18f1fb295e2a27cff))

- **auth**: Whitelist JWT algorithms for Supabase token verification
  ([`4d63449`](https://github.com/Astro-BEAM-AUTh/backend/commit/4d63449401bb5c34cb51999756125dae9906573b))

### Chores

- Migrate project to supabase and thus reinstantiate the initialization scripts just to be safe
  ([`9c3f228`](https://github.com/Astro-BEAM-AUTh/backend/commit/9c3f2283407a5aa44df5ed884cfc0e06478c1a08))

### Deps

- Bump the uv-dependencies group with 4 updates
  ([`2722848`](https://github.com/Astro-BEAM-AUTh/backend/commit/2722848ea815c4ddeb9cc92e885d7e06c92370b4))

### Features

- Add endpoints to get all observations and delete a specific one
  ([`a41838a`](https://github.com/Astro-BEAM-AUTh/backend/commit/a41838a9031af28aa3ecff78214b8759412034b7))

- Make the observation type an Enum
  ([`bb080e8`](https://github.com/Astro-BEAM-AUTh/backend/commit/bb080e84ef65c06566a775ba7353068ea9580576))

- **JWT**: Add support for JWT authentication
  ([`02349e6`](https://github.com/Astro-BEAM-AUTh/backend/commit/02349e66911db02d63dab947646740a921e26045))

### Refactoring

- **auth**: Decode JWT with validated header algorithm only
  ([`2d5c34e`](https://github.com/Astro-BEAM-AUTh/backend/commit/2d5c34e2a070200a5817f53d65401ad437b9a517))


## v0.6.0 (2026-05-05)

### Bug Fixes

- Align the alembic migration with the previous SQL approach
  ([`ff73bb1`](https://github.com/Astro-BEAM-AUTh/backend/commit/ff73bb167f7dfb7e49e0e80beba75270758f8cfa))

- Use Enum itself in the observation processor tool instead of its instance value
  ([`a13d9eb`](https://github.com/Astro-BEAM-AUTh/backend/commit/a13d9ebb96bc827d214fd0fb4cf7d645260eb49d))

### Features

- Create an observation processor to simulate the telescope's side
  ([`f1c5dbe`](https://github.com/Astro-BEAM-AUTh/backend/commit/f1c5dbe759d625d94d607e3ba2d99ebdfaac0638))

- Manage database through Alembic migrations and use an enumerator to define the observation status
  ([`7d56b10`](https://github.com/Astro-BEAM-AUTh/backend/commit/7d56b10ec1cc92ad0d732a74470d50ea8b1268db))

- Move the observation processor outside the backend project
  ([`626de1b`](https://github.com/Astro-BEAM-AUTh/backend/commit/626de1bdadacd62324b1203384a194af2c1224e8))


## v0.5.0 (2026-02-05)

### Chores

- **docker**: Dockerize the app in order to be deployable
  ([#19](https://github.com/Astro-BEAM-AUTh/backend/pull/19),
  [`64ca589`](https://github.com/Astro-BEAM-AUTh/backend/commit/64ca58960c2b42fdd96d1c9c675be45eb1f55b07))

- **docker**: Dockerize the app in order to be deployable
  ([`f83aa57`](https://github.com/Astro-BEAM-AUTh/backend/commit/f83aa57620b721246ce9b175466f094ac02b81e6))

- **docker**: Implement copilot's suggestions
  ([#19](https://github.com/Astro-BEAM-AUTh/backend/pull/19),
  [`64ca589`](https://github.com/Astro-BEAM-AUTh/backend/commit/64ca58960c2b42fdd96d1c9c675be45eb1f55b07))

- **docker**: Implement copilot's suggestions
  ([`d862c81`](https://github.com/Astro-BEAM-AUTh/backend/commit/d862c81b96b0d878a9b7c1064577b88efa6f9d31))

- **docker**: Use 'uv sync --frozen' to ensure reproducible builds
  ([#19](https://github.com/Astro-BEAM-AUTh/backend/pull/19),
  [`64ca589`](https://github.com/Astro-BEAM-AUTh/backend/commit/64ca58960c2b42fdd96d1c9c675be45eb1f55b07))

- **docker**: Use 'uv sync --frozen' to ensure reproducible builds
  ([`6af2d70`](https://github.com/Astro-BEAM-AUTh/backend/commit/6af2d700829ea4329b7b82e650c9bd5f843585db))

### Deps

- Bump sqlmodel from 0.0.31 to 0.0.32 in the uv-dependencies group
  ([`93ad862`](https://github.com/Astro-BEAM-AUTh/backend/commit/93ad8628a9bbcd003736c8ddc412254681f0e34e))

- Bump the uv-dependencies group with 2 updates
  ([`213f373`](https://github.com/Astro-BEAM-AUTh/backend/commit/213f373b23d824ea5932bbe52a5dc038d9fae245))

### Features

- Add favicon, exception handling on general and validation errors and correct how requests
  regarding observations are documented in fastapi
  ([`2efdc98`](https://github.com/Astro-BEAM-AUTh/backend/commit/2efdc9821f6131d27825ea943d3667d80b8d8e1e))

- Create an HTML error page and support for minimal front end handling from the server
  ([`fca1f94`](https://github.com/Astro-BEAM-AUTh/backend/commit/fca1f94398110fa33438f1ab44a4a7f73217ef15))

### Refactoring

- Remove TODO comment that was no longer applicable, change the response documentation status types
  to match the actual return types
  ([`6b95273`](https://github.com/Astro-BEAM-AUTh/backend/commit/6b95273ea19d052ddcc17350ce986325a2bb1fee))


## v0.4.1 (2026-01-12)

### Deps

- Bump fastapi from 0.123.4 to 0.124.0 in the uv-dependencies group
  ([`cd96563`](https://github.com/Astro-BEAM-AUTh/backend/commit/cd96563707b9acad76e2b6da9126b6b79bc51a63))

- Bump the uv-dependencies group across 1 directory with 5 updates
  ([`0498501`](https://github.com/Astro-BEAM-AUTh/backend/commit/04985012684e734923c3dcaa2056d1465b35cde8))

- Bump the uv-dependencies group with 3 updates
  ([`93fab12`](https://github.com/Astro-BEAM-AUTh/backend/commit/93fab1253044f995778650f70b8b6e140ab83945))

- Bump tox from 4.33.0 to 4.34.1 in the uv-dependencies group
  ([`cef65d1`](https://github.com/Astro-BEAM-AUTh/backend/commit/cef65d16bb47677954d2987cc012e993df7de3c8))

- Bump tox to v4.34.1 in the lockfile
  ([`afa7b91`](https://github.com/Astro-BEAM-AUTh/backend/commit/afa7b914466118f1968500d1eb4c9fe9e36de060))

- Pin tox to 4.34.1 in pyproject.toml ([#17](https://github.com/Astro-BEAM-AUTh/backend/pull/17),
  [`1abd5c0`](https://github.com/Astro-BEAM-AUTh/backend/commit/1abd5c0219c4ca9ccd05c42c9f07e7554c2b4cc0))

- Update tox to specific version 4.34.1 in pyproject.toml
  ([#17](https://github.com/Astro-BEAM-AUTh/backend/pull/17),
  [`1abd5c0`](https://github.com/Astro-BEAM-AUTh/backend/commit/1abd5c0219c4ca9ccd05c42c9f07e7554c2b4cc0))


## v0.4.0 (2025-12-06)

### Features

- Add explicit _subtype="plain" to MIMEText constructors for consistency
  ([`1415a2b`](https://github.com/Astro-BEAM-AUTh/backend/commit/1415a2b222e2b9e9f5d6929a9354883d24b70f2b))

- Add support for our mailserver, fix the MIME parts of the email message to include their policy &
  decouple unnecessary parameters in `_send_email()`
  ([`c8ec771`](https://github.com/Astro-BEAM-AUTh/backend/commit/c8ec771ddb9622555fa72f1ae50e29414b97ddee))


## v0.3.1 (2025-12-02)

### Deps

- Bump the uv-dependencies group across 1 directory with 3 updates
  ([`4dd8e14`](https://github.com/Astro-BEAM-AUTh/backend/commit/4dd8e14d3a594c5799814353855879fec4500d48))

- Use specific versions to denote the exact version that was used to deploy the app
  ([`bc98c7c`](https://github.com/Astro-BEAM-AUTh/backend/commit/bc98c7c47a88be43c4af9653062abfb461278b31))


## v0.3.0 (2025-12-02)

### Bug Fixes

- Add HTML escaping to numeric fields for comprehensive XSS protection
  ([`c55d88d`](https://github.com/Astro-BEAM-AUTh/backend/commit/c55d88db177e5345761a59dc00a725f0bac3f37f))

- Add HTML escaping to prevent XSS in email templates
  ([`35e1526`](https://github.com/Astro-BEAM-AUTh/backend/commit/35e1526e7493a9f92b6e472939316290b5a251cc))

### Continuous Integration

- Configure labeler action
  ([`87eb9fc`](https://github.com/Astro-BEAM-AUTh/backend/commit/87eb9fc1e989a5deb543f916ae029b6dc9ab1577))

### Documentation

- Document the command used to test the mailing functionality
  ([`0df87bf`](https://github.com/Astro-BEAM-AUTh/backend/commit/0df87bf5c626dbb36898dcadfd3b2781b18b464b))

### Features

- Add a function to send an email to notify user when their observation is complete and refactor a
  bit the email handling code to decouple its text/html templating
  ([`ec33636`](https://github.com/Astro-BEAM-AUTh/backend/commit/ec33636fc40de581bb58a41c5a92bb9a5f080b7a))

- Create initial email service support when submitting an observation request
  ([`7a6a7ee`](https://github.com/Astro-BEAM-AUTh/backend/commit/7a6a7eed3d80ec9314ab49d67864f35abf9a0c07))


## v0.2.0 (2025-11-12)

### Bug Fixes

- Correct timestamp insertions to be compatible with postgres default timestamps and add some
  examples in the user models
  ([`f2ca8af`](https://github.com/Astro-BEAM-AUTh/backend/commit/f2ca8af1f5c6ad79602b90edc320884062db0533))

### Chores

- Fix environment variables example file
  ([`8cdeb53`](https://github.com/Astro-BEAM-AUTh/backend/commit/8cdeb5347bb290d7caee2c02ef1a2357fc8c9964))

### Features

- Migrate to pydantic models sqlmodel for easier integration with the database
  ([`2a84734`](https://github.com/Astro-BEAM-AUTh/backend/commit/2a84734e4e83a07f7da1719c37edf761d1c7f9d2))


## v0.1.0 (2025-11-11)


## v0.0.0 (2025-11-07)

### Chores

- Initialize project
  ([`7622825`](https://github.com/Astro-BEAM-AUTh/backend/commit/7622825b43cc909a768ca3c9bf9429b9077f1889))
