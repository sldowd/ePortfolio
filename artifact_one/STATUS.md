# cms_rust_port: status and next steps

Last updated: 2026-10-16

## What this is
A Rust port of the CS-405 Project 2 C++ client management CLI. Goal for the CS-499 capstone: show which original vulnerabilities were fixed, which were reduced, and which remain, with honest documentation.

## Done
- Admin password stored as an Argon2 PHC hash, not plaintext. Plaintext appears only in the README, never in source.
- Username lookup is enforced. Unknown usernames run a dummy Argon2 verify so response timing does not reveal which usernames exist.
- Password input is masked (rpassword).
- Create-user asks for the password twice and rejects a mismatch.
- Role-based access: admins see 5 menu options, viewers see 3 (display, logout, exit). Write and create actions are admin-only.
- `display_customers` takes `&User`.
- Logout returns to the login screen.
- Login allows 3 failed attempts per launch, then exits.
- EOF (Ctrl-D or closed stdin) exits cleanly at every prompt. No panics, no spin.
- Seed data moved into `seed_users()` and `seed_customers(&User)`.
- `menu_action` enum dispatch (`MenuAction`).

## Open decisions
- **Test approach for the instructor.** Options:
  1. Unit tests in `src/main.rs` (`#[cfg(test)] mod tests`), run with `cargo test`. Covers pure functions only. Simplest.
  2. Move logic into `lib.rs` and add `tests/` integration tests. Cleaner, more work.
  3. Scripted run. Not practical: `rpassword` reads from the terminal, not stdin.
  Leaning toward option 1 for now.
- **README.** Needs: build and run commands, the admin test credentials, and the viewer test flow (admin logs in, creates a viewer, logs out, logs in as the viewer, confirms option 3 is missing). Not yet drafted.

## Cleanup
- Remove the redundant outer `loop` in `main`. Move `let mut failed_attempts = 0;` above the login loop and dedent.
- Optional: `const MAX_LOGIN_ATTEMPTS: u32 = 3;`

## Writeup
- Before/after table: draft exists in chat, not yet saved. Login row must say 3 attempts per launch, with reset on restart.
- Remaining `unwrap` calls should be listed and justified (bugs and invariants only, never user input).

## Known limitations (document, do not hide)
- Accounts exist only for the session. Nothing is saved to disk.
- No minimum password length.
- Login attempt limit resets on restart.
- Admin password hash is embedded in the binary.
- Some `unwrap`/`expect` calls remain for invariants.
- Viewer login is tested manually, not in automated tests.

## Next session, start here
1. Choose the test approach (see Open decisions).
2. Clean up `main`.
3. Write the tests and the README.
4. Update the writeup table, then save it to the project.
5. Start the CS-405 Project 2 gap analysis, using the tests as evidence.