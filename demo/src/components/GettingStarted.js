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
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    RegisterButton = bem('register-button', '<button>'),
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
          <ContentBg>
            <ContentTitle>Getting Started with EquityTool</ContentTitle>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas faucibus mollis interdum. Nullam quis risus eget urna mollis ornare vel eu leo. Curabitur blandit tempus porttitor. Nullam id dolor id nibh ultricies vehicula ut id elit.</p>
            <RegisterButton onClick={() => this.transitionTo('register')}>
              Create Account
            </RegisterButton>
            <p>
              <span>or </span>
              <Navlink href={'#/login'} m='login'>
                log in here
              </Navlink>
            </p>
            <p>
              <Navlink href={'#/new-project'} m='new-project'>
                new project
              </Navlink>
            </p>
            <p>
              <Navlink href={'#/projects'} m='projects'>
                project list
              </Navlink>
            </p>
          </ContentBg>
        </Content>
      );
  }
});

module.exports = GettingStarted;
