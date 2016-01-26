/*!
 * Licensed to Crate (https://crate.io) under one or more contributor
 * license agreements.  See the NOTICE file distributed with this work for
 * additional information regarding copyright ownership.  Crate licenses
 * this file to you under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.  You may
 * obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
 * License for the specific language governing permissions and limitations
 * under the License.
 *
 * However, if you have executed another commercial license agreement
 * with Crate these terms will supersede the license and you may use the
 * software solely pursuant to the terms of the relevant commercial agreement.
 */

var Term = function(elem){

  var prefix = "cr>";
  var statement = "";
  var pfLen = prefix.length + statement.length + 1;

  var _form = elem;
  var form = $(elem);
  var settings = form.data();

  var history = $('pre', elem);
  var prompt = $('textarea', elem);

  var setStatement = function(text) {
    statement = text;
    pfLen = prefix.length + statement.length + 1;
    prompt.val(prefix + ' ' + text);
    prompt[0].setSelectionRange(pfLen, pfLen);
    prompt.focus();
  };

  var addComment = function(text) {
    history.append('<div class="text-muted text-comment"><i>' + text + '</i></div>');
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
        'Content-Type': 'application/json',
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

  var resize = function(elem) {
    elem.style.height = 0;
    elem.style.height = elem.scrollHeight + 'px';
  };

  prompt.on('focus', function(e){
    resize(e.target);
  });

  prompt.on('keyup', function(e){
    resize(e.target);
    var len = e.target.value.length;
    if (len < pfLen) e.target.value = prefix + " ";
    if (e.target.selectionStart < pfLen) {
      e.target.setSelectionRange(pfLen, pfLen);
    }
    if (e.keyCode === 13) {
      form.submit();
    }
  });

  form.on('submit', function(e){
    e.preventDefault();
    var stmt = e.target.stmt.value.substr(prefix.length+1);
    console.info('EXECUTE:', stmt);
    execute(stmt);
    return false;
  });


  // Public API
  this.setStatement = setStatement;
  this.addComment = addComment;
  this.exec = function(stmt){
    $('html, body').animate({
      scrollTop: Math.max(form.offset().top - 110)
    }, 1000);
    execute(stmt);
  };
};
