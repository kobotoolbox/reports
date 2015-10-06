
'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import moment from 'moment';
import {requireLoggedInMixin} from '../mixins/requireLogins';
import Identicon from '../libs/react-identicon';
import actions from '../actions/actions';
import renderingsStore from '../stores/renderings';

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
  ],
  getInitialState () {
    return {
      projects: [],
    };
  },
  componentDidMount () {
    this.listenTo(renderingsStore, this.renderingsStoreChanged);
    actions.listRenderings();
  },
  renderingsStoreChanged (state) {
    this.setState({
      projects: state.projects,
    });
  },
  render: function () {
    return (
        <Content m='project-list'>
          <ContentBg>
            <ContentTitle>My Projects</ContentTitle>
            <ProjectUl>
              {this.state.projects.map(function({name, submissions, enterDataLink, dateCreated}){
                var dateStr = moment(dateCreated).fromNow();
                var identiconSeed = `equity-tool-project-${name}`;
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
                            {submissions} submissions
                          </ProjectAttribute>
                          <ProjectAttributeLink m='enter-data' href={enterDataLink}>
                            enter data
                          </ProjectAttributeLink>
                          <Navlink m='view-report' to='report' params={{ id: 'aBcXyZ' }}>
                            <i className="fa fa-cog" />
                            view report
                          </Navlink>
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
