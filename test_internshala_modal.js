async (page) => {
  const result = await page.evaluate(() => {
    const btn = document.querySelector('#top_easy_apply_button, #apply_now_button');
    let clicked = false;
    if (btn) {
      btn.click();
      clicked = true;
    }
    return { clicked };
  });

  await page.waitForTimeout(2000);

  const modalInfo = await page.evaluate(() => {
    const modal = document.querySelector('.modal.show, [role="dialog"], .application_form_modal') || document.body;
    const text = modal.innerText.slice(0, 800);
    const buttons = Array.from(modal.querySelectorAll('button, input[type="submit"]')).map(b => (b.innerText || b.value || '').trim()).filter(Boolean);
    const textareas = Array.from(modal.querySelectorAll('textarea')).map(t => ({ id: t.id, name: t.name, placeholder: t.placeholder }));
    return { text, buttons, textareas };
  });

  return { clicked: result.clicked, ...modalInfo };
}
