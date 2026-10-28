# Static analysis issues

| Issue | Type | Line(s) before fix | Description | Fix Approach |
|-------|------|--------------------|-------------|--------------|
| Shell command injection risk (`B602`) | Security - High | 53-55 | `pingHub` joined a hub address into a command string and ran it with `shell=True`, allowing shell metacharacters to be interpreted. | Remove the unused command execution helper and its subprocess import, eliminating the shell execution surface. |
| Insecure temporary file (`B306`) | Security - Medium | 48-50 | `tempfile.mktemp` generated a name without creating the file, leaving a race where another process could claim it first. | Create the file atomically with `NamedTemporaryFile(delete=False)` and return its allocated path. |
| Mutable default argument (`W0102`) | Bug / maintainability - Medium | 11 | The shared `history=[]` default could retain IDs across calls when callers omit the argument. | Default to `None` and append only to an explicitly supplied history list. |
| Broad exception handler (`W0718`) | Reliability - Medium | 34-38 | Catching every `Exception` could hide unrelated programming and runtime failures. | Use `dict.get` and handle the missing tracking ID case explicitly. |
| Non-cryptographic OTP (`B311`) | Security - Low | 72 | `random.randint` is predictable and unsuitable for a delivery authentication code. | Generate the four-digit OTP with `secrets.randbelow`. |
| Naming, documentation, and formatting (`C0103`, `C0114`, `C0116`, Flake8) | Style / maintainability - Low | Throughout | CamelCase names, missing documentation, and whitespace errors reduced readability and failed the configured linters. | Use snake_case, add documentation, and format consistently. |
