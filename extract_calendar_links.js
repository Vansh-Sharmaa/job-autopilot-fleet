async (page) => {
  const eventDetails = [];
  
  // Find event elements
  const eventSelectors = await page.evaluate(() => {
    const els = Array.from(document.querySelectorAll('[data-eventid]'));
    return els.map((el, i) => ({ index: i, eventId: el.getAttribute('data-eventid'), text: el.innerText.trim() }));
  });

  for (const ev of eventSelectors) {
    // Click event element
    await page.evaluate((id) => {
      const el = document.querySelector(`[data-eventid="${id}"]`);
      if (el) el.click();
    }, ev.eventId);

    await page.waitForTimeout(1500);

    // Extract details from the event popover dialog
    const details = await page.evaluate(() => {
      const dialog = document.querySelector('[role="dialog"], .kO001e, .I5Wmee') || document.body;
      const title = dialog.querySelector('[role="heading"], h2, span[id*="title"]')?.innerText.trim() || '';
      const text = dialog.innerText;
      const links = Array.from(dialog.querySelectorAll('a')).map(a => ({ text: a.innerText.trim(), href: a.href })).filter(l => l.href && !l.href.includes('calendar.google.com') && !l.href.includes('accounts.google.com'));
      
      // Close popover with Escape or close button
      const closeBtn = dialog.querySelector('button[aria-label*="Close"], button[aria-label*="Schließen"]');
      if (closeBtn) closeBtn.click();
      
      return { title, text: text.slice(0, 800), links };
    });

    eventDetails.push(details);
    await page.keyboard.press('Escape');
    await page.waitForTimeout(500);
  }

  return { events: eventDetails };
}
