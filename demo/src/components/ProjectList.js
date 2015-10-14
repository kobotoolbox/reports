
'use strict';

import React from 'react/addons';
import Reflux from 'reflux';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import moment from 'moment';
import {requireLoggedInMixin} from '../mixins/requireLogins';
import Identicon from '../libs/react-identicon';
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
    ProjectLinks = bem('project__links'),
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
      syncingProject: false,
    };
  },
  componentDidMount () {
    this.listenTo(renderingsStore, this.renderingsStoreChanged);
    actions.listRenderings();
  },
  syncProject (evt) {
    var $ect = evt.currentTarget;
    actions.syncProject($ect.dataset.projectId);
    this.setState({
      syncingProject: $ect.dataset.projectId,
    });
  },
  renderingsStoreChanged (state) {
    this.setState(state);
  },
  render: function () {
    return (
        <Content m='project-list'>
          <ContentBg>
            <ContentTitle>My Projects</ContentTitle>
            <ProjectUl>
              {this.state.projects.length === 0 ?
                <ProjectLi m={'notification'}>
                  {'You have no projects to display. Click "new project" below.'}
                </ProjectLi>
              : null}
              {this.state.projects.map(({name, submission_count, enter_data_link, created, id}) => {
                var dateStr = moment(new Date(created)).fromNow();
                var identiconSeed = `equity-tool-project-${id}`;
                var hasSubmissions = submission_count > 0;
                var isSyncing = this.state.syncingProject === id;
                return (
                    <ProjectLi key={`project-${name}`}>
                      <ProjectAttribute m='image'>
                        <Identicon id={identiconSeed} size={80} />
                      </ProjectAttribute>
                      <ProjectAttribute m='content'>
                        <ProjectAttribute m='name'>
                          {name}
                        </ProjectAttribute>
                        <ProjectLinks>
                          <ProjectAttribute m='submissions'>
                            {submission_count} submissions
                          </ProjectAttribute>
                          <ProjectAttributeLink m='enter-data' href={enter_data_link} target='_blank'>
                            enter data
                          </ProjectAttributeLink>
                          <ProjectAttribute m={{
                            sync: true,
                            syncpending: isSyncing,
                          }} onClick={this.syncProject} data-project-id={id}>
                            <i />
                            sync
                          </ProjectAttribute>
                          {hasSubmissions ?
                            <Navlink m='view-report' to='report' params={{ id: id }}>
                              <i />
                              view report
                            </Navlink>
                          : null}
                        </ProjectLinks>
                      </ProjectAttribute>
                      <ProjectAttribute m='date-created'>
                        {dateStr}
                      </ProjectAttribute>
                    </ProjectLi>
                  );
              })}
            </ProjectUl>
            <BorderedNavlink m='new-project' to='new-project'>
              New Project
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
