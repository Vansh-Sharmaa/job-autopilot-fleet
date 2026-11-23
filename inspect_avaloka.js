async (page) => {
  const avalokaLink = await page.evaluate(async () => {
    const events = Array.from(document.querySelectorAll('[data-eventid]'));
    for (const ev of events) {
      if (ev.innerText.includes('Avaloka')) {
        ev.click();
        return { clicked: true };
      }
    }
    return { clicked: false };
  });

  await page.waitForTimeout(1500);

  const dialogInfo = await page.evaluate(() => {
    const dialog = document.querySelector('[role="dialog"]') || document.body;
    const text = dialog.innerText;
    const links = Array.from(dialog.querySelectorAll('a')).map(a => ({ text: a.innerText.trim(), href: a.href }));
    return { text: text.slice(0, 500), links };
  });

  return { avalokaLink, dialogInfo };
}
