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
        <Switch>
          <Route path="/getting-started"> <GettingStarted/> </Route>
          <Route path="/register">        <Register/>       </Route>
          <Route path="/new-project">     <NewProject/>     </Route>
          <Route path="/project-list">    <ProjectList/>    </Route>
          <Route path="/report/:id" component={Report} /> {/* to get access to this.props.match.params.id */}
          <Route path="/terms">           <Terms/>          </Route>
          <Route>{/* default */}          <GettingStarted/> </Route>
          }
        </Switch>
      </MetricsUiApp>
    </Route>
  </HashRouter>,
  content
)

// https://github.com/reactjs/react-modal/blob/master/docs/accessibility/index.md#app-element
Modal.setAppElement(content);
