const fs = require("fs");

const affiliate =
"http://convert.ctypy.com/aff_c?offer_id=29465&aff_id=21885";

const cities = [
"Tokyo","London","Paris","Dubai","Rome","Bangkok",
"Barcelona","New York","Chicago","Berlin","Madrid","Sydney"
];

const intents = [
"cheap-flights-to",
"best-time-to-book",
"flight-deals-for",
"budget-travel-guide",
"airfare-savings-for"
];

function rand(a){ return a[Math.floor(Math.random()*a.length)]; }

let pages = [];
let links = {};

if(!fs.existsSync("pages")) fs.mkdirSync("pages");
if(!fs.existsSync("pages/guides")) fs.mkdirSync("pages/guides");

/* =========================
   CONTENT GENERATOR (UNIQUE STRUCTURE)
========================= */

function article(city,intent,i){

const hook = [
"Airfare prices change dynamically based on demand.",
"Flight pricing systems update every few hours.",
"Smart travelers use timing strategies to save money."
];

const tips = [
"Compare airlines before booking.",
"Use flexible travel dates.",
"Check price trends weekly."
];

return `<!DOCTYPE html>
<html>
<head>
<title>${intent} ${city}</title>
<meta name="description" content="Guide for ${intent} ${city}">
</head>

<body>

<h1>${intent} ${city}</h1>

<p>${hook[Math.floor(Math.random()*hook.length)]}</p>

<h2>Flight Strategy</h2>
<p>
Understanding airline pricing gives you an advantage when booking flights.
</p>

<h2>Money Saving Tips</h2>
<ul>
<li>${tips[Math.floor(Math.random()*tips.length)]}</li>
<li>${tips[Math.floor(Math.random()*tips.length)]}</li>
<li>${tips[Math.floor(Math.random()*tips.length)]}</li>
</ul>

<h2>Related Pages</h2>
<ul>
<li><a href="/pages/guides/${city.toLowerCase()}-guide.html">City Guide</a></li>
</ul>

<a href="${affiliate}?id=${i}">Search Flights</a>

</body>
</html>`;
}

/* =========================
   GENERATE 100 PAGES
========================= */

for(let i=1;i<=100;i++){

const city = rand(cities);
const intent = rand(intents);

const file = `${intent}-${city}-${i}.html`;

fs.writeFileSync("pages/"+file, article(city,intent,i));

pages.push(file);

/* link graph */
links[file] = pages.slice(-5);
}

/* =========================
   SITEMAP
========================= */

let sitemap =
`<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`;

pages.forEach(p=>{
  sitemap += `<url><loc>https://YOURNAME.github.io/pages/${p}</loc></url>`;
});

sitemap += `</urlset>`;

fs.writeFileSync("sitemap.xml", sitemap);
fs.writeFileSync("link-graph.json", JSON.stringify(links,null,2));

console.log("SEO SYSTEM BUILT: 100 pages + links + sitemap");
