#include <iostream>
#include <string>

using namespace std;

// global variables
int answer;
int choice;
std::string username;
std::string userpassword;
int changechoice;
int newservice;

std::string name1 = "Bob Jones";
std::string name2 = "Sarah Davis";
std::string name3 = "Amy Friendly";
std::string name4 = "Johnny Smith";
std::string name5 = "Carol Spears";

int num1 = 1;   // Bob Jones - option 1 (Brokerage)
int num2 = 2;   // Sarah Davis - option 2 (Retirement)
int num3 = 1;   // Amy Friendly - option 1 (Brokerage)
int num4 = 1;   // Johnny Smith - option 1 (Brokerage)
int num5 = 2;   // Carol Spears - option 2 (Retirement)

// function declarations 
int CheckUserPermissionAccess();
void DisplayInfo();
void ChangeCustomerChoice();

int main() {
    cout << "This cpp file was reverse engineered by Sarah Dowd" << endl;
    
    cout << "Hello! Welcome to our Investment Company" << endl;
    
    answer = CheckUserPermissionAccess();

    while (answer != 1) {
        cout << "Invalid Password. Please try again" << endl;
        answer = CheckUserPermissionAccess();
    }

    while (true) {
        cout << "What would you like to do?" << endl;
        cout << "DISPLAY the client list (enter 1)" << endl;
        cout << "CHANGE a client's choice (enter 2)" << endl;
        cout << "Exit the program.. (enter 3)" << endl;
        cin >> choice;
        cout << "You chose " << choice << endl;

        if (choice == 1) {
            DisplayInfo();
        } else if (choice == 2) {
            ChangeCustomerChoice();
        }

        if (choice == 3) {
            break;
        }
    }

    return 0;
}


int CheckUserPermissionAccess() {
    string syspassword = "123";
    int result = 0;

    cout << "Enter your username:" << endl;
    cin >> username;
    cout << "Enter your password:" << endl;
    cin >> userpassword;

    if (userpassword.compare(syspassword) == 0) {
        result = 1;
    } else {
        result = 2;
    }

    return result;

}

void DisplayInfo() {
    cout << "  Client's Name    Service Selected (1 = Brokerage, 2 = Retirement)" << endl;
    cout << "1. " << name1 << " selected option " << num1 << endl;
    cout << "2. " << name2 << " selected option " << num2 << endl;
    cout << "3. " << name3 << " selected option " << num3 << endl;
    cout << "4. " << name4 << " selected option " << num4 << endl;
    cout << "5. " << name5 << " selected option " << num5 << endl;
}

void ChangeCustomerChoice() {
    cout << "Enter the number of the client that you wish to change" << endl;
    cin >> changechoice;
    cout << "Please enter the client's new service choice (1 = Brokerage, 2 = Retirement)" << endl;
    cin >> newservice;

    if (changechoice == 1) {
        num1 = newservice;
    } else if (changechoice == 2) {
        num2 = newservice;
    } else if (changechoice == 3) {
        num3 = newservice;
    } else if (changechoice == 4) {
        num4 = newservice;
    } else if (changechoice == 5) {
        num5 = newservice;
    }

}