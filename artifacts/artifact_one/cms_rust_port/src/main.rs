use std::{io::{self, Write}};
use argon2::{ // used for password salting / hashing
    password_hash::{phc::PasswordHash, PasswordHasher, PasswordVerifier},
    Argon2
};
use rpassword::{ConfigBuilder}; // crate used to obscure password text as it is typed on screen

// stored admin password hash replaced plaintext password stored to seed admin user
const ADMIN_PASSWORD_HASH: &str = "$argon2id$v=19$m=19456,t=2,p=1$itK811UwzB+LdqgWycF7ow$hmPhGE7adatm/OczsQpgqv24jyOoTDZvVJHkE6wEx6s";
const MAX_LOGIN_ATTEMPTS: u32 = 3;

// RBAC - User ==============================
#[derive(Clone)]
enum Role { Admin, Viewer }
#[derive(Clone)]
struct User {
    username: String,
    password_hash: String,
    role: Role
}
impl User {
    fn new(username: String, password: String, role: Option<Role>) -> User {
        // use argon2 to hash password before storing
        let password_hash = Argon2::default()
            .hash_password(password.as_bytes())
            .expect("password hash failed")
            .to_string();
        let role = role.unwrap_or(Role::Viewer);
        User { username, password_hash, role }
    }
    fn from_hash(username: String, password_hash: String, role: Role) -> User {
        User { username, password_hash, role }
    }
    // create user function using rpassword rust crate to obscure text in terminal
    fn create_user(users: &UserList) -> Result<User, String> {
        let username = prompt("Enter username: ");
        if username.is_empty() {
            return Err("Username cannot be empty.".to_string());
        }
        if users.find_by_username(&username).is_some() {
            return Err("That username is already taken.".to_string());
        }
        let config = ConfigBuilder::new()
         .password_feedback_mask('*')
         .build();
        let password = match rpassword::prompt_password_with_config("Your password: ", config) {
            Ok(pw) => pw,
            // handle unexpected EOF
            Err(_) => {
                println!("\nInput closed. Exiting.");
                std::process::exit(0);
            }
        };
        if password.is_empty() {
            return Err("Password cannot be empty.".to_string());
        }
        let retype_config = ConfigBuilder::new()
         .password_feedback_mask('*')
         .build();
        let password_retype = match rpassword::prompt_password_with_config("Retype password: ", retype_config) {
            Ok(pw) => pw,
            // handle unexpected EOF
            Err(_) => {
                println!("\nInput closed. Exiting.");
                std::process::exit(0);
            }
        };
        if password != password_retype {
            return Err("Passwords do not match".to_string())
        }
        // Users created by admin default to Viewer role
        Ok(User::new(username, password, None))
    }
}

// UserList ==============================
struct UserList { users: Vec<User> }
impl UserList {
    fn new() -> UserList { UserList { users: Vec::new() } }
    fn add_user(&mut self, u: User) { self.users.push(u); }

    fn find_by_username(&self, username: &str) -> Option<&User> {
        self.users.iter().find(|u| u.username == username)
    }
}

// Customer ==============================
enum ServiceType { Brokerage, Retirement }
impl ServiceType {
    fn from_int(value: u32) -> Result<ServiceType, String> {
        match value {
            1 => Ok(ServiceType::Brokerage),
            2 => Ok(ServiceType::Retirement),
            _ => Err("Invalid service entered. Valid service = 1 or 2.".to_string()),
        }
    }
}
// Lets ServiceType print as "Brokerage" or "Retirement" with {}
impl std::fmt::Display for ServiceType {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        let label = match self {
            ServiceType::Brokerage => "Brokerage",
            ServiceType::Retirement => "Retirement",
        };
        write!(f, "{}", label)
    }
}
struct Customer {
    id: u32,
    name: String,
    service: ServiceType
}

impl Customer {
    // Constructor
    fn new(id: u32, name: String, service: ServiceType) -> Customer {
        Customer { id, name, service }
    }
    // getters
    pub fn get_id(&self) -> u32 { self.id }
    pub fn get_name(&self) -> &str { &self.name }
    pub fn get_service(&self) -> &ServiceType { &self.service }

    //setter
    pub fn update_service(&mut self, service: ServiceType) {
        self.service = service;
    }
}

 // Customer List ==============================
struct CustomerList { customers: Vec<Customer> }
impl CustomerList {
    fn new() -> CustomerList {
        CustomerList { customers: Vec::new() }
    }
    
    pub fn add_customer(&mut self, c: Customer, user: &User) -> Result<(), String> {
        check_user_authorization(user)?;
        self.customers.push(c);
        Ok(())
    }    
    
    pub fn display_customers(&self, _user: &User) {
        for c in &self.customers {
            println!(
                "ID: {}\nName: {}\nService: {}\n", c.get_id(), c.get_name(), c.get_service())
        }
    }

    // change customer service 
    pub fn change_customer_service(&mut self, user: &User) -> Result<(), String> {
        check_user_authorization(user)?;
        let customer_id = validate_int_input("Enter customer id: ");
        let service = validate_int_input("Enter service id (1=Brokerage, 2=Retirement): ");
        let service_type = ServiceType::from_int(service)?;
        for c in &mut self.customers {
            if c.get_id() == customer_id {
                c.update_service(service_type);
                return Ok(());
            }
        }
        Err(format!("Client not found: for id: {customer_id}"))
    }
}

// Helpers & Auth Functions ==============================
// Helper function to prompt user
fn prompt(message: &str) -> String {
    print!("{message}");
    io::stdout().flush().unwrap();
    let mut input = String::new();
    // handle unexpected EOF
    let bytes_read =  match io::stdin().read_line(&mut input) {
        Ok(bytes) => bytes,
        // handle unexpected EOF
        Err(_) => {
            println!("\nInput closed. Exiting.");
            std::process::exit(0);
        }
    };
    if bytes_read == 0 {
        println!("\nInput closed. Exiting.");
        std::process::exit(0);
    }

    input.trim().to_string()
}
// Helper function to validate integer user input 
fn validate_int_input(message: &str) -> u32 {
    loop {
        let input = prompt(message);
        match input.parse::<u32>() {
            Ok(input_int) => return input_int,
            Err(_) => println!("!! Invalid input: Input must be a number !!") 
        }
    }
}

// Menu choice handler
enum MenuAction { Display, Change, Create, Logout, Exit, Invalid }
fn menu_action(is_admin: bool, choice: u32) -> MenuAction {
    match (is_admin, choice) {
        (_, 1) => MenuAction::Display,
        (true, 2) => MenuAction::Change,
        (true, 3) => MenuAction::Create,
        (true, 4) | (false, 2) => MenuAction::Logout,
        (true, 5) | (false, 3) => MenuAction::Exit,
        _ => MenuAction::Invalid,
    }
}

// Authenticate user
fn authenticate_user(users: &UserList) -> Result<User, String> {
    // rpassword config setup to mask password while typed in command line
    let config = ConfigBuilder::new()
         .password_feedback_mask('*')
         .build();
    // prompt for username and password
    let username = prompt("Enter username: ");
    let password = match rpassword::prompt_password_with_config("Enter password: ", config) {
        Ok(pw) => pw,
        // handle unexpected EOF
        Err(_) => {
            println!("\nInput closed. Exiting.");
            std::process::exit(0);
        }
    };
    // look up user by username
    let user = match users.find_by_username(&username) {
        // if username: return user
        Some(user) => user,
        // else run dummy hash check to prevent timing side-channel
        None => {
            let parsed_hash = PasswordHash::new(ADMIN_PASSWORD_HASH)
                .map_err(|_| "Invalid username or password".to_string())?; // Error returns on failed hash, shows generic message, would be logged in a real system
            let _ = Argon2::default()
                .verify_password(password.as_bytes(), &parsed_hash);
            return Err("Invalid username or password".to_string())
        }
    };
    // if user: parse password hash and verify password
    let parsed_hash = PasswordHash::new(&user.password_hash)
        .map_err(|_| "Invalid username or password".to_string())?; // Error returns on failed hash, shows generic message, would be logged in a real system
    Argon2::default()
        .verify_password(password.as_bytes(), &parsed_hash)
        .map_err(|_| "Invalid username or password".to_string())?;
    Ok(user.clone()) // refactored to cloned vs borrowed user 
}

// Check User Permissions
fn check_user_authorization(user: &User) -> Result<(), String> {
    match user.role {
        Role::Admin => Ok(()),
        Role::Viewer => Err("Permission Denied: admin permission needed".to_string())
    }
}

// Seed user and customer data 
fn seed_users() -> UserList {
    let mut users = UserList::new();
    users.add_user(User::from_hash(String::from("admin"), String::from(ADMIN_PASSWORD_HASH), Role::Admin));
    users
}
fn seed_customers(admin: &User) -> CustomerList {
    let mut customers = CustomerList::new();
    customers.add_customer(Customer::new(1, String::from("Bob Jones"), ServiceType::Brokerage), admin).unwrap();
    customers.add_customer(Customer::new(2, String::from("Sarah Davis"), ServiceType::Retirement), admin).unwrap();
    customers.add_customer(Customer::new(3, String::from("Amy Friendly"), ServiceType::Brokerage), admin).unwrap();
    customers.add_customer(Customer::new(4, String::from("Johnny Smith"), ServiceType::Brokerage), admin).unwrap();
    customers.add_customer(Customer::new(5, String::from("Carol Spears"), ServiceType::Retirement), admin).unwrap();
    customers
}

fn main() {
    // seed user list
    let mut users = seed_users();
    // seed customer list
    let mut clients = seed_customers(users.find_by_username("admin").expect("admin should exist"));

    println!("Welcome to the CSM: Rust Port");
    
    // Authenticate user & assign current user
    let mut failed_attempts = 0;
    loop {
        println!("Enter username and password to login--");
        let current_user = match authenticate_user(&users) {
            Ok(user) => {
                failed_attempts = 0;
                user
            }
            Err(msg) => {
                println!("{msg}");
                failed_attempts += 1;
                if failed_attempts == MAX_LOGIN_ATTEMPTS {
                    println!("Maximum failed attempt limit reached");
                    return;
                }
                continue;
            }
        };
    
        let is_admin = matches!(current_user.role, Role::Admin);
    
        // Command line interface menu
        // refactored to conditionally display additional options for admin role
        loop {
            if is_admin {
                println!("1. DISPLAY the client list");
                println!("2. CHANGE a client's service");
                println!("3. CREATE a new user");
                println!("4. Log out user");
                println!("5. Exit the program");
            } else {
                println!("1. DISPLAY the client list");
                println!("2. Log out user");
                println!("3. Exit the program");
            }

            let menu_choice = validate_int_input("Enter menu choice: ");
            println!("You chose: {menu_choice}");

            match menu_action(is_admin, menu_choice) {
                MenuAction::Display => clients.display_customers(&current_user),
                MenuAction::Change => {
                    if let Err(msg) = clients.change_customer_service(&current_user) {
                        println!("{msg}")
                    }
                }
                MenuAction::Create => {
                    match User::create_user(&users) {
                        Ok(new_user) => {
                            users.add_user(new_user);
                            println!("New user successfully created")
                        },
                        Err(msg) => println!("{msg}")
                    }
                }
                MenuAction::Logout => break,
                MenuAction::Exit => { println!("Goodbye!"); return; }
                MenuAction::Invalid => println!("Invalid menu choice"),
            };
        }
    }
}

#[cfg(test)]
mod tests {
    // Run with: cargo test
    use super::*;
    
    // Menu mapping (menu_action)
    #[test]
    fn admin_menu_maps_correctly() {
        assert!(matches!(menu_action(true, 1), MenuAction::Display));
        assert!(matches!(menu_action(true, 2), MenuAction::Change));
        assert!(matches!(menu_action(true, 3), MenuAction::Create));
        assert!(matches!(menu_action(true, 4), MenuAction::Logout));
        assert!(matches!(menu_action(true, 5), MenuAction::Exit));
    }

    #[test]
    fn invalid_admin_menu_choices_rejected() {
        assert!(matches!(menu_action(true, 0), MenuAction::Invalid));
        assert!(matches!(menu_action(true, 6), MenuAction::Invalid));
    }
    
    #[test]
    fn viewer_menu_maps_correctly() {
        assert!(matches!(menu_action(false, 1), MenuAction::Display));
        assert!(matches!(menu_action(false, 2), MenuAction::Logout));
        assert!(matches!(menu_action(false, 3), MenuAction::Exit));
    }
    
    #[test]
    fn invalid_viewer_menu_choices_rejected() {
        assert!(matches!(menu_action(false, 4), MenuAction::Invalid));
        assert!(matches!(menu_action(false, 5), MenuAction::Invalid));
    }

    // Input validation (ServiceType::from_int)
    #[test]
    fn validate_servicetype_from_input() {
        assert!(matches!(ServiceType::from_int(1), Ok(ServiceType::Brokerage)));
        assert!(matches!(ServiceType::from_int(2), Ok(ServiceType::Retirement)));
        assert!(matches!(ServiceType::from_int(0), Err(_)));
        assert!(matches!(ServiceType::from_int(3), Err(_)));
    }

    // Authorization (check_user_authorization)
    #[test]
    fn admin_passes_auth_check() {
        let admin = User::from_hash("admin".into(), "unused".into(), Role::Admin);
        assert!(matches!(check_user_authorization(&admin), Ok(())));
    }
    #[test]
    fn viewer_fails_authorization_check() {
        let viewer = User::from_hash("viewer".into(), "unused".into(), Role::Viewer);
        assert!(check_user_authorization(&viewer).is_err());
    }

    // Account creation and hashing (User::new, User::from_hash)
    #[test]
    fn new_user_defaults_to_viewer_role() {
        let user = User::new("username".into(), "unused".into(), None);
        assert!(matches!(user.role, Role::Viewer));
    }

    #[test]
    fn stored_hash_is_not_plaintext_and_is_argon2() {
        let user = User::new("alice".into(), "secret-pass".into(), None);
        assert_ne!(user.password_hash, "secret-pass");
        assert!(user.password_hash.starts_with("$argon2"));
    }

    #[test]
    fn hash_verifies_correct_password_only() {
        let user = User::new("alice".into(), "secret-pass".into(), None);
        let parsed = PasswordHash::new(&user.password_hash).unwrap();
        assert!(Argon2::default().verify_password(b"secret-pass", &parsed).is_ok());
        assert!(Argon2::default().verify_password(b"wrong-pass", &parsed).is_err());
    }

    #[test]
    fn from_hash_stores_values_as_given() {
        let user = User::from_hash("bob".into(), "stored-hash".into(), Role::Admin);
        assert_eq!(user.username, "bob");
        assert_eq!(user.password_hash, "stored-hash");
        assert!(matches!(user.role, Role::Admin));
    }

    // Lookup (UserList::find_by_username)
    #[test]
    fn existing_username_is_found() {
        let mut users = UserList::new();
        users.add_user(User::from_hash("viewer".into(), "unused".into(), Role::Viewer));
        users.add_user(User::from_hash("admin".into(), "unused".into(), Role::Admin));
        assert!(users.find_by_username("viewer").is_some());
        assert!(users.find_by_username("admin").is_some());
    }

    #[test]
    fn unknown_username_returns_none() {
        let users = UserList::new();
        assert!(users.find_by_username("test").is_none());
    }
    
    #[test]
    fn matching_is_case_sensitive() {
        let mut users = UserList::new();
        users.add_user(User::from_hash("admin".into(), "unused".into(), Role::Admin));
        assert!(users.find_by_username("Admin").is_none());
    }

    // Customer records
    // Helper: a fresh list with one customer, added by an admin.
    fn sample_list() -> CustomerList {
        let admin = User::from_hash("admin".into(), "unused".into(), Role::Admin);
        let mut list = CustomerList::new();
        list.add_customer(
            Customer::new(1, "Bob Jones".into(), ServiceType::Brokerage),
            &admin,
        ).unwrap();
        list
    }

    #[test]
    fn viewer_cannot_add_customer() {
        let mut list = sample_list();
        let viewer = User::from_hash("viewer".into(), "unused".into(), Role::Viewer);
        let before = list.customers.len();
        let result = list.add_customer(
            Customer::new(2, "Sarah Davis".into(), ServiceType::Retirement),
            &viewer,
        );
        assert!(result.is_err());
        assert_eq!(list.customers.len(), before);
    }

    #[test]
    fn admin_can_add_customer() {
        let mut list = sample_list();
        let admin = User::from_hash("admin".into(), "unused".into(), Role::Admin);
        let before = list.customers.len();
        let result = list.add_customer(
            Customer::new(2, "Sarah Davis".into(), ServiceType::Retirement),
            &admin,
        );
        assert!(result.is_ok());
        assert_eq!(list.customers.len(), before + 1);
    }

    #[test]
    fn update_service_changes_service() {
        let mut list = sample_list();
        list.customers[0].update_service(ServiceType::Retirement);
        assert!(matches!(list.customers[0].get_service(), ServiceType::Retirement));
    }

    #[test]
    fn viewer_cannot_change_customer_service() {
        let mut list = sample_list();
        let viewer = User::from_hash("viewer".into(), "unused".into(), Role::Viewer);
        assert!(list.change_customer_service(&viewer).is_err());
    }

    // Not testable with cargo test: prompt, validate_int_input, authenticate_user, create_user, and the menu loop. They read from the terminal, so they stay in the manual test flow in the README.
}