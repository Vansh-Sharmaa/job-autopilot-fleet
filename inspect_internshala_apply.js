async (page) => {
  await page.waitForTimeout(2000);
  const info = await page.evaluate(() => {
    const applyBtn = document.querySelector('#apply_now_button, .apply_now_button, button.btn-primary');
    const alreadyApplied = document.body.innerText.includes('You have already applied');
    return {
      title: document.title,
      applyBtnText: applyBtn ? applyBtn.innerText.trim() : null,
      applyBtnId: applyBtn ? applyBtn.id : null,
      alreadyApplied
    };
  });
  return info;
}
