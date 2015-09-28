'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import sessionStore from '../stores/session';
import Reflux from 'reflux';

require('styles/GettingStarted.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    Navlink = bem('navlink', '<a>');

var GettingStarted = React.createClass({
  mixins: [
    Navigation,
    Reflux.connect(sessionStore, 'session'),
  ],
  getInitialState() {
    return {
      session: sessionStore.state,
    };
  },
  render: function () {
    return (
        <Content m='getting-started'>
          <p>Content for GettingStarted</p>
          <Navlink href={'#/login'} m='login'>
            Login
          </Navlink>
        </Content>
      );
  }
});

module.exports = GettingStarted;
