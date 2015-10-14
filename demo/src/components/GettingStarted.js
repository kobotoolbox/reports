'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import sessionStore from '../stores/session';
import bemRouterLink from '../libs/bemRouterLink';
import Reflux from 'reflux';
import authUrls from '../stores/authUrls';

require('styles/GettingStarted.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    BorderedNavlink = bemRouterLink('bordered-navlink');

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
            { this.state.session.loggedIn ?
              <div>
                <p>
                  <BorderedNavlink m='new-project' to='new-project'>
                    new project
                  </BorderedNavlink>
                  <span> or </span>
                  <BorderedNavlink m='projects' to='project-list'>
                    project list
                  </BorderedNavlink>
                </p>
              </div>
            :
              <div>
                <BorderedNavlink href={authUrls.register} m='register'>
                  Create Account
                </BorderedNavlink>
                <span> or </span>
                <BorderedNavlink href={authUrls.login} to='login'>
                  log in here
                </BorderedNavlink>
              </div>
            }
          </ContentBg>
        </Content>
      );
  }
});

module.exports = GettingStarted;
