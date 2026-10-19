# Project One — Reverse Engineering Process Walkthrough

## How I found the credential check

I started by linking the binary and running it once to see what I was actually dealing with — a login gate followed by a client management menu. From there I wanted to find where the credential check actually happened before diving into the full disassembly.

I ran `objdump -s -j .rodata` and `strings -a` on the linked binary first, hoping the password would just be sitting there in plain text. It wasn't obvious at a glance, so I moved to disassembling `main` directly. Right away I saw a call to `CheckUserPermissionAccess()`, so I disassembled that function next.

To confirm what kind of comparison was happening, I ran `nm` on the file and searched the symbol table for library calls related to string comparison. I found:

```
U _ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE7compareEPKc@@GLIBCXX_3.4.21
```

Demangling it with `c++filt` confirmed it was:

```
std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>::compare(char const*) const
```

So the binary was doing a `std::string::compare()` call somewhere — I just needed to find where.

Back in `CheckUserPermissionAccess()`, there was only one call to `.compare()`. I cross-referenced the string argument being loaded right before that call:

```
0x1008 <+158>: lea 0x545(%rip),%rsi  #0x1554
0x100f <+165>: mov %rax,%rdi
0x1012 <+168>: call 0xc50 <...basic_string::compare(char const*) const@plt>
```

I used GDB to dump the string at that address directly:

```
(gdb) x/s 0x1554
0x1554: "123"
```

That's the hardcoded password.

## Finding the username bypass

With no second `.compare()` call anywhere in the function, I went looking for where `username` was actually used. I found it loaded right before the first `cin` read, and checked its value with GDB the same way:

```
0x0fcb <+97>: lea 0x20130e(%rip),%rsi  #0x2022e0 <username>

(gdb) x/s 0x2022e0
0x2022e0 <username>: ""
```

It's declared but never initialized with anything — an empty global string. That told me `username` gets read from user input, but I couldn't find any comparison logic touching it anywhere in the function. The only thing gating access was the password check.

## Confirming the vulnerability empirically

Rather than just trust that read from the disassembly, I tested it directly by running the compiled binary multiple times with different inputs:

**Attempt 1** — empty-feeling input, correct password:
```
Enter your username:
username
Enter your password:
123
```
Result: access granted, reached the main menu.

**Attempt 2** — a completely different, arbitrary username, same password:
```
Enter your username:
sd
Enter your password:
123
```
Result: access granted again.

Since the login succeeded both times regardless of what I typed for the username, and only failed when the password was wrong, this confirms the username field is read but never validated. **Any username plus the correct password grants full access.**

## Security Flags for Project Two

Two vulnerabilities identified in this binary, to be addressed in the Project Two writeup:

1. **Username validation bypass** — `CheckUserPermissionAccess()` reads a value into the global `username` variable but never checks it against anything. Access is granted purely on the password comparison. This means the username field provides zero actual access control — it's cosmetic.

2. **Unvalidated numeric input causing denial of service** — the main menu loop reads user choice via `cin >> choice` with no check on whether the read succeeded. Entering a non-numeric character (e.g., a letter) causes the input stream to enter a permanent fail state. Every subsequent `cin >>` call on that stream then silently fails without blocking for input, causing the program to loop infinitely printing "You chose 0" with no way to recover except killing the process.

Both stem from the same root issue: user input is trusted without validating either its content (username) or its success/failure state (numeric reads).
