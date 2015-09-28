
'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';

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
    Navlink = bem('navlink', '<a>'),
    ProjectUl = bem('project-list', '<ul>'),
    ProjectLi = bem('project-list__item', '<li>'),
    ProjectAttribute = bem('project__attribute', '<span>'),
    ProjectAttributeLink = bem('project__attribute-link', '<a>');

var ProjectList = React.createClass({
  mixins: [
    Navigation,
  ],
  render: function () {
    return (
        <Content m='project-list'>
          <ProjectUl>
            {projects.map(function({name, submissions, enterDataLink, dateCreated}){
              return (
                  <ProjectLi>
                    <ProjectAttribute m='name'>
                      {name}
                    </ProjectAttribute>
                    <ProjectAttribute m='date-created'>
                      {dateCreated}
                    </ProjectAttribute>
                    <ProjectAttribute m='submissions'>
                      {submissions}
                    </ProjectAttribute>
                    <ProjectAttributeLink m='enter-data' href={enterDataLink}>
                      enter data
                    </ProjectAttributeLink>
                  </ProjectLi>
                );
            })}
          </ProjectUl>
          <Navlink m={'new-project'} href={'#/new-project'}>
            {'new project'}
          </Navlink>
        </Content>
      );
  }
});

module.exports = ProjectList;
