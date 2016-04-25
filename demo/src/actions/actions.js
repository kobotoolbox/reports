import Reflux from 'reflux';
import $ from 'jquery';
import assign from 'react/lib/Object.assign';
import alertify from 'alertifyjs';

require('../styles/libs/alertify.scss');

var token = (function(){
  var _m = document.head.querySelector('meta[name=csrf-token]');
  return _m && _m.content || '';
})();

var dataInterface = (function(){
  var rootUrl = '';
  this.listRenderings = ()=> {
    return $.getJSON(rootUrl + '/renderings/');
  };

  /*
  this.syncRendering = (renderingId) => {
    return $.getJSON(rootUrl + '/renderings/' + renderingId);
  };
  */

  this.createTemplate = (templateData) => {
    var postData = assign({csrfmiddlewaretoken: token}, templateData);
    return $.ajax({
      url: '/equitytool/create_friendly',
      dataType: 'json',
      method: 'POST',
      data: postData,
    });
  };
  this.confirmLogin = () => {
    return $.getJSON(rootUrl + '/me/');
  };
  this.syncProject = (projectId) => {
    return $.ajax({
      url: `${rootUrl}/equitytool/sync/${projectId}`,
    });
  };
  this.getFormBuilderAccess = (projectId) => {
    return $.ajax({
      url: `${rootUrl}/renderings/${projectId}/one_time_form_builder_access/`,
    });
  };
  this.getRendering = (projectId) => {
    return $.ajax({
      url: `${rootUrl}/rendering/${projectId}.html`
    });
  };

  this.registerAccount = (accountData) => {
    var postData = assign({csrfmiddlewaretoken: token}, accountData);
    return $.ajax({
      url: '/register/',
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
    asyncResult: true,
  },
  registerAccount: {
    asyncResult: true,
  },
  getRendering: {
    asyncResult: true,
  },
  listRenderings: {
    asyncResult: true,
  },
  confirmLogin: {
    asyncResult: true,
  },
  syncProject: {
    asyncResult: true,
  },
  getFormBuilderAccess: {
    asyncResult: true,
  },
  placeholder: {
    asyncResult: true,
  },
});

actions.placeholder.listen(function(desc){
  console.log(`placeholder action called: '${desc}'`);
});

actions.registerAccount.listen(function (accountData) {
  // window.setTimeout((() => {
  //   actions.registerAccount.failed({
  //     username: [
  //       "this field must be unique"
  //     ]
  //   });
  // }), 2000);
  dataInterface.registerAccount(accountData)
    .done(actions.registerAccount.completed)
    .fail(actions.registerAccount.failed);
});

actions.registerAccount.completed.listen(function() {
  alertify.success('Registration successful!');
});
actions.registerAccount.failed.listen(function() {
  alertify.warning('Registration failed!');
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
  dataInterface.confirmLogin()
    .done(actions.confirmLogin.completed)
    .fail(actions.confirmLogin.failed);
});

actions.syncProject.listen(function (projectId) {
  dataInterface.syncProject(projectId)
    .done(actions.syncProject.completed)
    .fail(actions.syncProject.failed);
});

actions.syncProject.completed.listen(function() {
  actions.listRenderings();
});

actions.getFormBuilderAccess.listen(function (projectId) {
  dataInterface.getFormBuilderAccess(projectId)
    .done(actions.getFormBuilderAccess.completed)
    .fail(actions.getFormBuilderAccess.failed);
});

actions.getRendering.listen(function (projId) {
  dataInterface.getRendering(projId)
    .done(function(html){
      actions.getRendering.completed(projId, html);
    })
    .fail(actions.getRendering.failed);
});


export default actions;
