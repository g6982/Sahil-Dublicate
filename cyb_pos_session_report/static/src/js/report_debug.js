(function(){
    let dt = new Date();
    dt = dt.getMinutes() + '-' + dt.getSeconds();
    let scripts = `
    <script type="text/javascript" defer src="/cyb_pos_session_report/static/src/js/report.js?v=${dt}"></script>
    `;
    console.log('deferred');
    document.write(scripts);
})();