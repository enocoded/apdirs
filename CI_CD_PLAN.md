# CI/CD decisions

## Current scope

- Apdirs is currently complete for Ubuntu; keep the existing repository layout
  and Linux/Nautilus installation workflow.
- Use GitHub Actions for continuous integration on pushes and pull requests.
- CI currently targets Ubuntu and tests the core filesystem behavior, Python
  syntax, and Linux shell-script syntax. GTK dialog previews remain manual
  because they need a graphical desktop session.
- Do not add automated deployment or release publishing yet.

## Future work

- Decide how Apdirs should be distributed and released before implementing CD.
  Then automate release artifacts and publishing only for the chosen channel.
- When Windows 11 support is developed, add its implementation under the
  platform-specific structure and add Windows CI coverage for supported
  behavior. Keep cross-platform core tests separate from OS-specific
  installation and UI checks.
- Revisit Python packaging before offering Apdirs as a Python package; the
  current layout is organized around the Ubuntu application and installer.
