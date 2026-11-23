async (page) => {
  const jobInfo = await page.evaluate(() => {
    const card = document.querySelector('.individual_internship');
    if (!card) return null;
    return {
      id: card.id,
      html: card.innerHTML.slice(0, 500),
      links: Array.from(card.querySelectorAll('a')).map(a => ({ text: a.innerText.trim(), href: a.href }))
    };
  });
  return jobInfo;
}
