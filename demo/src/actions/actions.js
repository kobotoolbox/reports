import Reflux from 'reflux';
import $ from 'jquery';
import assign from 'react/lib/Object.assign';

var token = '';

var dataInterface = (function(){
  var rootUrl = '';
  this.listRenderings = ()=> {
    return $.getJSON(rootUrl + '/renderings/');
  };

  this.syncRendering = (renderingId) => {
    return $.getJSON(rootUrl + '/renderings/' + renderingId);
  };

  this.createTemplate = (templateData) => {
    var postData = assign({csrfmiddlewaretoken: token}, templateData);
    return $.ajax({
      dataType: 'json',
      method: 'POST',
      data: postData,
    });
  };

  return this;
}).call({});

var actions = Reflux.createActions({
/*
  register: {
    asyncResult: true,
    children: [],
  },
  login: {
    asyncResult: true,
  },
  generateRendering: {
    asyncResult: true,
  },
*/
  createTemplate: {
    asyncResults: true,
  },
  listRenderings: {
    asyncResult: true,
  },
  confirmLogin: {
    asyncResult: true,
  },
  placeholder: {
    asyncResult: true,
  },
});

actions.placeholder.listen(function(desc){
  console.log(`placeholder action called: '${desc}'`);
});

actions.confirmLogin.listen(function() {
  dataInterface.confirmLogin().done(function(data) {
    actions.confirmLogin.completed(data);
  }).fail(function(data) {
    actions.confirmLogin.failed(data);
  });
});

export default actions;
