import Reflux from 'reflux';
import $ from 'jquery';
import assign from 'react/lib/Object.assign';

var token = (function(){
  var _m = document.head.querySelector('meta[name=csrf-token]');
  return _m && _m.content || '';
})();

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
      url: '/equitytool/create',
      dataType: 'json',
      method: 'POST',
      data: postData,
    });
  };
  this.confirmLogin = () => {
    return $.getJSON(rootUrl + '/me/');
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

actions.createTemplate.listen(function (templateData) {
  dataInterface.createTemplate(templateData)
    .done(actions.createTemplate.completed)
    .fail(actions.createTemplate.failed);
});

actions.listRenderings.listen(function () {
  dataInterface.listRenderings()
    .done(actions.listRenderings.completed)
    .fail(actions.listRenderings.failed);
});

actions.confirmLogin.listen(function() {
  dataInterface.confirmLogin().done(function(data) {
    actions.confirmLogin.completed(data);
  }).fail(function(data) {
    actions.confirmLogin.failed(data);
  });
});

export default actions;
