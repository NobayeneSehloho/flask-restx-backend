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

[Unreleased]: https://github.com/yourusername/yourrepo/compare/v1.0.3...HEAD
[1.0.3]: https://github.com/yourusername/yourrepo/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/yourusername/yourrepo/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/yourusername/yourrepo/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/yourusername/yourrepo/releases/tag/v1.0.0
