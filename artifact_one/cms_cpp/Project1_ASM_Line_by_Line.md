# Project 1 — Line-by-Line Assembly Functionality

## Function: `main()`

| Address | Instruction | Functionality |
|---|---|---|
| 0x0e4a <+0> | `push %rbp` | Save caller's base pointer onto the stack (function prologue). |
| 0x0e4b <+1> | `mov %rsp,%rbp` | Set up new base pointer for this stack frame. |
| 0x0e4e <+4> | `lea 0x5eb(%rip),%rsi` | Load address of a string literal (intro/welcome text) into `%rsi`. |
| 0x0e55 <+11> | `lea 0x201244(%rip),%rdi` | Load address of `std::cout` into `%rdi`. |
| 0x0e5c <+18> | `call std::operator<<(ostream&, char const*)@plt` | Print the string literal to `std::cout`. |
| 0x0e61 <+23> | `call CheckUserPermissionAccess()` | Call the login/authentication function. |
| 0x0e66 <+28> | `mov %eax,0x201494(%rip) # <answer>` | Store the return value (1 = pass, 2 = fail) into global `answer`. |
| 0x0e6c <+34> | `mov 0x20148e(%rip),%eax # <answer>` | Load `answer` back into `%eax`. |
| 0x0e72 <+40> | `cmp $0x1,%eax` | Compare `answer` to 1 (success). |
| 0x0e75 <+43> | `je 0xe8a <main+64>` | If `answer == 1`, jump ahead — skip the "access denied" message. |
| 0x0e77 <+45> | `lea 0x5f2(%rip),%rsi` | Load address of "access denied" style string. |
| 0x0e7e <+52> | `lea 0x20121b(%rip),%rdi` | Load address of `std::cout`. |
| 0x0e85 <+59> | `call std::operator<<@plt` | Print the denial message. |
| 0x0e8a <+64> | `mov 0x201470(%rip),%eax # <answer>` | Reload `answer` (landing point of the je above). |
| 0x0e90 <+70> | `cmp $0x1,%eax` | Check again whether `answer == 1`. |
| 0x0e93 <+73> | `je 0xe97 <main+77>` | If access was granted, fall through into the menu section. |
| 0x0e95 <+75> | `jmp 0xe61 <main+23>` | Otherwise, loop back and call `CheckUserPermissionAccess()` again — this is the retry-login loop. |
| 0x0e97 <+77> | `lea 0x5f6(%rip),%rsi` | Load address of menu string (option 1 text). |
| 0x0e9e <+84> | `lea 0x2011fb(%rip),%rdi` | Load `std::cout`. |
| 0x0ea5 <+91> | `call std::operator<<@plt` | Print menu line 1. |
| 0x0eaa <+96> | `lea 0x5ff(%rip),%rsi` | Load address of menu string (option 2 text). |
| 0x0eb1 <+103> | `lea 0x2011e8(%rip),%rdi` | Load `std::cout`. |
| 0x0eb8 <+110> | `call std::operator<<@plt` | Print menu line 2. |
| 0x0ebd <+115> | `lea 0x614(%rip),%rsi` | Load address of menu string (option 3 text). |
| 0x0ec4 <+122> | `lea 0x2011d5(%rip),%rdi` | Load `std::cout`. |
| 0x0ecb <+129> | `call std::operator<<@plt` | Print menu line 3. |
| 0x0ed0 <+134> | `lea 0x625(%rip),%rsi` | Load address of prompt string ("Enter choice:"). |
| 0x0ed7 <+141> | `lea 0x2011c2(%rip),%rdi` | Load `std::cout`. |
| 0x0ede <+148> | `call std::operator<<@plt` | Print the prompt. |
| 0x0ee3 <+153> | `lea 0x20140a(%rip),%rsi # <choice>` | Load address of global `choice` variable. |
| 0x0eea <+160> | `lea 0x2012cf(%rip),%rdi` | Load `std::cin`. |
| 0x0ef1 <+167> | `call std::istream::operator>>(int&)@plt` | Read user's integer input into `choice`. |
| 0x0ef6 <+172> | `lea 0x61d(%rip),%rsi` | Load address of echo string ("You selected:" or similar). |
| 0x0efd <+179> | `lea 0x20119c(%rip),%rdi` | Load `std::cout`. |
| 0x0f04 <+186> | `call std::operator<<@plt` | Print the echo string. |
| 0x0f09 <+191> | `mov %rax,%rdx` | Save the `cout` stream reference returned from the previous call. |
| 0x0f0c <+194> | `mov 0x2013e2(%rip),%eax # <choice>` | Load `choice` value. |
| 0x0f12 <+200> | `mov %eax,%esi` | Move `choice` into `%esi` as the argument to print. |
| 0x0f14 <+202> | `mov %rdx,%rdi` | Move the stream reference into `%rdi`. |
| 0x0f17 <+205> | `call std::ostream::operator<<(int)@plt` | Print the numeric value of `choice`. |
| 0x0f1c <+210> | `mov %rax,%rdx` | Save stream reference again. |
| 0x0f1f <+213> | `mov 0x2010aa(%rip),%rax` | Load `std::endl` manipulator address. |
| 0x0f26 <+220> | `mov %rax,%rsi` | Set `std::endl` as argument. |
| 0x0f29 <+223> | `mov %rdx,%rdi` | Set stream as target. |
| 0x0f2c <+226> | `call std::ostream::operator<<(manipulator)@plt` | Print newline via `std::endl`. |
| 0x0f31 <+231> | `mov 0x2013bd(%rip),%eax # <choice>` | Reload `choice`. |
| 0x0f37 <+237> | `cmp $0x1,%eax` | Compare `choice` to 1. |
| 0x0f3a <+240> | `jne 0xf43 <main+249>` | If not 1, skip the DisplayInfo call. |
| 0x0f3c <+242> | `call DisplayInfo()` | If `choice == 1`, call `DisplayInfo()`. |
| 0x0f41 <+247> | `jmp 0xf53 <main+265>` | Skip past the other branch checks. |
| 0x0f43 <+249> | `mov 0x2013ab(%rip),%eax # <choice>` | Reload `choice` (landing point if choice != 1). |
| 0x0f49 <+255> | `cmp $0x2,%eax` | Compare `choice` to 2. |
| 0x0f4c <+258> | `jne 0xf53 <main+265>` | If not 2, skip ChangeCustomerChoice call. |
| 0x0f4e <+260> | `call ChangeCustomerChoice()` | If `choice == 2`, call `ChangeCustomerChoice()`. |
| 0x0f53 <+265> | `mov 0x20139b(%rip),%eax # <choice>` | Reload `choice` (landing point regardless of branch taken). |
| 0x0f59 <+271> | `cmp $0x3,%eax` | Compare `choice` to 3 (exit option). |
| 0x0f5c <+274> | `je 0xf63 <main+281>` | If `choice == 3`, jump to the return sequence. |
| 0x0f5e <+276> | `jmp 0xe97 <main+77>` | Otherwise, loop back to redisplay the menu — this is the main menu loop. |
| 0x0f63 <+281> | `mov $0x0,%eax` | Set return value to 0 (success). |
| 0x0f68 <+286> | `pop %rbp` | Restore caller's base pointer (function epilogue). |
| 0x0f69 <+287> | `ret` | Return from `main`. |

---

## Function: `CheckUserPermissionAccess()`

| Address | Instruction | Functionality |
|---|---|---|
| 0x0f6a <+0> | `push %rbp` | Save caller's base pointer. |
| 0x0f6b <+1> | `mov %rsp,%rbp` | Set up new base pointer. |
| 0x0f6e <+4> | `push %rbx` | Save `%rbx` — this function uses it as a callee-saved return-value holder. |
| 0x0f6f <+5> | `sub $0x48,%rsp` | Allocate 0x48 bytes of local stack space (for local `std::string` objects, etc.). |
| 0x0f73 <+9> | `mov %fs:0x28,%rax` | Load the stack canary value from thread-local storage. |
| 0x0f7c <+18> | `mov %rax,-0x18(%rbp)` | Store the canary on the stack — used later to detect buffer overflows. |
| 0x0f80 <+22> | `xor %eax,%eax` | Zero out `%eax` (idiom for clearing a register cheaply). |
| 0x0f82 <+24> | `lea -0x45(%rbp),%rax` | Load address of a local `std::allocator<char>` object. |
| 0x0f86 <+28> | `mov %rax,%rdi` | Set it as the `this` pointer argument. |
| 0x0f89 <+31> | `call std::allocator<char>::allocator()@plt` | Construct the allocator object (needed to build the password string). |
| 0x0f8e <+36> | `lea -0x45(%rbp),%rdx` | Load address of that allocator again, as an argument. |
| 0x0f92 <+40> | `lea -0x40(%rbp),%rax` | Load address of a local `std::string` object being constructed. |
| 0x0f96 <+44> | `lea 0x588(%rip),%rsi` | Load address of the hardcoded password string literal. |
| 0x0f9d <+51> | `mov %rax,%rdi` | Set the string object as `this`. |
| 0x0fa0 <+54> | `call std::string::basic_string(char const*, allocator const&)@plt` | Construct a `std::string` from the hardcoded password literal — this is the correct/expected password being stored locally. |
| 0x0fa5 <+59> | `lea -0x45(%rbp),%rax` | Load address of the temporary allocator. |
| 0x0fa9 <+63> | `mov %rax,%rdi` | Set as `this`. |
| 0x0fac <+66> | `call std::allocator<char>::~allocator()@plt` | Destroy the temporary allocator (no longer needed after string construction). |
| 0x0fb1 <+71> | `movl $0x0,-0x44(%rbp)` | Initialize a local int (likely the eventual return/result variable) to 0. |
| 0x0fb8 <+78> | `lea 0x567(%rip),%rsi` | Load address of "Enter username:" prompt string. |
| 0x0fbf <+85> | `lea 0x2010da(%rip),%rdi` | Load `std::cout`. |
| 0x0fc6 <+92> | `call std::operator<<@plt` | Print the username prompt. |
| 0x0fcb <+97> | `lea 0x20130e(%rip),%rsi # <username>` | Load address of the global `username` buffer. |
| 0x0fd2 <+104> | `lea 0x2011e7(%rip),%rdi` | Load `std::cin`. |
| 0x0fd9 <+111> | `call std::istream::operator>>(char*)@plt` | Read the username input into the global `username` buffer. **Note: this value is read but never validated anywhere in this function — this is the vulnerability you already flagged.** |
| 0x0fde <+116> | `lea 0x558(%rip),%rsi` | Load address of "Enter password:" prompt string. |
| 0x0fe5 <+123> | `lea 0x2010b4(%rip),%rdi` | Load `std::cout`. |
| 0x0fec <+130> | `call std::operator<<@plt` | Print the password prompt. |
| 0x0ff1 <+135> | `lea -0x40(%rbp),%rax` | Load address of a *second* local `std::string` (the one the user will type into). |
| 0x0ff5 <+139> | `mov %rax,%rsi` | Set as the destination argument. |

> Note: at `0x0ff1`/`0x0ff5` the disassembly reuses the same local string slot at `-0x40(%rbp)` that held the hardcoded password. In GDB output like this, that's expected — watch this closely when you convert to C++, since it means the input is being read into a *different* local `std::string` object than the one holding the hardcoded value (they're constructed/destroyed at different points in the function's flow), and the `.compare()` call below is what actually does the real comparison between them.

| Address | Instruction | Functionality |
|---|---|---|
| 0x0ff8 <+142> | `lea 0x2011c1(%rip),%rdi` | Load `std::cin`. |
| 0x0fff <+149> | `call std::istream::operator>>(string&)@plt` | Read the user's typed password into the local `std::string`. |
| 0x1004 <+154> | `lea -0x40(%rbp),%rax` | Load address of the string just read from input. |
| 0x1008 <+158> | `lea 0x545(%rip),%rsi` | Load address of the hardcoded comparison password literal. |
| 0x100f <+165> | `mov %rax,%rdi` | Set `this` for the compare call. |
| 0x1012 <+168> | `call std::string::compare(char const*) const@plt` | Compare the user-entered password string against the hardcoded literal. Returns 0 if equal. |
| 0x1017 <+173> | `mov %eax,-0x44(%rbp)` | Store the comparison result into the local result variable. |
| 0x101a <+176> | `cmpl $0x0,-0x44(%rbp)` | Check whether the compare result is 0 (i.e., strings matched). |
| 0x101e <+180> | `jne 0x1027 <CheckUserPermissionAccess()+189>` | If not equal (wrong password), jump to the "fail" branch. |
| 0x1020 <+182> | `mov $0x1,%ebx` | Passwords matched — set return value to 1 (access granted). |
| 0x1025 <+187> | `jmp 0x102c <CheckUserPermissionAccess()+194>` | Skip the fail branch. |
| 0x1027 <+189> | `mov $0x2,%ebx` | Passwords did not match — set return value to 2 (access denied). |
| 0x102c <+194> | `lea -0x40(%rbp),%rax` | Load address of the local password string. |
| 0x1030 <+198> | `mov %rax,%rdi` | Set as `this`. |
| 0x1033 <+201> | `call std::string::~basic_string()@plt` | Destroy the local password string (cleanup / RAII). |
| 0x1038 <+206> | `mov %ebx,%eax` | Move the result (1 or 2) into `%eax` as the return value. |
| 0x103a <+208> | `mov -0x18(%rbp),%rcx` | Reload the stack canary that was saved at function entry. |
| 0x103e <+212> | `xor %fs:0x28,%rcx` | XOR it against the current canary value — if unchanged, result is 0. |
| 0x1047 <+221> | `je 0x1084 <CheckUserPermissionAccess()+282>` | If canary is intact (no stack corruption), jump to clean return. |
| 0x1049 <+223> | `jmp 0x107f <CheckUserPermissionAccess()+277>` | Otherwise, fall into the stack-check-fail path. |
| 0x104b <+225> | `mov %rax,%rbx` | *(Exception-handling landing pad — preserves the in-flight exception object.)* |
| 0x104e <+228> | `lea -0x45(%rbp),%rax` | Load address of the allocator (exception cleanup path). |
| 0x1052 <+232> | `mov %rax,%rdi` | Set as `this`. |
| 0x1055 <+235> | `call std::allocator<char>::~allocator()@plt` | Destroy the allocator during exception unwinding. |
| 0x105a <+240> | `mov %rbx,%rax` | Restore exception object pointer. |
| 0x105d <+243> | `mov %rax,%rdi` | Pass it along. |
| 0x1060 <+246> | `call _Unwind_Resume@plt` | Continue C++ exception propagation. |
| 0x1065 <+251> | `mov %rax,%rbx` | *(Second exception landing pad, for a different unwind path.)* |
| 0x1068 <+254> | `lea -0x40(%rbp),%rax` | Load address of the password string. |
| 0x106c <+258> | `mov %rax,%rdi` | Set as `this`. |
| 0x106f <+261> | `call std::string::~basic_string()@plt` | Destroy the password string during unwinding. |
| 0x1074 <+266> | `mov %rbx,%rax` | Restore exception object pointer. |
| 0x1077 <+269> | `mov %rax,%rdi` | Pass it along. |
| 0x107a <+272> | `call _Unwind_Resume@plt` | Continue exception propagation. |
| 0x107f <+277> | `call __stack_chk_fail@plt` | Stack corruption detected — abort the program. |
| 0x1084 <+282> | `add $0x48,%rsp` | Deallocate local stack space (normal return path). |
| 0x1088 <+286> | `pop %rbx` | Restore `%rbx`. |
| 0x1089 <+287> | `pop %rbp` | Restore caller's base pointer. |
| 0x108a <+288> | `ret` | Return to `main` with 1 (granted) or 2 (denied) in `%eax`. |

---

## Function: `DisplayInfo()`

This function repeats the same five-instruction pattern for each of 5 customer records (`name1`/`num1` through `name5`/`num5`). The pattern is documented once below; the addresses for each repetition are listed in the table beneath it.

**Repeating pattern per record:**
1. `lea` a label string ("Name: ", "Service #: ", etc.) → `%rsi`
2. `lea` / `mov` `std::cout` (or the returned stream) → `%rdi`
3. `call std::operator<<@plt` — print the label
4. `lea` the record's `nameN` global → `%rsi`; `call std::operator<<@plt` — print the name
5. `mov` the record's `numN` global → `%esi`; `call std::ostream::operator<<(int)@plt` — print the number
6. `call std::ostream::operator<<(manipulator)@plt` with `std::endl` loaded — print a newline

| Address Range | Record | Functionality |
|---|---|---|
| 0x108b–0x10b2 | Header | Prints a title/header line (e.g., "Customer Info:") followed by `std::endl`. |
| 0x10b7–0x110b | name1/num1 | Prints label, `name1`, another label, `num1`, then newline. |
| 0x1110–0x1164 | name2/num2 | Prints label, `name2`, another label, `num2`, then newline. |
| 0x1169–0x11bd | name3/num3 | Prints label, `name3`, another label, `num3`, then newline. |
| 0x11c2–0x1216 | name4/num4 | Prints label, `name4`, another label, `num4`, then newline. |
| 0x121b–0x126f | name5/num5 | Prints label, `name5`, another label, `num5`, then newline. |
| 0x1274 <+489> | `nop` | Padding/alignment instruction, no effect. |
| 0x1275 <+490> | `pop %rbp` | Restore caller's base pointer. |
| 0x1276 <+491> | `ret` | Return to `main`. |

---

## Function: `ChangeCustomerChoice()`

| Address | Instruction | Functionality |
|---|---|---|
| 0x1277 <+0> | `push %rbp` | Save caller's base pointer. |
| 0x1278 <+1> | `mov %rsp,%rbp` | Set up new base pointer. |
| 0x127b <+4> | `lea 0x346(%rip),%rsi` | Load address of prompt string ("Which record to change?"). |
| 0x1282 <+11> | `lea 0x200e17(%rip),%rdi` | Load `std::cout`. |
| 0x1289 <+18> | `call std::operator<<@plt` | Print the prompt. |
| 0x128e <+23> | `lea 0x201063(%rip),%rsi # <changechoice>` | Load address of the global `changechoice` variable. |
| 0x1295 <+30> | `lea 0x200f24(%rip),%rdi` | Load `std::cin`. |
| 0x129c <+37> | `call std::istream::operator>>(int&)@plt` | Read the record number (1-5) into `changechoice`. |
| 0x12a1 <+42> | `lea 0x358(%rip),%rsi` | Load address of prompt string ("New service value:"). |
| 0x12a8 <+49> | `lea 0x200df1(%rip),%rdi` | Load `std::cout`. |
| 0x12af <+56> | `call std::operator<<@plt` | Print the prompt. |
| 0x12b4 <+61> | `lea 0x201041(%rip),%rsi # <newservice>` | Load address of the global `newservice` variable. |
| 0x12bb <+68> | `lea 0x200efe(%rip),%rdi` | Load `std::cin`. |
| 0x12c2 <+75> | `call std::istream::operator>>(int&)@plt` | Read the new value into `newservice`. |
| 0x12c7 <+80> | `mov 0x20102b(%rip),%eax # <changechoice>` | Load `changechoice`. |
| 0x12cd <+86> | `cmp $0x1,%eax` | Check if the user chose record 1. |
| 0x12d0 <+89> | `jne 0x12e0 <ChangeCustomerChoice()+105>` | If not, skip to the next check. |
| 0x12d2 <+91> | `mov 0x201024(%rip),%eax # <newservice>` | Load the new value. |
| 0x12d8 <+97> | `mov %eax,0x200d82(%rip) # <num1>` | Write it into `num1`. |
| 0x12de <+103> | `jmp 0x1342 <ChangeCustomerChoice()+203>` | Done — skip the remaining checks. |
| 0x12e0 <+105> | `mov 0x201012(%rip),%eax # <changechoice>` | Reload `changechoice` (record != 1 path). |
| 0x12e6 <+111> | `cmp $0x2,%eax` | Check if the user chose record 2. |
| 0x12e9 <+114> | `jne 0x12f9 <ChangeCustomerChoice()+130>` | If not, skip to the next check. |
| 0x12eb <+116> | `mov 0x20100b(%rip),%eax # <newservice>` | Load the new value. |
| 0x12f1 <+122> | `mov %eax,0x200d6d(%rip) # <num2>` | Write it into `num2`. |
| 0x12f7 <+128> | `jmp 0x1342 <ChangeCustomerChoice()+203>` | Done. |
| 0x12f9 <+130> | `mov 0x200ff9(%rip),%eax # <changechoice>` | Reload `changechoice` (record != 2 path). |
| 0x12ff <+136> | `cmp $0x3,%eax` | Check if the user chose record 3. |
| 0x1302 <+139> | `jne 0x1312 <ChangeCustomerChoice()+155>` | If not, skip to the next check. |
| 0x1304 <+141> | `mov 0x200ff2(%rip),%eax # <newservice>` | Load the new value. |
| 0x130a <+147> | `mov %eax,0x200d58(%rip) # <num3>` | Write it into `num3`. |
| 0x1310 <+153> | `jmp 0x1342 <ChangeCustomerChoice()+203>` | Done. |
| 0x1312 <+155> | `mov 0x200fe0(%rip),%eax # <changechoice>` | Reload `changechoice` (record != 3 path). |
| 0x1318 <+161> | `cmp $0x4,%eax` | Check if the user chose record 4. |
| 0x131b <+164> | `jne 0x132b <ChangeCustomerChoice()+180>` | If not, skip to the last check. |
| 0x131d <+166> | `mov 0x200fd9(%rip),%eax # <newservice>` | Load the new value. |
| 0x1323 <+172> | `mov %eax,0x200d43(%rip) # <num4>` | Write it into `num4`. |
| 0x1329 <+178> | `jmp 0x1342 <ChangeCustomerChoice()+203>` | Done. |
| 0x132b <+180> | `mov 0x200fc7(%rip),%eax # <changechoice>` | Reload `changechoice` (record != 4 path). |
| 0x1331 <+186> | `cmp $0x5,%eax` | Check if the user chose record 5. |
| 0x1334 <+189> | `jne 0x1342 <ChangeCustomerChoice()+203>` | If not (invalid entry, not 1-5), fall through and exit with no changes made. |
| 0x1336 <+191> | `mov 0x200fc0(%rip),%eax # <newservice>` | Load the new value. |
| 0x133c <+197> | `mov %eax,0x200d2e(%rip) # <num5>` | Write it into `num5`. |
| 0x1342 <+203> | `nop` | Padding/alignment (landing point for all the `jmp`s above). |
| 0x1343 <+204> | `pop %rbp` | Restore caller's base pointer. |
| 0x1344 <+205> | `ret` | Return to `main`. |
