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
    ctaHref: p + 'contact.html'
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
    { label: 'Careers', href: p + 'join-our-team.html' },
    { label: 'Become a REALTOR&reg;', href: p + 'become-a-realtor.html' },
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
        ['Careers', p + 'join-our-team.html'],
        ['Become a REALTOR&reg;', p + 'become-a-realtor.html'],
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

  window.SITE = SITE;
  window.MENU = MENU;
  window.FOOTER = FOOTER;
})();
