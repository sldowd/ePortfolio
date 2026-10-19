using namespace std;

#include <iostream>
#include <vector>
#include <limits>

// funcion declarations
int ValidateIntegerInput();
int CheckUserPermissionAccess();

// Customer class - customers now represented by a Customer object that includes name and service choice plus new id field
// 
class Customer {
    private:
    // private customer fields 
        int id; // additional id field added
        string name;
        int service;
    
    public:
    // public constructor and methods for use by main function 
        // Constructor
        Customer(int id, string name, int service) {
            this->id = id;
            this->name = name;
            this->service = service;
        }

        // getters
        int getId() const { return id; }
        string getName() const { return name; }
        int getService() const { return service; }

        // setters
        // updateService() method validates service value before assigning
        void updateService(int service) {
            if (service == 1 || service == 2) {
                this->service = service;
            } else {
                cout << "Invalid service entered. Valid service = 1 or 2." << endl;
            }
        }

        // additional updateName() method would be useful to add here
};
// CustomerList class
class CustomerList {
    private:
        vector<Customer> customers;

    public:
        void addCustomer(Customer c) {
            customers.push_back(c);
        }

        // VULNERABILITY: no authorization check - any authenticated user has full read access
        void displayCustomers() {
            for(int i=0; i < customers.size(); i++) {
                cout << "ID: " << customers[i].getId() << ", Name: " << customers[i].getName()
                << ", Service: " << customers[i].getService() << endl;
            }
        }
        // VULNERABILITY: no authorization check - any authenticated user has full write access
        void changeCustomerService() {
            int id, newService;
            
            cout << "Enter id of client you wish to update:\n";
            // helper function reads input, checks for failstate
            id = ValidateIntegerInput();
            cout << "Enter the client's new service choice (1 = Brokerage, 2 = Retirement)\n";
            // helper function reads input, checks for failstate
            newService = ValidateIntegerInput();

            bool found = false;
            // customer id is validated before calling updateService method
            for (Customer& c : customers) {
                if (c.getId() == id) {
                    c.updateService(newService);
                    found = true;
                    break;
                }
            }
            if (!found) {
                cout << "Client not found" << endl;
            }
        }
};


// main
int main() {
    int choice = 0;
    int answer = 0;
    int authAttemptCounter = 0;

    cout << "This program was reverse engineered and evaluated for security vulnerabilities by Sarah Dowd" << endl;
    // instantiate CustomerList class to store clients
    CustomerList clientList;
    // add previously globally initialized customers & service numbers as instances of Customer class
    // & add each customer to clientList
    clientList.addCustomer(Customer(1, "Bob Jones", 1));
    clientList.addCustomer(Customer(2, "Sarah Davis", 2));
    clientList.addCustomer(Customer(3, "Amy Friendly", 1));
    clientList.addCustomer(Customer(4, "Johnny Smith", 1));
    clientList.addCustomer(Customer(5, "Carol Spears", 2));
    
    cout << "Hello! Welcome to our Investment Company" << endl;
    
    // implemented authAttemptCounter to add bounds check to failed password input -- maximum num attempts == 3
    do {
        answer = CheckUserPermissionAccess();
        // counter increments after each call to authentication function
        authAttemptCounter++;
        if (answer != 1) {
            cout << "Invalid Password" << endl;
        }
    } while (answer != 1 && authAttemptCounter < 3);
    
    if (answer !=1) {
        // after 3 failed attempts notify user and abort
        // still lacks lock out -- user can just run program again after abort
        cout << "!!: Maximum failed attempt limit reached" << endl;
        return 1;
    }

    while (true) {
        cout << "What would you like to do?\n";
        cout << "DISPLAY the client list (enter 1)\n";
        cout << "CHANGE a client's choice (enter 2)\n";
        cout << "Exit the program.. (enter 3)\n";
        // helper function reads input, checks for failstate
        choice = ValidateIntegerInput();
        cout << "You chose " << choice << endl;

        // general else statement added to notify user of invalid menu selection
        if (choice == 1) {
            clientList.displayCustomers();
        } else if (choice == 2) {
            clientList.changeCustomerService();
        } else if (choice == 3) {
            break;
        } else {
            cout << "Invalid menu selection." << endl;
        }
    }
    return 0;
}

// ValidateIntegerInput -- Helper function 
// Reads user input, handles failstate and validates data type to prevent silent failure or infinite loop
int ValidateIntegerInput() {
    int value = 0;
    cin >> value;
    while (cin.fail()) {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Invalid input. Enter a number:\n";
        cin >> value;
    }
    return value;
}
// CheckUserPermissionAccess() 
int CheckUserPermissionAccess() {
    string username = "";
    string userpassword = "";
    // VULNERABILITY: hardcoded plaintext credential, recoverable via strings/objdump on the compiled binary
    string syspassword = "123";
    int result = 0;

    cout << "Enter your username:" << endl;
    // VULNERABILITY: username is read but never validated against any stored value
    cin >> username;
    cout << "Enter your password:" << endl;
    // VULNERABILITY: no input masking - password is echoed as plaintext to the terminal
    cin >> userpassword;

    // VULNERABILITY: .compare() is not constant-time, creating a timing side-channel
    if (userpassword.compare(syspassword) == 0) {
        result = 1;
    } else {
        result = 2;
    }

    return result;

}