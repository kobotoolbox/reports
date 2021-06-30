'use strict';

import MetricsUiApp from './MetricsUiApp';
import GettingStarted from './GettingStarted';
import ProjectList from './ProjectList';
import NewProject from './NewProject';
import Register from './Register';
import Terms from './Terms';
import React from 'react';
import ReactDOM from 'react-dom'
import Report from './Report';
import {
  HashRouter,
  Switch,
  Route
} from 'react-router-dom';
import Modal from 'react-modal';

var content = document.getElementById('content');

ReactDOM.render(
  <HashRouter>
    <Route path="/">
      <MetricsUiApp>
        <Switch> {/* stops after the first match */}
          <Route path="/getting-started" component={GettingStarted} />
          <Route path="/register"        component={Register} />
          <Route path="/new-project"     component={NewProject} />
          <Route path="/project-list"    component={ProjectList} />
          {/* id available in the component as this.props.match.params.id */}
          <Route path="/report/:id"      component={Report} />
          <Route path="/terms"           component={Terms} />
          {/* omitting the path matches everything, i.e. makes the route the default */}
          <Route component={GettingStarted} />
        </Switch>
      </MetricsUiApp>
    </Route>
  </HashRouter>,
  content
)

// https://github.com/reactjs/react-modal/blob/master/docs/accessibility/index.md#app-element
Modal.setAppElement(content);
