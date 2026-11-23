async (page) => {
  const nextInfo = await page.evaluate(() => {
    const nextBtn = Array.from(document.querySelectorAll('span, button')).find(el => (el.innerText || '').trim() === 'Next');
    if (nextBtn) {
      nextBtn.click();
      return { clicked: true };
    }
    return { clicked: false };
  });

  await page.waitForTimeout(2000);

  const page2Text = await page.evaluate(() => {
    return document.body.innerText.slice(0, 1500);
  });

  return { nextInfo, page2Text };
}
