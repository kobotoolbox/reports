'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';

require('styles/NewProject.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    Navlink = bem('navlink', '<a>');

var NewProject = React.createClass({
  mixins: [
    Navigation,
  ],
  render: function () {
    return (
        <Content m='new-project'>
          <p>Content for NewProject</p>
          {/*
            input fields go here
          */}
          <Navlink href={'#/project-list'} m='project-list'>
            Project List
          </Navlink>
        </Content>
      );
  }
});

module.exports = NewProject;
