// setup_db_users.js - creates least-privilege users for the AAC database.
//
// Usage (MongoDB running; if auth is already on, connect as an admin first):
//   mongosh setup_db_users.js
//
// aac_reader : read-only. Use this account for the dashboard.
// aac_writer : read/write. Use only for maintenance scripts and CRUD tests.
// Passwords are typed at the prompt so they never appear in this file or in shell history.

const aac = db.getSiblingDB("aac");

aac.createUser({
  user: "aac_reader",
  pwd: passwordPrompt(),
  roles: [{ role: "read", db: "aac" }]
});

aac.createUser({
  user: "aac_writer",
  pwd: passwordPrompt(),
  roles: [{ role: "readWrite", db: "aac" }]
});

print("Created aac_reader (read) and aac_writer (readWrite). Restart mongod with --auth.");
