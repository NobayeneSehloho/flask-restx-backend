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

[Unreleased]: https://github.com/yourusername/yourrepo/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/yourusername/yourrepo/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/yourusername/yourrepo/releases/tag/v1.0.0
