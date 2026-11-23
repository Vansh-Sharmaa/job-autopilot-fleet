async (page) => {
  await page.evaluate(() => {
    const next = document.querySelector('.YhQJj');
    if (next) next.click();
  });
  await page.waitForTimeout(2500);
  const text = await page.evaluate(() => document.body.innerText);
  return { text: text.slice(0, 1500) };
}
