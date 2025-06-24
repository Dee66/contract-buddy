# Dependency Management Strategy

## Overview

This project uses a layered, DRY requirements structure for robust, scalable, and maintainable dependency management across all environments.

## Structure

- **base.in**: All shared, production-grade dependencies and pins.
- **prod.in**: Production-only dependencies. References `base.in`.
- **staging.in**: Staging-only dependencies. References `prod.in`.
- **dev.in**: Development and testing dependencies. References `prod.in`.

## How to Update

1. **Add or update shared dependencies in `base.in`.**
2. **Add environment-specific dependencies in the respective `.in` file.**
3. **Run lockfile sync:**
   ```sh
   nox -s sync_deps
   ```
