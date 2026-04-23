const fs = require("fs");

const affiliate =
"http://convert.ctypy.com/aff_c?offer_id=29465&aff_id=21885";

const cities = ["Tokyo","London","Paris","Dubai","New York","Bangkok"];
const intents = ["cheap flights","flight deals","budget travel","airfare savings"];

function rand(a){ return a[Math.floor(Math.random()*a.length)]; }

function makePost(city,intent){

const templates = [
`✈️ Cheapest ${intent} to ${city} just dropped!

Compare live fares and save instantly.

👉 ${affiliate}

#travel #flights #${city.toLowerCase()}`,

`Looking for ${intent} to ${city}?  
Prices change daily — don’t overpay.

Check deals here:
👉 ${affiliate}`,

`Stop overpaying for flights to ${city} ✈️

Smart travelers use real-time comparison tools.

Start saving:
👉 ${affiliate}`
];

return rand(templates);
}

let posts = [];

for(let i=1;i<=50;i++){

const city = rand(cities);
const intent = rand(intents);

posts.push({
  platform: "x",
  content: makePost(city,intent),
  city,
  intent
});
}

fs.writeFileSync("social-posts.json", JSON.stringify(posts,null,2));

console.log("Social posts generated: 50 ready-to-post entries");
