'use strict';

var MetricsUiApp = require('./MetricsUiApp');
var GettingStarted = require('./GettingStarted');
var ProjectList = require('./ProjectList');
var NewProject = require('./NewProject');
var Login = require('./Login');
var Register = require('./Register');
var React = require('react');
import Report from './Report';
import Router from 'react-router';

let {
  DefaultRoute,
  Route,
} = Router;

var content = document.getElementById('content');

var Routes = (
  <Route handler={MetricsUiApp} path="/">
    <DefaultRoute handler={GettingStarted} />
    <Route name="getting-started" path="/getting-started" handler={GettingStarted}/>
    <Route name="login" path="/login" handler={Login}/>
    <Route name="register" path="/register" handler={Register}/>
    <Route name="new-project" path="/new-project" handler={NewProject}/>
    <Route name="project-list" path="/projects" handler={ProjectList}/>
    <Route name="report" path="/report/:id" handler={Report}/>
  </Route>
);

Router.run(Routes, function (Handler) {
  React.render(<Handler/>, content);
});
