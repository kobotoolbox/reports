'use strict';

// import MetricsUiApp from './MetricsUiApp';
// import GettingStarted from './GettingStarted';
// import ProjectList from './ProjectList';
// import NewProject from './NewProject';
import Register from './Register';
// import Terms from './Terms';
import React from 'react';
import ReactDOM from 'react-dom'
// import Report from './Report';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from 'react-router-dom';

var content = document.getElementById('content');

// var Routes = (
//   <Route handler={MetricsUiApp} path="/">
//     <DefaultRoute handler={GettingStarted} />
//     <Route name="getting-started" path="/getting-started" handler={GettingStarted}/>
//     <Route name="login" path="/login" handler={Login}/>
//     <Route name="register" path="/register" handler={Register}/>
//     <Route name="new-project" path="/new-project" handler={NewProject}/>
//     <Route name="project-list" path="/projects" handler={ProjectList}/>
//     <Route name="report" path="/report/:id" handler={Report}/>
//     <Route name="terms" path="/terms" handler={Terms}/>
//   </Route>
// );

// Router.run(Routes, function (Handler) {
//   React.render(<Handler/>, content);
// });

function App() {
  return (
    <Router>
      <Switch>
        {/* <Route exact path="/">          <MetricsUiApp/>   </Route> */}
        <Route exact path="/">          <Register/>   </Route>
        {/* <Route path="/getting-started"> <GettingStarted/> </Route>
        <Route path="/register">        <Register/>       </Route>
        <Route path="/new-project">     <NewProject/>     </Route>
        <Route path="/project-list">    <ProjectList/>    </Route>
        <Route path="/report/:id">      <Report/>         </Route>
        <Route path="/terms">           <Terms/>          </Route> */}
      </Switch>
    </Router>
  )
}

ReactDOM.render(
  <App />,
  document.getElementById('content')
)