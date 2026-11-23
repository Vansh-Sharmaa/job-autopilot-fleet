
(() => {
    // Collect all table rows or email entries in Gmail list
    const rows = Array.from(document.querySelectorAll('tr[role="row"], .zA'));
    return rows.map(r => {
        const sender = r.querySelector('.yX, .bA4, .zF, .yP')?.innerText?.trim() || '';
        const subjectEl = r.querySelector('.bog, .bqe');
        const subject = subjectEl?.innerText?.trim() || '';
        const snippet = r.querySelector('.y2')?.innerText?.trim() || '';
        const date = r.querySelector('.xW, .m1, .xY')?.innerText?.trim() || '';
        const linkEl = r.querySelector('a[href*="#search"], a[href*="#inbox"]');
        const link = linkEl ? linkEl.href : window.location.href;
        return { sender, subject, snippet, date, link };
    }).filter(item => item.sender || item.subject);
})()
