// The array of prefixes you want to match
const prefixes = ["CLI_000028-BAN_000066-AGE_000054", "CLI_000028"];

// Dynamically create an array of regex conditions
const orConditions = prefixes.map(prefix => {
  return {
    "hierarchy_id": {
      "$regex": `^${prefix}`
    }
  };
});

// The final query object
const query = {
  "$or": orConditions
};

// Execute the find command
db.accounts.find(query);