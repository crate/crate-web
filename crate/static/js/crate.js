var Term = function(elem){

  var prefix = "cr>";
  var pfLen = prefix.length +1;

  var _form = elem;
  var form = $(elem);
  var settings = form.data();

  var history = $('pre', elem);
  var prompt = $('input', elem);

  var addComment = function(text) {
    history.append('<div class="text-muted"><i>' + text + '</i></div>');
  };

  var addErrorResponse = function(text) {
    history.append('<div class="text-danger"><b>' + text + '</b></div>');
  };

  var addSQLResponse = function(res) {
    if (res.cols.length == 0) return;
    var t = new AsciiTable();
    t.setHeading.apply(t, res.cols);
    for (var r = 0; r < res.rows.length; r++) {
      var row = res.rows[r].map(function(e){ return typeof e === 'object' ? JSON.stringify(e) : e; });
      t.addRow.apply(t, row);
    }
    history.append('<div class="txt-sql">' + t.toString() + '</div>');
  };

  var addRequest = function(stmt) {
    var span = document.createElement('span');
    var sql = document.createTextNode(stmt);
    span.appendChild(sql);
    hljs.highlightBlock(span);
    history.append('<div class="text-muted">' + prefix + ' ' + span.innerHTML + '</div>');
  };

  var execute = function(stmt) {
    addRequest(stmt);
    $.ajax({
      type: 'POST',
      url: settings.host + '/_sql',
      headers: {
        'Accept': 'application/json',
        'Origin': 'play.crate.io'
      },
      data: JSON.stringify({"stmt": stmt.replace(/;+$/, ''), "args": []})
    }).done(function(response){
      var duration = parseFloat(response.duration) / 1000.0;
      addSQLResponse(response);
      addComment('OK ('+ duration +'s)');
    }).fail(function(req){
      if (req.responseJSON) {
        addErrorResponse(req.responseJSON.error.message);
      } else if (req.statusText) {
        addErrorResponse(req.statusText);
      }
    }).always(function(e){
      history[0].scrollTop = history[0].scrollHeight;
      _form.reset();
    });
  };

  prompt.focus();
  prompt[0].value = prefix + ' ';
  prompt[0].setSelectionRange(pfLen, pfLen);
  prompt.on('keyup', function(e){
    var len = e.target.value.length;
    if (len < pfLen) e.target.value = prefix + " ";
    if (e.target.selectionStart < pfLen) {
      e.target.setSelectionRange(pfLen, pfLen);
    }
  });

  form.on('submit', function(e){
    e.preventDefault();
    var stmt = e.target.input.value.substr(prefix.length+1);
    execute(stmt);
    return false;
  });

  // Public API
  this.addComment = addComment;
  this.exec = function(stmt){
    $('html, body').animate({
      scrollTop: Math.max(form.offset().top - 110)
    }, 1000);
    execute(stmt);
  };
};
