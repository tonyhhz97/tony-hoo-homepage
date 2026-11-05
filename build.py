"""Builds Tony Hoo's multi-page site from src/.

Run:  python3 build.py
Output: index.html, about/, services/, properties/, calculator/, stories/, contact/, privacy/
(each folder holds an index.html, so Netlify serves clean URLs like /calculator/),
plus assets/site.css and assets/site.js shared by every page.

Edit the shared header/footer/nav here, page content in PAGES below or in src/*.html,
styles in src/base.css (+ EXTRA_CSS), and settings (WhatsApp number, project list) in src/site.js.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
part = lambda name: (SRC / f"{name}.html").read_text()

SITE_URL = "https://tonyhoo-homepage.netlify.app"  # switch to the custom domain when it's connected

NAV = [  # (path, label in desktop nav, label in mobile menu)
    ("/about/", "About", "About Tony"),
    ("/services/", "How I Help", "How I help"),
    ("/properties/", "Properties", "Properties"),
    ("/calculator/", "Calculator", "Loan calculator"),
    ("/stories/", "Stories", "Client stories"),
    ("/contact/", "Contact", "Contact"),
]

EXTRA_CSS = """
/* ---------- multi-page additions ---------- */
.nav-links a[aria-current="page"]{color:var(--ink);font-weight:700;box-shadow:inset 0 -2px 0 var(--gold)}
.mobile-nav a[aria-current="page"]{color:var(--gold-text);font-weight:700}
.page-hero{position:relative;overflow:hidden;color:#f5efe1;background:#16130d}
.page-hero::before{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;
  background-image:linear-gradient(to bottom,rgba(22,19,13,.6) 0%,rgba(22,19,13,.45) 50%,#16130d 100%),url('/assets/skyline.jpg');
  background-size:cover;background-position:center 38%}
.page-hero .container{position:relative;z-index:1;padding-block:48px 40px;display:grid;gap:10px}
.page-hero .eyebrow{color:#e3bd77;text-shadow:0 0 3px rgba(0,0,0,.85)}
.page-hero h1{font-size:clamp(2rem,4.4vw,3rem);line-height:1.08;text-shadow:0 0 4px rgba(0,0,0,.85),0 0 14px rgba(0,0,0,.6)}
.page-hero p.lead{font-size:1.15rem;color:#f7f3ea;max-width:62ch;text-shadow:0 0 3px rgba(0,0,0,.85)}
.crumbs{font-size:.92rem;color:#c2b8a3}
.crumbs a{color:#e3bd77;text-decoration:none}
.explore-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
@media (max-width:1000px){.explore-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.explore-grid{grid-template-columns:1fr}}
a.explore{display:grid;gap:8px;align-content:start;text-decoration:none;color:inherit;transition:border-color .15s ease,transform .15s ease}
a.explore:hover{border-color:var(--gold);transform:translateY(-2px)}
a.explore .go{color:var(--gold-text);font-weight:700;margin-top:4px}
.more{margin-top:22px;display:flex;flex-wrap:wrap;gap:10px}
.cta-band{background:var(--bg-soft);border-top:1px solid var(--line)}
.cta-band .container{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:18px}
.cta-band h2{font-size:clamp(1.5rem,2.8vw,1.9rem)}
.cta-band p{color:var(--ink-soft)}
.cta-band .acts{display:flex;flex-wrap:wrap;gap:10px}

/* ---------- motion + photo backgrounds (v3) ---------- */
.page-hero::before{animation:bgSlowZoom 15s ease-in-out infinite alternate}
.page-hero.ph-team::before{background-image:linear-gradient(to bottom,rgba(22,19,13,.72) 0%,rgba(22,19,13,.55) 50%,#16130d 100%),url('/assets/skyline2.jpg');background-position:center 30%}
/* light-mode (and dark) photo backdrops: building / team, slowly moving, faded so text stays readable */
.bgph{position:relative;isolation:isolate;overflow:hidden}
.bgph::before{content:"";position:absolute;inset:-2%;z-index:-2;background-size:cover;background-position:center;opacity:.13;animation:bgSlowZoom 15s ease-in-out infinite alternate;pointer-events:none}
.bgph::after{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:linear-gradient(to bottom,var(--bg) 0%,transparent 14%,transparent 86%,var(--bg) 100%)}
.bg-city::before{background-image:url('/assets/skyline.jpg')}
.bg-team::before{background-image:url('/assets/skyline2.jpg');background-position:center 35%}
:root[data-theme="dark"] .bgph::before{opacity:.2}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .bgph::before{opacity:.2}}
/* hero stats: 4 across on desktop (the .hero .container grid rule was winning) */
.hero .container.hero-stats{grid-template-columns:repeat(4,1fr);padding-block:0 40px;gap:10px}
@media (max-width:860px){.hero .container.hero-stats{grid-template-columns:repeat(2,1fr)}}
/* closing photo band */
.cta-band{position:relative;isolation:isolate;overflow:hidden;background:#16130d;color:#f5efe1;border-top:0}
.cta-band::before{content:"";position:absolute;inset:-2%;z-index:-2;background:linear-gradient(90deg,rgba(22,19,13,.82) 0%,rgba(22,19,13,.3) 100%),url('/assets/skyline2.jpg') center 38%/cover;animation:bgSlowZoom 15s ease-in-out infinite alternate}
.cta-band p{color:#e6dcc6}
.cta-band h2{text-shadow:0 0 12px rgba(0,0,0,.6)}
.cta-band .btn-outline{color:#f5efe1;border-color:rgba(245,239,225,.5)}
/* buttons: lift, light sweep, press, ripple */
.btn{position:relative;overflow:hidden;isolation:isolate;transition:transform .25s cubic-bezier(.2,.8,.2,1),box-shadow .25s ease,border-color .2s ease,background-color .2s ease}
.btn::after{content:"";position:absolute;top:0;bottom:0;left:-70%;width:50%;z-index:-1;background:linear-gradient(105deg,transparent,rgba(255,255,255,.35),transparent);transform:skewX(-18deg);transition:left .6s ease}
.btn:hover{transform:translateY(-3px)}
.btn:hover::after{left:130%}
.btn:active{transform:translateY(0) scale(.97)}
.btn-outline:hover{background:rgba(184,134,47,.12)}
.btn .arr{display:inline-block;transition:transform .25s ease}
.btn:hover .arr{transform:translateX(4px)}
.ripple{position:absolute;border-radius:50%;background:rgba(255,255,255,.45);transform:scale(0);animation:ripple .6s ease-out forwards;pointer-events:none;z-index:-1}
@keyframes ripple{to{transform:scale(4);opacity:0}}
.btn-gold{animation:goldPulse 3.2s ease-in-out infinite}
@keyframes goldPulse{0%,100%{box-shadow:0 6px 20px rgba(184,134,47,.35)}50%{box-shadow:0 8px 28px rgba(184,134,47,.6)}}
.btn-gold:hover{animation:none;box-shadow:0 12px 30px rgba(184,134,47,.5)}
/* cards + links */
.card,.handle,.pcard,a.explore{transition:transform .3s cubic-bezier(.2,.8,.2,1),box-shadow .3s ease,border-color .2s ease}
.card:hover,.handle:hover,.pcard:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg);border-color:var(--gold)}
a.explore:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg)}
.nav-links a{position:relative}
.nav-links a::after{content:"";position:absolute;left:10px;right:10px;bottom:2px;height:2px;background:var(--gold);transform:scaleX(0);transform-origin:left;transition:transform .3s ease}
.nav-links a:hover::after{transform:scaleX(1)}
.photos img{transition:transform .4s ease,box-shadow .4s ease}
.photos figure:hover img{transform:scale(1.05) rotate(-1deg);box-shadow:var(--shadow-lg)}
/* scroll reveal */
.js .reveal{opacity:0;transform:translateY(22px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.8,.2,1);transition-delay:var(--d,0s)}
.js .reveal.in{opacity:1;transform:none}
"""

HEAD_THEME = '<script>try{var t=localStorage.getItem("th-theme");if(t)document.documentElement.dataset.theme=t}catch(e){}</script>'


def nav(active):
    links = "\n      ".join(
        f'<a href="{p}"{" aria-current=\"page\"" if p == active else ""}>{d}</a>' for p, d, _ in NAV)
    mobile = "".join(
        f'<a href="{p}"{" aria-current=\"page\"" if p == active else ""}>{m}</a>' for p, _, m in NAV)
    return f'''<nav class="nav" aria-label="Main">
  <div class="container nav-inner">
    <a class="brand" href="/">
      <span class="brand-mark" aria-hidden="true">TH</span>
      <span><span class="brand-title">Tony Hoo | Your Neighbourhood Home Advisor</span><span class="brand-tagline" style="display:block">IQI Realty · Klang Valley New Launches · @tonyhoo_97</span></span>
    </a>
    <div class="nav-links">
      {links}
    </div>
    <div class="nav-actions">
      <button class="icon-btn" id="themeBtn" aria-label="Switch light or dark mode" title="Light / dark">🌓</button>
      <a class="btn btn-wa btn-sm js-wa" href="/contact/">💬<span class="lbl"> WhatsApp Tony</span></a>
      <button class="icon-btn menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mobileNav" aria-label="Menu">☰</button>
    </div>
  </div>
  <div class="container mobile-nav" id="mobileNav" hidden>
    <a href="/"{" aria-current=\"page\"" if active == "/" else ""}>Home</a>{mobile}
  </div>
</nav>'''


FOOTER = '''<footer>
  <div class="container foot">
    <div style="display:grid;gap:8px">
      <b style="font-size:1.5rem">Tony Hoo</b>
      <span style="color:#c2b8a3">Your Neighbourhood Home Advisor · Transparent Comparisons. Better Decisions.</span>
      <span style="color:#c2b8a3">REN 75480 · IQI Realty</span>
    </div>
    <div><h4>Explore</h4><ul><li><a href="/about/">About Tony</a></li><li><a href="/services/">How I Help</a></li><li><a href="/properties/">Properties</a></li><li><a href="/calculator/">Loan Calculator</a></li><li><a href="/stories/">Client Stories</a></li><li><a href="/contact/">Contact</a></li></ul></div>
    <div><h4>Tools &amp; social</h4><ul><li><a href="https://kl-property-atlas-tonyhoo.netlify.app/" target="_blank" rel="noopener">KL Projects Atlas</a></li><li><a href="https://tonyhoo-home-loan-calculator.netlify.app/" target="_blank" rel="noopener">Full Home Loan Calculator</a></li><li><a href="https://www.instagram.com/tonyhoo_97/" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://www.tiktok.com/@tonyhoo_97" target="_blank" rel="noopener">TikTok</a></li><li><a href="https://www.youtube.com/@tonyhoo97" target="_blank" rel="noopener">YouTube</a></li><li><a href="/privacy/">Privacy notice</a></li></ul></div>
    <p class="fine">This is the personal website of Tony Hoo (REN 75480), a real estate negotiator with IQI Realty [agency registration no. to add]. It is not the official website of any developer. Project information is for reference and may change without notice; please confirm the latest details before making a decision. Loan figures are illustrative estimates, not financing offers. © <span id="yr"></span> Tony Hoo.</p>
  </div>
</footer>

<a class="btn btn-wa wa-float js-wa" href="/contact/" aria-label="WhatsApp Tony">💬 WhatsApp</a>'''


def page_hero(eyebrow, title, lead, crumb):
    return f'''<header class="page-hero">
    <div class="container">
      <p class="crumbs"><a href="/">Home</a> / {crumb}</p>
      <p class="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
    </div>
  </header>'''


def strip_head(html):
    """Drop a section's own heading block when the page hero already carries it."""
    return re.sub(r'\s*<div class="section-head"[^>]*>.*?</div>', '', html, count=1, flags=re.S)


def cta_band(title, text):
    return f'''<section class="section cta-band">
    <div class="container">
      <div style="display:grid;gap:6px;max-width:640px"><h2>{title}</h2><p>{text}</p></div>
      <div class="acts"><a class="btn btn-wa js-wa" href="/contact/">💬 WhatsApp Tony</a><a class="btn btn-outline" href="/contact/">Send an enquiry</a></div>
    </div>
  </section>'''


def fix_links(html):
    return (html.replace('href="#projects"', 'href="/properties/"').replace('href="#about"', 'href="/about/"')
                .replace('href="#contact"', 'href="/contact/"').replace('href="#privacy"', 'href="/privacy/"')
                .replace('href="#calculator"', 'href="/calculator/"').replace('href="#stories"', 'href="/stories/"')
                .replace('src="assets/', 'src="/assets/')
                .replace('id="pgrid"', 'data-projects=""'))


# ---------- page bodies ----------
_st = part("stories")
testi_cards = _st[_st.index('<div class="tgrid">'):_st.index('<div class="photos">')].rstrip()

HOME = fix_links(part("hero")) + "\n\n" + fix_links(part("approach")) + '''

  <section class="section journey">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Explore</p>
        <h2>Everything you need to decide, in one place.</h2>
        <p>Start wherever you are in your search.</p>
      </div>
      <div class="explore-grid">
        <a class="card explore" href="/services/"><span class="ico" aria-hidden="true">🧭</span><h3>How I help</h3><p>Six stops from first search to key collection, and what happens at each one.</p><span class="go">See the journey →</span></a>
        <a class="card explore" href="/properties/"><span class="ico" aria-hidden="true">🏙️</span><h3>Properties</h3><p>The Bukit Jalil and Klang Valley projects I'm following closely right now.</p><span class="go">View projects →</span></a>
        <a class="card explore" href="/calculator/"><span class="ico" aria-hidden="true">🧮</span><h3>Loan calculator</h3><p>Check your monthly instalment, loan amount and down payment in seconds.</p><span class="go">Try the calculator →</span></a>
        <a class="card explore" href="/stories/"><span class="ico" aria-hidden="true">💬</span><h3>Client stories</h3><p>What buyers say about comparing projects and deciding with me.</p><span class="go">Read their stories →</span></a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">💬 What buyers say</p>
        <h2>From the buyers I've worked with.</h2>
      </div>
      ''' + testi_cards + '''
      <div class="more"><a class="btn btn-outline" href="/stories/">Read all client stories</a></div>
    </div>
  </section>

  ''' + cta_band("Have a question? Talk to Tony.", "No pressure and no obligation. Tell me what you're looking for and I'll come back with options that fit.")

ABOUT = page_hero("About Tony", "More than property. It's about the people behind every decision.",
                  "I'm Tony Hoo (REN 75480, IQI Realty), a property advisor for new launches in Bukit Jalil and the Klang Valley.", "About") + '''

  <section class="section">
    <div class="container story-grid">
      <div class="hero-photo" style="justify-self:start">
        <div class="portrait"><img src="/assets/tony.jpg" alt="Tony Hoo, property advisor"></div>
        <p class="who" style="color:var(--ink)">Tony Hoo<small style="color:var(--ink-soft)">REN 75480 · IQI Realty</small></p>
      </div>
      <div class="placeholder">
        <span class="pill-gold draft" style="justify-self:start">Your words go here</span>
        <p>Three or four short paragraphs in your own voice. Things worth covering:</p>
        <ul>
          <li>How you got into real estate, and why new launches</li>
          <li>A buyer you helped who changed how you work</li>
          <li>Why you built the Atlas and the calculator instead of just sending brochures</li>
          <li>What buyers can expect from you, and what you won't do</li>
        </ul>
      </div>
    </div>
  </section>

''' + fix_links(part("approach")).replace('class="section"', 'class="section journey"', 1) + "\n\n" + fix_links(part("social")) + "\n\n  " + cta_band("Want to talk it through?", "Tell me where you are in your search and I'll point you to the right next step.")

SERVICES = page_hero("How I help", "Clear guidance from first search to key collection.",
                     "Each stop has a tool or a checklist behind it, so you always know what happens next.", "How I Help") + "\n\n" + \
    strip_head(fix_links(part("journey"))).replace('class="section journey"', 'class="section"', 1) + "\n\n  " + \
    cta_band("Not sure which stop you're at?", "Message me and we'll start with your budget and priorities.")

PROPERTIES = page_hero("Featured projects", "Projects I'm following closely right now.",
                       "Live prices, PSF and availability are in the KL Projects Atlas, updated weekly from developer sales galleries.", "Properties") + "\n\n" + \
    strip_head(fix_links(part("projects"))).replace('<div class="note">', '<div class="more"><a class="btn btn-gold" href="https://kl-property-atlas-tonyhoo.netlify.app/" target="_blank" rel="noopener">📊 Compare All Projects in the Atlas</a></div>\n      <div class="note">', 1) + "\n\n  " + \
    cta_band("Want the latest price list?", "Ask me about any project and I'll send the current prices, layouts and availability.")

CALCULATOR = page_hero("Home loan calculator", "What would your monthly instalment be?",
                       "A quick estimate. The full Integrated Home Loan Calculator also covers rebates, upfront cash and DSR.", "Loan Calculator") + "\n\n" + \
    strip_head(fix_links(part("calculator")))

STORIES = page_hero("💬 Client stories", "From the buyers I've worked with.",
                    "Real buyers, real decisions. Here's what they say about comparing projects with me.", "Client Stories") + "\n\n" + \
    strip_head(fix_links(part("stories"))) + "\n\n  " + \
    cta_band("Ready to start your own search?", "Tell me what you're looking for and we'll go from there.")

CONTACT = page_hero("Contact", "Have a question? Talk to Tony.",
                    "No pressure and no obligation. WhatsApp me or send the form below.", "Contact") + "\n\n" + \
    fix_links(part("contact")).replace('<span class="muted" id="waNote"></span>', '')

PRIVACY = page_hero("Privacy notice", "How I handle your details.",
                    "What I collect when you send an enquiry, and what I do with it.", "Privacy notice") + "\n\n" + \
    fix_links(part("privacy")).replace('class="privacy"', 'class="section"', 1)

PAGES = [  # (output path, nav path, <title>, meta description, body)
    ("index.html", "/", "Tony Hoo | Your Neighbourhood Home Advisor",
     "Tony Hoo (REN 75480, IQI Realty), property advisor for new launches in Bukit Jalil and the Klang Valley. Compare projects, check your monthly instalment, and talk it through before you commit.", HOME),
    ("about/index.html", "/about/", "About Tony Hoo | Property Advisor, Bukit Jalil & Klang Valley",
     "Meet Tony Hoo (REN 75480, IQI Realty): transparent comparisons, the full cost upfront, and trade-offs said plainly.", ABOUT),
    ("services/index.html", "/services/", "How I Help | Tony Hoo Property",
     "From first search to key collection: how Tony Hoo guides buyers through comparing, calculating, viewing, booking and handover.", SERVICES),
    ("properties/index.html", "/properties/", "Properties | Bukit Jalil & Klang Valley New Launches | Tony Hoo",
     "New launch projects in Bukit Jalil and the Klang Valley that Tony Hoo is following closely, with links to live prices in the KL Projects Atlas.", PROPERTIES),
    ("calculator/index.html", "/calculator/", "Home Loan Calculator Malaysia | Tony Hoo",
     "Estimate your monthly instalment, loan amount, down payment and total interest for a Malaysian property purchase.", CALCULATOR),
    ("stories/index.html", "/stories/", "Client Stories | Tony Hoo Property",
     "What buyers say about comparing projects and deciding with Tony Hoo.", STORIES),
    ("contact/index.html", "/contact/", "Contact Tony Hoo | WhatsApp or Enquiry Form",
     "WhatsApp Tony Hoo or send an enquiry about Bukit Jalil and Klang Valley new launch properties.", CONTACT),
    ("privacy/index.html", "/privacy/", "Privacy Notice | Tony Hoo Property",
     "How Tony Hoo collects and uses the details you send through this website.", PRIVACY),
]


def decorate(body, active):
    n = [0]
    def sec(m):
        cls = m.group(1)
        if any(k in cls for k in ("calc", "privacy", "cta-band")):
            return m.group(0)
        n[0] += 1
        return f'<section class="{cls} bgph {"bg-city" if n[0] % 2 else "bg-team"}"'
    body = re.sub(r'<section class="([^"]*)"', sec, body)
    if active in ("/about/", "/stories/", "/contact/"):
        body = body.replace('<header class="page-hero">', '<header class="page-hero ph-team">')
    return body


def render(path, active, title, desc, body):
    url = SITE_URL + active
    body = decorate(body, active)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE_URL}/assets/tony.jpg">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
{HEAD_THEME}
<script>document.documentElement.classList.add("js")</script>
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
{nav(active)}

<main id="top">
  {body}
</main>

{FOOTER}

<script src="/assets/site.js"></script>
</body>
</html>
'''


def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "site.css").write_text((SRC / "base.css").read_text() + EXTRA_CSS)
    (ROOT / "assets" / "site.js").write_text((SRC / "site.js").read_text())
    for out, active, title, desc, body in PAGES:
        p = ROOT / out
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(render(out, active, title, desc, body))
    print(f"built {len(PAGES)} pages")


if __name__ == "__main__":
    main()
