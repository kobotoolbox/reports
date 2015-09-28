
'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';

require('styles/Login.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    Navlink = bem('navlink', '<a>');

var Login = React.createClass({
  mixins: [
    Navigation,
  ],
  render: function () {
    return (
        <Content m='login'>
          <p>Content for Login</p>
          <Navlink href={'#/new-project'} m='new-project'>
            New Project
          </Navlink>
        </Content>
      );
  }
});

module.exports = Login;
