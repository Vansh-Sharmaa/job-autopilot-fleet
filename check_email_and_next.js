async (page) => {
  await page.evaluate(() => {
    // Find checkbox for email record
    const cb = document.querySelector('[role="checkbox"]');
    if (cb && cb.getAttribute('aria-checked') !== 'true') {
      cb.click();
    }
  });

  await page.waitForTimeout(500);

  // Click Next
  await page.evaluate(() => {
    const nextBtn = document.querySelector('.YhQJj');
    if (nextBtn) nextBtn.click();
  });

  await page.waitForTimeout(2500);

  const page2Text = await page.evaluate(() => document.body.innerText);
  return { page2Text: page2Text.slice(0, 1500) };
}
