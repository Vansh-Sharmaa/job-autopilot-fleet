async (page) => {
  await page.waitForTimeout(3000);
  const info = await page.evaluate(() => {
    // Check active google account email
    const accountEl = document.querySelector('a[aria-label*="Google Account"], a[aria-label*="Google-Konto"]');
    const accountLabel = accountEl ? accountEl.getAttribute('aria-label') : '';

    // Check calendar events
    const eventEls = Array.from(document.querySelectorAll('[data-eventid], [role="button"][data-keyboard-focusable="true"], .jPtWwb, .NlLKec'));
    const events = eventEls.map(el => {
      return {
        text: el.innerText.trim(),
        aria: el.getAttribute('aria-label') || ''
      };
    }).filter(e => e.text || e.aria);

    // Also look for any link or text with http/https
    const bodyText = document.body.innerText;
    const links = Array.from(document.querySelectorAll('a')).map(a => a.href).filter(h => h.includes('http') && !h.includes('google.com'));

    return {
      accountLabel,
      eventsCount: events.length,
      events: events.slice(0, 20),
      externalLinks: links
    };
  });
  return info;
}
