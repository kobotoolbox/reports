
'use strict';

import React from 'react/addons';
import Reflux from 'reflux';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import moment from 'moment';
import {requireLoggedInMixin} from '../mixins/requireLogins';
import actions from '../actions/actions';
import {renderingsStore} from '../stores/renderings';

require('styles/ProjectList.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    Navlink = bemRouterLink('navlink'),
    BorderedNavlink = bemRouterLink('bordered-navlink'),
    ProjectUl = bem('project-list', '<ul>'),
    ProjectLi = bem('project-list__item', '<li>'),
    ProjectAttribute = bem('project__attribute', '<span>'),
    ProjectAttributeLink = bem('project__attribute-link', '<a>');

var ProjectList = React.createClass({
  mixins: [
    Navigation,
    requireLoggedInMixin({failTo: 'getting-started'}),
    Reflux.ListenerMixin,
  ],
  getInitialState () {
    return {
      projects: [],
      projectsLoading: true,
      syncingProject: false,
    };
  },
  componentDidMount () {
    this.listenTo(renderingsStore, this.renderingsStoreChanged);
    actions.listRenderings();
  },
  syncProject (evt) {
    var $ect = evt.currentTarget;
    this.setState({
      syncingProject: parseInt($ect.dataset.projectId),
    });
    actions.syncProject($ect.dataset.projectId);
  },
  renderingsStoreChanged (state) {
    this.setState(state);
  },
  render: function () {
    // var projects = [
    //   {name: 'a1', created: new Date(), submission_count: 2, enter_data_link: '1234', id: 1},
    //   {name: 'a2', created: new Date(), submission_count: 3, enter_data_link: '1234', id: 2},
    //   {name: 'a3', created: new Date(), submission_count: 4, enter_data_link: '1234', id: 3},
    //   {name: 'a4', created: new Date(), submission_count: 0, enter_data_link: '1234', id: 4},
    // ];

    return (
        <Content m='project-list'>
          <ContentBg>
            <ContentTitle>My Surveys</ContentTitle>
            <p>This page contains a list of your survey projects. Each survey is assigned a unique URL that can be used by multiple data collectors at the same time. Simply copy the link and send it to your data collectors. Remember, surveys can be conducted online or offline. Before viewing a report, be sure to click "sync" to update all data collected and to see the most up-to-date results. </p>
            <p>Each survey shows the number of submissions, or surveys with complete data uploaded to the project. Click on the "sync" button to update data collected across all survey enumerators. Under "View report" select how you would like to view your survey results: in your browser, as a PDF or as a Word document.</p>
            <p>For more information about how to use the tool, click <a href="http://www.equitytool.org/how-to-use-the-equity-tool/">here</a>.</p>
            <ProjectUl>
              {this.state.projects.length === 0 ?
                <ProjectLi m={this.state.projectsLoading ? 'loadingmessage' : 'notification'}>
                  <i />
                  {this.state.projectsLoading ?
                    'Loading survey list'
                  :
                    'You have no surveys to display. Click "new survey" below.'
                  }
                </ProjectLi>
              : null}
              {this.state.projects.map(({name, submission_count, enter_data_link, created, id}) => {
                var dateStr = moment(new Date(created)).fromNow();
                var hasSubmissions = submission_count > 0;
                var isSyncing = this.state.syncingProject !== false && this.state.syncingProject === id;
                return (
                    <ProjectLi key={`project-${name}`}>
                      <ProjectAttribute m='name'>
                        {name}
                      </ProjectAttribute>
                      <ProjectAttribute m='date-created'>
                        {dateStr}
                      </ProjectAttribute>
                      <ProjectAttribute m='content'>
                        <ProjectAttribute m='data-collections'>
                          <label>Data collection link: </label>
                          <ProjectAttributeLink m='enter-data' href={enter_data_link} target='_blank'>
                            enter data
                          </ProjectAttributeLink>
                        </ProjectAttribute>
                        <ProjectAttribute m='submissions'>
                          <label>{submission_count} submissions</label>
                          <ProjectAttribute m={{
                            sync: true,
                            syncpending: isSyncing,
                          }} onClick={this.syncProject} data-project-id={id}>
                            <i />
                            sync
                          </ProjectAttribute>
                        </ProjectAttribute>
                        {hasSubmissions ?
                          <ProjectAttribute m='view-report'>
                            <label>View report:</label>
                              <Navlink m='view-report' to='report' params={{ id: id }}>
                                view report
                              </Navlink>
                              <ProjectAttributeLink m='enter-data' href={'/rendering/' + id + '.pdf'}>
                                PDF
                              </ProjectAttributeLink>
                              <ProjectAttributeLink m='enter-data' href={'/rendering/' + id + '.docx'}>
                                DOC
                              </ProjectAttributeLink>
                          </ProjectAttribute>
                        : null}
                      </ProjectAttribute>
                    </ProjectLi>
                  );
              })}
            </ProjectUl>
            <BorderedNavlink m='new-project' to='new-project'>
              New survey
            </BorderedNavlink>
            <span> or </span>
            <BorderedNavlink m='back' to='getting-started'>
              Back
            </BorderedNavlink>
          </ContentBg>
        </Content>
      );
  }
});

module.exports = ProjectList;
