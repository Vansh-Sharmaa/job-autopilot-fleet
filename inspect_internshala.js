async (page) => {
  await page.waitForTimeout(2000);
  const jobs = await page.$$eval('.individual_internship', els => els.map(el => {
    const titleEl = el.querySelector('.job-internship-name, .heading_4_5');
    const compEl = el.querySelector('.company-name, .link_display_like_text');
    const locEl = el.querySelector('.row-1-item.locations, .locations');
    const ctcEl = el.querySelector('.salary, .stipend');
    const linkEl = el.querySelector('a.view_detail_button');
    return {
      title: titleEl ? titleEl.innerText.trim() : '',
      company: compEl ? compEl.innerText.trim() : '',
      location: locEl ? locEl.innerText.trim() : '',
      ctc: ctcEl ? ctcEl.innerText.trim() : '',
      link: linkEl ? linkEl.href : ''
    };
  }));

  return { count: jobs.length, sample: jobs.slice(0, 5) };
}
