/* ---------- Editable settings ---------- */
const CONFIG = {
  whatsappNumber: "601113207364",  // country code, no + or dashes. Empty = WhatsApp buttons go to the contact page
  whatsappMessage: "Hi Tony, I visited your website and would like to explore some property options.",
  atlasUrl: "https://kl-property-atlas-tonyhoo.netlify.app/"
};
const PROJECTS = [
  {name:"The Queenswoodz", area:"Bukit Jalil", developer:"EXSIM", type:"Serviced residence", tenure:"Leasehold", status:"Selling"},
  {name:"The Vividz", area:"Bukit Jalil", developer:"EXSIM", type:"Serviced residence", tenure:"To confirm", status:"Selling"},
  {name:"Oaka Residences", area:"Bukit Jalil", developer:"Berjaya", type:"Condominium", tenure:"Freehold", status:"To confirm"},
  {name:"Aetas", area:"Taman Desa", developer:"To confirm", type:"Condominium", tenure:"Freehold", status:"Selling"}
];

const el = id => document.getElementById(id);

/* ---------- Theme toggle (same idea as the Atlas) ---------- */
const root = document.documentElement;
const isDark = () => root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
el("themeBtn").addEventListener("click", () => {
  root.dataset.theme = isDark() ? "light" : "dark";
  try { localStorage.setItem("th-theme", root.dataset.theme); } catch (e) {}
});

/* ---------- Projects (Properties page, and the preview on Home) ---------- */
document.querySelectorAll("[data-projects]").forEach(grid => {
  const limit = parseInt(grid.dataset.projects, 10) || PROJECTS.length;
  grid.innerHTML = PROJECTS.slice(0, limit).map(p => `
  <article class="pcard">
    <div class="top"><span class="area">📍 ${p.area}</span><span class="badge">${p.status}</span></div>
    <h3>${p.name}</h3>
    <dl><dt>Developer</dt><dd>${p.developer}</dd><dt>Type</dt><dd>${p.type}</dd><dt>Tenure</dt><dd>${p.tenure}</dd><dt>Latest price</dt><dd>In the Atlas</dd></dl>
    <div class="acts"><a class="btn btn-outline btn-sm" href="${CONFIG.atlasUrl}" target="_blank" rel="noopener">Compare</a><a class="btn btn-wa btn-sm js-ask" data-project="${p.name}" href="/contact/">💬 Ask Tony</a></div>
  </article>`).join("");
});

/* ---------- WhatsApp ---------- */
const waLink = m => `https://wa.me/${CONFIG.whatsappNumber}?text=${encodeURIComponent(m)}`;
document.querySelectorAll(".js-wa").forEach(a => {
  if (CONFIG.whatsappNumber) { a.href = waLink(CONFIG.whatsappMessage); a.target = "_blank"; a.rel = "noopener"; }
});
document.querySelectorAll(".js-ask").forEach(a => {
  const m = `Hi Tony, I'd like to know more about ${a.dataset.project}.`;
  if (CONFIG.whatsappNumber) { a.href = waLink(m); a.target = "_blank"; a.rel = "noopener"; }
});

/* ---------- Mobile menu ---------- */
const menuBtn = el("menuBtn"), mobileNav = el("mobileNav");
const setMenu = o => { mobileNav.hidden = !o; menuBtn.setAttribute("aria-expanded", String(o)); menuBtn.textContent = o ? "✕" : "☰"; };
menuBtn.addEventListener("click", () => setMenu(mobileNav.hidden));

/* ---------- Calculator (Calculator page only) ---------- */
if (el("price")) {
  const rm = n => "RM " + Math.round(n).toLocaleString("en-MY");
  const parse = v => parseFloat(String(v).replace(/[^0-9.]/g, ""));
  const monthlyPayment = (P, ratePct, years) => { const n = years * 12, r = ratePct / 100 / 12; if (P <= 0 || n <= 0) return 0; if (r === 0) return P / n; return P * r / (1 - Math.pow(1 + r, -n)); };
  const lim = {price:[100000,20000000,"Property price must be between RM100,000 and RM20,000,000."],margin:[10,100,"Loan margin must be between 10% and 100%."],rate:[0,15,"Interest rate must be between 0% and 15%."],tenure:[1,35,"Loan tenure must be between 1 and 35 years."]};
  const calc = () => {
    const v = {price:parse(el("price").value),margin:parse(el("margin").value),rate:parse(el("rate").value),tenure:parse(el("tenure").value)};
    const bad = Object.keys(lim).find(k => isNaN(v[k]) || v[k] < lim[k][0] || v[k] > lim[k][1]);
    const err = el("calcErr");
    if (bad) { err.textContent = lim[bad][2]; err.hidden = false; return; }
    err.hidden = true;
    const loan = v.price * v.margin / 100, down = v.price - loan, m = monthlyPayment(loan, v.rate, v.tenure), total = m * v.tenure * 12, interest = total - loan;
    el("oPrice").textContent = rm(v.price); el("oLoan").textContent = rm(loan) + ` (${v.margin}%)`; el("oDown").textContent = rm(down);
    el("oInt").textContent = rm(interest); el("oMonthly").textContent = rm(m);
    const pp = total > 0 ? loan / total * 100 : 100; el("barP").style.width = pp + "%"; el("barI").style.width = (100 - pp) + "%";
  };
  [["price","priceR"],["margin","marginR"],["rate","rateR"],["tenure","tenureR"]].forEach(([i, r]) => {
    const inp = el(i), rng = el(r);
    rng.addEventListener("input", () => { inp.value = i === "price" ? Number(rng.value).toLocaleString("en-MY") : rng.value; calc(); });
    inp.addEventListener("input", () => { const x = parse(inp.value); if (!isNaN(x)) rng.value = x; calc(); });
    if (i === "price") inp.addEventListener("blur", () => { const x = parse(inp.value); if (!isNaN(x)) inp.value = Math.round(x).toLocaleString("en-MY"); });
  });
  calc();
}

/* ---------- Lead form (Contact page only; not connected yet, so never fake a success) ---------- */
if (el("leadForm")) {
  el("leadForm").addEventListener("submit", e => {
    e.preventDefault();
    const err = el("formErr"), msg = el("formMsg");
    const name = el("fName").value.trim(), phone = el("fPhone").value.trim(), email = el("fEmail").value.trim();
    let p = "";
    if (!name) p = "Please enter your name.";
    else if (phone.replace(/\D/g, "").length < 9) p = "Please enter a phone number I can reach you on.";
    else if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) p = "That email address doesn't look right.";
    else if (!el("fConsent").checked) p = "Please tick the consent box so I can contact you.";
    if (p) { err.textContent = p; err.hidden = false; msg.hidden = true; return; }
    err.hidden = true;
    const purpose = document.querySelector('input[name="purpose"]:checked').value;
    const s = `Name: ${name}\nPhone: ${phone}${email ? "\nEmail: " + email : ""}\nArea: ${el("fArea").value}\nBudget: ${el("fBudget").value}\nPurpose: ${purpose}${el("fMsg").value.trim() ? "\nMessage: " + el("fMsg").value.trim() : ""}`;
    msg.innerHTML = "<strong>Draft preview: nothing was sent.</strong> Once connected, this goes to your Leads Google Sheet and the visitor sees a thank-you page. This is what it would deliver:";
    const pre = document.createElement("pre"); pre.textContent = s; msg.appendChild(pre); msg.hidden = false;
  });
  ["fName","fPhone","fEmail","fConsent"].forEach(id => el(id).addEventListener("input", () => el("formErr").hidden = true));
}

el("yr").textContent = new Date().getFullYear();
