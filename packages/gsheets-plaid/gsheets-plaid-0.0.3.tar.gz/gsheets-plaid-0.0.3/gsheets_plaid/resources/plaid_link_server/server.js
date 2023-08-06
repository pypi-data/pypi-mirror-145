/*
server.js – Configures the Plaid client and uses Express to defines routes that call Plaid endpoints in the Sandbox environment.
Utilizes the official Plaid node.js client library to make calls to the Plaid API.
*/

const express = require("express");
const bodyParser = require("body-parser");
const session = require("express-session");
const fs = require("fs");
const { Configuration, PlaidApi, PlaidEnvironments } = require("plaid");
const path = require("path");
const app = express();

app.use(
  // FOR DEMO PURPOSES ONLY
  // Use an actual secret key in production
  session({ secret: "bosco", saveUninitialized: true, resave: true })
);

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get("/", async (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.get("/oauth", async (req, res) => {
  res.sendFile(path.join(__dirname, "oauth.html"));
});

let plaidSecret = process.env.PLAID_SECRET_SANDBOX;
if (process.env.PLAID_ENV === 'development') {
  plaidSecret = process.env.PLAID_SECRET_DEVELOPMENT;
} else if (process.env.PLAID_ENV === 'production') {
  plaidSecret = process.env.PLAID_SECRET_PRODUCTION;
}

// Configuration for the Plaid client
const config = new Configuration({
  basePath: PlaidEnvironments[process.env.PLAID_ENV],
  baseOptions: {
    headers: {
      "PLAID-CLIENT-ID": process.env.PLAID_CLIENT_ID,
      "PLAID-SECRET": plaidSecret,
      "Plaid-Version": "2020-09-14",
    },
  },
});

//Instantiate the Plaid client with the configuration
const client = new PlaidApi(config);

//Creates a Link token and return it
app.get("/api/create_link_token", async (req, res, next) => {
  const tokenResponse = await client.linkTokenCreate({
    user: { client_user_id: req.sessionID },
    client_name: "Plaid's Tiny Quickstart",
    language: "en",
    products: ["transactions"],
    country_codes: ["US"],
    redirect_uri: process.env.PLAID_SANDBOX_REDIRECT_URI,
  });
  res.json(tokenResponse.data);
});

// Exchanges the public token from Plaid Link for an access token
app.post("/api/exchange_public_token", async (req, res, next) => {
  const exchangeResponse = await client.itemPublicTokenExchange({
    public_token: req.body.public_token,
  });

  let file_contents = '[]';
  try {
    file_contents = fs.readFileSync(process.env.PLAID_TOKENS_OUTPUT_FILENAME, "utf8");
  } catch (err) {
    console.log(err);
    console.log("The tokens file probably just didn't exist yet.");
  }
  const tokens = new Map(JSON.parse(file_contents).map(x => [x['item_id'], x['access_token']]));
  tokens.set(exchangeResponse.data.item_id, exchangeResponse.data.access_token);
  tokens_json = JSON.stringify(Array.from(tokens, ([item_id, access_token]) => ({ item_id, access_token })));
  fs.writeFile(process.env.PLAID_TOKENS_OUTPUT_FILENAME, tokens_json, "utf8", (err) => {
    if (err) throw err;
    console.log("Tokens written successfully.");
  });

  // FOR DEMO PURPOSES ONLY
  // Store access_token in DB instead of session storage
  req.session.access_token = exchangeResponse.data.access_token;
  res.json(true);
});

// Fetches balance data using the Node client library for Plaid
app.get("/api/data", async (req, res, next) => {
  const access_token = req.session.access_token;
  const balanceResponse = await client.accountsBalanceGet({ access_token });
  res.json({
    Balance: balanceResponse.data,
  });
});

// Checks whether the user's account is connected, called
// in index.html when redirected from oauth.html
app.get("/api/is_account_connected", async (req, res, next) => {
  return (req.session.access_token ? res.json({ status: true }) : res.json({ status: false}));
});

app.listen(process.env.PLAID_LINK_PORT || 8080);
