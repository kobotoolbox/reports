
'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import moment from 'moment';

require('styles/ProjectList.scss');

let {
  Navigation,
} = require('react-router');

var projects = [
  {name: 'a1', dateCreated: new Date(), submissions: 2, enterDataLink: '1234'},
  {name: 'a2', dateCreated: new Date(), submissions: 3, enterDataLink: '1234'},
  {name: 'a3', dateCreated: new Date(), submissions: 4, enterDataLink: '1234'},
  {name: 'a4', dateCreated: new Date(), submissions: 2, enterDataLink: '1234'},
];

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    Navlink = bemRouterLink('navlink'),
    NewProjectButton = bem('new-project-button', '<button>'),
    ProjectUl = bem('project-list', '<ul>'),
    ProjectLi = bem('project-list__item', '<li>'),
    ProjectAttribute = bem('project__attribute', '<span>'),
    ProjectLinks = bem('project__links'),
    ProjectAttributeLink = bem('project__attribute-link', '<a>');

var ProjectList = React.createClass({
  mixins: [
    Navigation,
  ],
  render: function () {
    return (
        <Content m='project-list'>
          <ContentBg>
            <ContentTitle>My Projects</ContentTitle>
            <ProjectUl>
              {projects.map(function({name, submissions, enterDataLink, dateCreated}){
                var dateStr = moment(dateCreated).fromNow();
                return (
                    <ProjectLi>
                      <ProjectAttribute m='image'>
                        image
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
                            <i class="fa fa-cog"> </i>
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
            <NewProjectButton onClick={() => this.transitionTo('new-project')}>
              New Project
            </NewProjectButton>
          </ContentBg>
        </Content>
      );
  }
});

module.exports = ProjectList;
