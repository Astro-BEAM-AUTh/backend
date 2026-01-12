# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->

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
