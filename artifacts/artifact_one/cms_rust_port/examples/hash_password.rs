//! Generates an Argon2 password hash for the ADMIN_PASSWORD_HASH constant in main.rs.
//!
//! Run with:  cargo run --example hash_password
//!
//! Prompts for a password (input is hidden) and prints the hash in PHC format.
//! Paste the printed string into ADMIN_PASSWORD_HASH.
//! The password is never stored or printed by this program.

use argon2::{ // used for password hashing
    password_hash::{PasswordHasher},
    Argon2
};
use rpassword::{ConfigBuilder};
fn main() {
    // rpassword configuration masks password output with '*' char
    let config = ConfigBuilder::new()
        .password_feedback_mask('*')
        .build();

    let password = rpassword::prompt_password_with_config("Your password: ", config).unwrap();

    let password_hash = Argon2::default()
        .hash_password(password.as_bytes())
        .expect("password hash failed")
        .to_string();
    println!("{password_hash}");
}

