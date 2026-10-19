# CMS: Rust Port

A Rust port of the CS-410 Project 2 client management command-line program. The port fixes several vulnerabilities from the original C++ version. See the writeup for the full before-and-after comparison.

## Requirements

- Rust and Cargo (install from https://rustup.rs)
- A terminal. Password input is read from the terminal, not from piped input.

## Running the program

From the project folder:

```
cargo run
```

## Running the tests

```
cargo test
```

This runs 18 unit tests covering menu mapping, input validation, authorization, account creation and password hashing, username lookup, and customer permissions. Each test prints `ok` or `FAILED`.

The tests do not cover the login prompts, account creation through the prompts, or the menu loop. Those read from the terminal and are covered by the manual test flow below.

## Test credentials

| Account | Password | Role |
|---|---|---|
| admin | `d9Q-7kR2&aZ!` | Admin |

The admin password is stored only as an Argon2 hash in the code. The plaintext password appears only in this README.

Accounts other than admin are created while the program runs. They exist only for that session and are lost when the program exits.

## Manual test flow

Use this to check the role-based access controls.

1. Run `cargo run`.
2. Log in as `admin` with the password above.
3. Confirm the menu shows all five options. Try **2** (change a customer's service) and confirm it works.
4. At the first menu, choose **3** (Create new user). Enter a username, such as `viewer1`, and a password twice. The new account is a viewer.
5. Choose **4** (Log out). You return to the login menu. Log in as `viewer1`.
6. Confirm the menu shows only three options: display customers, logout, and exit. The change-service and create-user options should not appear.
7. Choose **3** (exit) to end the program.

## Other behavior to check

- **Failed logins:** Enter a wrong password three times. The program prints a limit message and exits.
- **Closed input:** Press Ctrl-D at any prompt. The program exits cleanly instead of crashing.
- **Password confirmation:** When creating a user, enter mismatched passwords. The program rejects the account.

## Generating a new admin hash

If you want to change the admin password:

```
cargo run --example hash_password
```

Enter the new password when prompted. Paste the printed hash into the `ADMIN_PASSWORD_HASH` constant in `src/main.rs`, and update the password in this README.

## Known limitations

- Accounts exist only for the current session. Nothing is saved to disk.
- There is no minimum password length.
- The failed-login limit resets when the program restarts.
- The admin password hash is stored in the compiled program.
- Some `unwrap` and `expect` calls remain for internal errors. They are used only where a failure would mean a bug, not bad user input.