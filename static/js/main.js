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

;(function($){

  /**
  * Crate.IO main.js
  */

  var ga = window.ga || function(){ console.warn('GA not enabled'); };

  /**
  * Email input field on download page
  */
  $('input.form-control').on('focus', function(e){
    var control = $(this).parent().parent();
    control.removeClass('has-error');
    $('.text-danger', control).addClass('hide');
  });

  $('form.crate-cli').each(function(idx, elem){
    var term = new Term(elem);
    term.addComment('# Why not start with the following query?');
    term.addComment('# SELECT id, name, hostname FROM sys.nodes;');
    term.addComment('# Execute the examples on the right by clicking into the code box.');
    window.term = term;
  });

  $('pre.tut').each(function(idx, elem) {
    var tname = 'table_' + ($.cookie('uid') || 'foo');
    $(elem).text(elem.textContent.replace('T_NAME', tname));
    hljs.highlightBlock(elem);
    $(elem).tooltip({'title':'Click to execute query!', 'placement':'top'});
  });

  $('pre.tut').on('click', function(e){
    window.term.exec(this.textContent);
  });


  $('form#form-download').on('submit', function(e){
    var url = $(this).data('url');
    e.preventDefault();


    if (url) {
      ga('send', 'event', 'button', 'click', 'download_download', 1);
      window.open(url, '_blank');
      this.reset();
    }
  });

}(jQuery));
