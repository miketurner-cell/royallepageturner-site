/**
 * Hub (royallepageturner.com) site config + nav data -- consumed by the
 * shared js/nav.js renderer (Tier-1, byte-identical across the fleet).
 * This file is deliberately UN-synced -- every site has its own copy,
 * same shape as _fleet_config.py / agent_roster_loader.py's per-repo
 * sibling-data pattern. Load this script BEFORE js/nav.js on every page.
 *
 * Slice 3 step 4 (2026-09-09): the hub previously hand-baked its own nav
 * in 6 structurally distinct variants across 17 pages (see
 * [[nl-network-portal]] memory for the full catalog) -- this file plus
 * js/nav.js/js/footer.js replace all of them with the same shared
 * chrome the 3 spoke sites already use. Menu items + footer columns
 * extracted VERBATIM from the existing baked nav/footer (Variant 1, the
 * 12-page standard), not redesigned; the hub's own wordmark text is
 * intentionally dropped in favor of nav.js's hardcoded "Turner Realty"
 * -- this IS the point of Slice 3 (the same wordmark everywhere is what
 * makes the fleet read as one site). NAP borrowed from Gander HQ
 * (the hub has no physical office of its own), matching what the
 * hub's own pre-existing footer already showed.
 */
(function () {
  'use strict';

  var p = '', r = '';

  var SITE = {
    brandSub: 'Royal LePage',
    logo: r + 'images/rlp-logo.png',
    address: '204 Airport Blvd, Gander',
    email: 'miketurner@royallepage.ca',
    phone: '709-256-7999', phoneTel: '7092567999',
    facebook: 'https://www.facebook.com/realestategander',
    instagram: 'https://www.instagram.com/turnerrealty2014',
    youtube: 'https://www.youtube.com/playlist?list=PLr4XcQLT7UeO_8OZSgtx6h2N6dvsmsY_Y',
    ctaHref: p + 'contact.html',
    // js/nav.js is one fleet file now (2026-10-08); this site's own copy used 1024 as the menu breakpoint, kept here.
    navBreakpoint: 1024,
    // The new header (redesign, D-1009-10: the hub "as drawn"). OFF: nothing changes until Mike's GO flips this to 'v2'
    // (?header=v2 previews it on any page). Four words, one button, the phone; no search bar (the hub has no listings);
    // the regions sit in the phone menu's More line (js/nav.js adds them after the three links below).
    header: 'off',
    // js/nav.js loads css/header-v2.css with this ?v= (sha256[:8] of the file; tools/tests/header-v2-test.mjs fails when it is stale and prints the value)
    header2Stamp: '4f6b917c',
    header2: {
      region: 'The brokerage',
      office: '204 Airport Blvd, Gander &middot; 709-256-7999',
      bar: false, signIn: false, sheetCta: true,
      // asks the region first (home-value.html: Gander and Area / Avalon / Labrador), then hands over to that site's page
      ctaHref: p + 'home-value.html',
      menu: [
        { label: 'Offices', href: p + 'offices.html', items: [
          ['All offices', p + 'offices.html'],
          ['Gander and Area', 'https://realestategander.com'],
          ['Avalon', 'https://avalonrealestate.ca'],
          ['Labrador', 'https://goosebayrealestate.ca'],
          ['Labrador West', 'https://labwestrealty.com']
        ] },
        { label: 'Our team', href: p + 'team.html', items: [
          ['Our team', p + 'team.html'],
          ['Agent training', p + 'agent-training.html']
        ] },
        { label: 'Awards', href: p + 'awards.html', items: [
          ['Awards', p + 'awards.html'],
          ['The Shelter Foundation', p + 'shelter-foundation.html']
        ] },
        { label: 'Careers at Lab West', href: 'https://labwestrealty.com/become-a-realtor.html' }
      ],
      more: [
        ['Home', r + 'index.html'],
        ['About', p + 'about.html'],
        ['Our team', p + 'team.html'],
        ['Contact', p + 'contact.html']
      ]
    }
  };

  // Top-level MENU entries are {label, href} objects (nav.js's menuItem()
  // reads m.label/m.href directly) -- NOT [label, href] tuples, which are
  // only valid inside a dropdown's own items[] array. Preserves the exact
  // 9-item list the old baked nav (Variant 1) already showed, in order.
  var MENU = [
    { label: 'Home', href: r + 'index.html' },
    { label: 'Offices', href: p + 'offices.html' },
    { label: 'About', href: p + 'about.html' },
    { label: 'Awards', href: p + 'awards.html' },
    { label: 'Our Team', href: p + 'team.html' },
    { label: 'Shelter Foundation', href: p + 'shelter-foundation.html' },
    { label: 'Agent Training', href: p + 'agent-training.html' },
    { label: 'Careers at Lab West', href: 'https://labwestrealty.com/become-a-realtor.html' },
    { label: 'Contact', href: p + 'contact.html' }
  ];

  // Consumed by the shared js/footer.js. Content extracted verbatim from
  // the existing baked footer -- one real fix along the way: the
  // Offices column was missing Avalon on every page except index.html
  // (a real, flagged gap -- see the Slice 3 canvas's decision (d) note
  // on Avalon being the weakest node in the network); added here so it's
  // fixed everywhere at once via the shared config.
  var FOOTER = {
    copyright: '&copy; 1998&ndash;{year} Royal LePage Turner Realty (2014) Inc.',
    columns: [
      { heading: 'Company', links: [
        ['About Us', p + 'about.html'],
        ['Offices', p + 'offices.html'],
        ['Awards', p + 'awards.html'],
        // D-1009-19 (2026-10-09): Careers / Become a REALTOR removed while recruiting is off; the hub's one
        // careers link is 'Careers at Lab West' in the header menu above.
        ['Contact', p + 'contact.html']
      ] },
      { heading: 'Offices', links: [
        ['Gander', 'https://realestategander.com'],
        ['Avalon / St. John&rsquo;s', 'https://avalonrealestate.ca'],
        ['Happy Valley&ndash;Goose Bay', 'https://goosebayrealestate.ca'],
        ['Labrador West', 'https://labwestrealty.com']
      ] }
    ]
  };

  // Header v2 touch-ups that are this site's own (D-1009-10), done here so the shared js/nav.js and css/header-v2.css stay byte-identical
  // fleet-wide (always-on #27): nav.js hard-codes the button's words ("Get my home's value") and a Sign in link, and its phone sheet has no
  // button (the listing sites' bottom action bar carries it; this site has none). On turner:nav-injected, and only while the new header
  // is on (html.header-v2), this applies SITE.header2.ctaLabel / signIn:false / sheetCta:true. With the switch off it does nothing.
  if (typeof document.addEventListener === 'function') document.addEventListener('turner:nav-injected', function () {
    var h2 = SITE.header2, root = document.documentElement;
    if (!h2 || !root.classList.contains('header-v2')) return;
    var cta = document.querySelector('.nav2-cta');
    if (cta && h2.ctaLabel) cta.innerHTML = h2.ctaLabel;
    if (h2.signIn === false) { var si = document.querySelector('.nav2-signin'); if (si && si.parentNode) si.parentNode.removeChild(si); }
    var links = document.querySelector('.nav2-links');
    if (h2.sheetCta === true && links && !links.querySelector('.nav2-sheet-cta')) {
      var li = document.createElement('li');
      li.className = 'nav2-sheet-cta';
      li.innerHTML = '<a href="' + (h2.ctaHref || SITE.ctaHref) + '">' + (h2.ctaLabel || cta && cta.innerHTML || '') + '</a>';
      links.appendChild(li);
    }
    if (!document.getElementById('nav2-site-style')) {
      var st = document.createElement('style');
      st.id = 'nav2-site-style';
      st.textContent = 'html.header-v2 .nav2-sheet-cta{display:none}' +
        '@media (max-width:1023px){html.header-v2 .nav2-links>li.nav2-sheet-cta{display:block;padding:4px 0 8px}' +
        'html.header-v2 .nav2-links>li.nav2-sheet-cta>a{display:flex;align-items:center;justify-content:center;min-height:48px;padding:0 20px;border:0;border-radius:999px;background:var(--h2-red);color:#fff;text-decoration:none;font:800 15px/1 Raleway,sans-serif;letter-spacing:.01em;text-transform:none}' +
        'html.header-v2 .nav2-links>li.nav2-sheet-cta>a:hover{background:var(--h2-red-hover)}}';
      document.head.appendChild(st);
    }
  });

  window.SITE = SITE;
  window.MENU = MENU;
  window.FOOTER = FOOTER;
})();
