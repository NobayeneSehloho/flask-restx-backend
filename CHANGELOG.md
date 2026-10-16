# Changelog - Flask-RESTX Backend

All notable changes to the backend will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [2.1.0] - 2026-10-16

### Added
- **JWT authentication enforcement** across the entire `api` namespace
  (`/api/...`). A new `token_required` decorator (`app/security.py`) reads the
  `Authorization: Bearer <token>` header, verifies the token signature and
  expiry, and returns `401` for missing, malformed, expired, or invalid
  tokens. Applied to all 17 Resource classes via
  `method_decorators = [token_required]`.
- **Swagger "Authorize" button** — the API now declares a `Bearer` security
  scheme so the interactive docs can send the token when calling protected
  endpoints.

### Changed
- The JWT signing key is now centralized in application config, read from the
  `SECRET_KEY` environment variable with a local/test fallback, instead of a
  constant defined in `auth.py`. The login endpoint (signing) and the
  `token_required` verifier (verifying) now share this single value.

### Security
- All `/api/...` endpoints now reject unauthenticated requests. The login
  endpoint (token issuance) and the `/health` check remain open by design so
  that clients can obtain a token and container/load-balancer health checks
  continue to succeed.
- The token verifier pins the signing algorithm to `HS256` to prevent
  algorithm-confusion attacks.

### Production TO DO
> This authentication is intended for a test environment. Harden the following
> before using it beyond testing:
- Provide a strong, randomly generated signing key via a secrets manager rather
  than relying on the built-in fallback; refuse to start if it is unset.
- Replace the in-memory user store and plaintext password check with a
  persisted user model and hashed passwords.
- Use short-lived access tokens with a refresh and revocation mechanism instead
  of long-lived, non-revocable tokens.
- Enforce TLS end to end.
- Add rate limiting / brute-force protection on the login endpoint.
- Log authentication failures and monitor `401` rates (never log tokens).
- Restrict or disable the interactive API docs where they should not be
  reachable.
- Replace the deprecated `datetime.utcnow()` usage with a timezone-aware
  equivalent.

## [2.0.1] - 2026-10-15

### Security
- Remediated **all 377 vulnerabilities** reported by Trivy across every
  severity (1 CRITICAL, 166 HIGH, 129 MEDIUM, 79 LOW, 2 UNKNOWN) in the
  `v2.0.0` image; the `v2.0.1` image scans clean (0 CVEs).
- **PyJWT 2.13.0 → 2.15.0** — fixes CRITICAL `CVE-2026-102268` (authentication
  bypass via improper public key validation) and the related HIGH/MEDIUM PyJWT
  advisories.
- **Werkzeug 3.1.8 → 3.1.9** — fixes `CVE-2026-102598` (DoS via `safe_join()`
  Windows special device paths).
- Alpine OS libraries (curl, openssl, libuuid, libxml2, sqlite-libs, c-ares,
  zlib) patched by rebuilding against the current Alpine 3.23 package index.

### Removed
- **`postgresql-dev`** build dependency from the Dockerfile — the application
  is SQLite-only and never used it. Removing it eliminated the entire
  `libpq`/`libecpg`/`postgresql18-dev` CVE set (~185 findings) and cut the
  image size roughly in half.

### Changed
- Dropped the redundant narrow `apk upgrade nghttp2-libs xz-libs` step; the
  single `apk upgrade --no-cache --available` now governs OS package patching.
- Image published to ECR as a multi-architecture manifest
  (`linux/amd64` + `linux/arm64`).

## [2.0.0] - 2026-05-27

### Added
- **Departments** — new model and full CRUD endpoints (`/api/departments`)
  - `GET /api/departments/{id}` returns nested courses in the response
  - `GET /api/departments/{id}/courses` — dedicated route to list a department's courses
- **Student Enrolments** — many-to-many student-course relationship via `/api/student-enrolments`
  - Students can now enrol in multiple courses
  - Response includes resolved `student_name`, `course_name`, `enrolled_at`, and `status`
- **Teacher Enrolments** — teacher-course assignment via `/api/enrolments` with `enrolled_at` and `status`
- **Course-Department link** — courses now belong to a department (`department_id` required)
- **Nested routes** for querying relationships:
  - `GET /api/students/{id}/courses` — list courses a student is enrolled in
  - `GET /api/teachers/{id}/courses` — list courses a teacher is assigned to
  - `GET /api/courses/{id}/students` — list students enrolled in a course
  - `GET /api/departments/{id}/courses` — list courses in a department
- **PATCH endpoints** for partial updates on all resources:
  - `PATCH /api/students/{id}` — update name, email, and/or student_number
  - `PATCH /api/courses/{id}` — update name and/or department
  - `PATCH /api/teachers/{id}` — update name and/or email
  - `PATCH /api/departments/{id}` — update name
- **Student fields** — `email` (required, unique) and `student_number` (required, unique)
- **Teacher email** — teachers now have a required `email` field (unique)
- **Enrolment metadata** — `enrolled_at` timestamp and `status` field (default: "active") on both student and teacher enrolments
- **Cascade deletes** — deleting a department removes its courses and their enrolments; deleting a student/teacher removes their enrolments
- **FK validation** — creating/updating a course with a non-existent `department_id` returns 404
- Proper error handling on all endpoints (404 for missing resources, 409 for duplicates)
- Input validation with `IntegrityError` handling and session rollback
- Course response includes `department_name` for readability

### Changed
- **BREAKING**: `POST /api/students` no longer accepts `course_id` — use `/api/student-enrolments` instead
- **BREAKING**: `POST /api/students` now requires `email` and `student_number` fields
- **BREAKING**: Student response no longer includes `course_id`, now includes `email` and `student_number`
- **BREAKING**: `POST /api/teachers` now requires `email` field
- **BREAKING**: Teacher response now includes `email`
- **BREAKING**: `POST /api/courses` now requires `department_id` (was optional)
- **BREAKING**: Course response now includes `department_id` and `department_name`
- **BREAKING**: Department response now includes nested `courses` array

### Removed
- Direct student-course foreign key relationship (replaced by `student_enrolment` table)
- `greenlet` and `pyrsistent` dependencies (no longer needed)

### Security
- **flask-cors** 6.0.0 → 6.0.2
- **Flask-SQLAlchemy** 3.0.3 → 3.1.1
- **SQLAlchemy** 2.0.12 → 2.0.50
- **Werkzeug** 3.1.6 → 3.1.8
- **PyJWT** 2.12.0 → 2.13.0
- **MarkupSafe** 2.1.2 → 3.0.3
- **click** 8.1.3 → 8.4.1
- **jsonschema** 4.17.3 → 4.26.0
- **typing_extensions** 4.12.2 → 4.15.0
- All dependencies updated to latest versions to address known CVEs
- Resolves all CVEs identified in v1.0.4 (nghttp2-libs, xz-libs, pip, python-dotenv)
- Trivy security scan: 0 vulnerabilities (OS + Python packages)

## [1.0.4] - 2026-05-12

### Security
- **nghttp2-libs** (1.68.0-r0 → 1.69.0-r0)
  - CVE-2026-27135 (HIGH): Denial of Service via malformed HTTP/2 frames after session termination
- **xz-libs** (5.8.2-r0 → 5.8.3-r0)
  - CVE-2026-34743 (MEDIUM): Denial of Service via buffer overflow in index decoding
- **pip** (26.0.1 → upgraded to latest)
  - CVE-2026-3219 (MEDIUM): Incorrect file installation due to improper archive handling
  - CVE-2026-6357 (MEDIUM): Arbitrary code execution or information disclosure via malicious wheel package
- **python-dotenv** (1.0.0 → 1.2.2)
  - CVE-2026-28684 (MEDIUM): Arbitrary file overwrite via symbolic link following
- Removed pip from final image to reduce attack surface
- Trivy security scan: 0 vulnerabilities

## [1.0.3] - 2026-04-14

### Security
- **libcrypto3** (3.5.5-r0 → 3.5.6-r0)
  - CVE-2026-28390 (HIGH): Denial of Service due to NULL pointer dereference in CMS
  - CVE-2026-28388 (MEDIUM): Denial of Service due to NULL pointer dereference in delta CRL
  - CVE-2026-28389 (MEDIUM): Denial of Service vulnerability in CMS processing
  - CVE-2026-31790 (MEDIUM): Information Disclosure from Uninitialized Memory via Invalid RSA Public Key
  - CVE-2026-2673 (LOW): TLS 1.3 server may choose unexpected key agreement group
  - CVE-2026-28387 (LOW): Arbitrary code execution due to use-after-free in DANE TLSA authentication
  - CVE-2026-31789 (LOW): Denial of Service via excessively large OCTET STRING conversion
- **libssl3** (3.5.5-r0 → 3.5.6-r0)
  - CVE-2026-28390 (HIGH): Denial of Service due to NULL pointer dereference in CMS
  - CVE-2026-28388 (MEDIUM): Denial of Service due to NULL pointer dereference in delta CRL
  - CVE-2026-28389 (MEDIUM): Denial of Service vulnerability in CMS processing
  - CVE-2026-31790 (MEDIUM): Information Disclosure from Uninitialized Memory via Invalid RSA Public Key
  - CVE-2026-2673 (LOW): TLS 1.3 server may choose unexpected key agreement group
  - CVE-2026-28387 (LOW): Arbitrary code execution due to use-after-free in DANE TLSA authentication
  - CVE-2026-31789 (LOW): Denial of Service via excessively large OCTET STRING conversion
- **libuuid** (2.41.2-r0 → 2.41.4-r0)
  - CVE-2026-27456 (MEDIUM): TOCTOU in mount program when setting up loop devices
- **musl** (1.2.5-r21 → 1.2.5-r23)
  - CVE-2026-40200 (UNKNOWN): Stack-based buffer overflow in musl libc
  - CVE-2026-6042 (UNKNOWN): Security flaw in musl libc up to 1.2.6
- **musl-dev** (1.2.5-r21 → 1.2.5-r23)
  - CVE-2026-40200 (UNKNOWN): Stack-based buffer overflow in musl libc
  - CVE-2026-6042 (UNKNOWN): Security flaw in musl libc up to 1.2.6
- **musl-utils** (1.2.5-r21 → 1.2.5-r23)
  - CVE-2026-40200 (UNKNOWN): Stack-based buffer overflow in musl libc
  - CVE-2026-6042 (UNKNOWN): Security flaw in musl libc up to 1.2.6
- **openssl-dev** (3.5.5-r0 → 3.5.6-r0)
  - CVE-2026-28390 (HIGH): Denial of Service due to NULL pointer dereference in CMS
  - CVE-2026-28388 (MEDIUM): Denial of Service due to NULL pointer dereference in delta CRL
  - CVE-2026-28389 (MEDIUM): Denial of Service vulnerability in CMS processing
  - CVE-2026-31790 (MEDIUM): Information Disclosure from Uninitialized Memory via Invalid RSA Public Key
  - CVE-2026-2673 (LOW): TLS 1.3 server may choose unexpected key agreement group
  - CVE-2026-28387 (LOW): Arbitrary code execution due to use-after-free in DANE TLSA authentication
  - CVE-2026-31789 (LOW): Denial of Service via excessively large OCTET STRING conversion
- Trivy security scan: 0 vulnerabilities

## [1.0.2] - 2026-03-17

### Security
- Updated PyJWT from 2.8.0 to 2.12.0 (CVE-2026-32597: missing `crit` header validation per RFC 7515 §4.1.11)
- Updated zlib from 1.3.1-r2 to 1.3.2-r0 (CVE-2026-22184, CVE-2026-27171)
- Trivy security scan: 0 vulnerabilities

## [1.0.1] - 2026-02-23

### Security
- Updated Flask from 2.3.2 to 3.1.3 (CVE fix)
- Updated Werkzeug from 3.1.5 to 3.1.6 (CVE fix)
- Updated blinker from 1.6.2 to 1.9.0 (required by Flask 3.1.3)
- Updated itsdangerous from 2.1.2 to 2.2.0 (required by Flask 3.1.3)

## [1.0.0] - 2026-02-05

### Added
- RESTful API with Flask-RESTX and Swagger documentation
- Course management endpoints (CRUD operations)
- Student management endpoints (CRUD operations)
- SQLAlchemy ORM with SQLite database
- Automatic database table creation on startup
- Health check endpoint at `/health`
- JWT authentication support
- CORS support for frontend communication
- Docker support with health checks
- Dockerfile with multi-stage optimization

### Security
- Updated flask-cors from 4.0.0 to 6.0.0 (fixed 5 CVEs)
  - CVE-2024-1681: Improper Output Neutralization for Logs
  - CVE-2024-6221: Access-Control-Allow-Private-Network vulnerability
  - CVE-2024-6866: Improper Handling of Case Sensitivity
  - CVE-2024-6839: Improper Input Validation - flawed regex pattern
  - CVE-2024-6844: Improper Input Validation - inconsistent URL path handling
- Updated typing_extensions from 4.5.0 to 4.12.2 for Python 3.12 compatibility
- Added curl to Docker image for health checks
- Trivy security scan: 0 vulnerabilities

### Technical Details
- Python 3.12-alpine base image
- Flask 2.3.2
- Flask-RESTX 1.3.2
- Flask-SQLAlchemy 3.0.3
- SQLAlchemy 2.0.12

[Unreleased]: https://github.com/yourusername/yourrepo/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/yourusername/yourrepo/compare/v2.0.1...v2.1.0
[2.0.1]: https://github.com/yourusername/yourrepo/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/yourusername/yourrepo/compare/v1.0.4...v2.0.0
[1.0.4]: https://github.com/yourusername/yourrepo/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/yourusername/yourrepo/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/yourusername/yourrepo/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/yourusername/yourrepo/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/yourusername/yourrepo/releases/tag/v1.0.0
