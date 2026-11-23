async (page) => {
  await page.waitForTimeout(3000);
  const title = await page.title();
  const url = page.url();
  
  // Find job items
  const items = await page.$$eval('li[data-occludable-job-id], .jobs-search-results__list-item', els => els.map(el => {
    const t = el.querySelector('a.job-card-list__title--link, a.job-card-container__link, strong');
    const c = el.querySelector('.artdeco-entity-lockup__subtitle, .job-card-container__primary-description');
    return {
      title: t ? t.innerText.trim() : '',
      company: c ? c.innerText.trim() : ''
    };
  }));

  // Check if easy apply button is visible on the current detail pane
  const easyApply = await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Easy Apply'));
    return btn ? btn.innerText.trim() : null;
  });

  return { title, url, count: items.length, sample: items.slice(0, 5), easyApplyOnSelected: easyApply };
}
