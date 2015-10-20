'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import sessionStore from '../stores/session';
import bemRouterLink from '../libs/bemRouterLink';
import Reflux from 'reflux';
import accountStore from '../stores/account';
import authUrls from '../stores/authUrls';

require('styles/GettingStarted.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    InfoMessage = bem('info-message'),
    InfoMessage__link = bemRouterLink('info-message__link'),
    BorderedNavlink = bemRouterLink('bordered-navlink');

var GettingStarted = React.createClass({
  mixins: [
    Navigation,
    Reflux.connect(sessionStore, 'session'),
  ],
  componentDidMount () {
    this.listenTo(accountStore, this.accountStoreUpdated);
  },
  accountStoreUpdated ({created}) {
    if (created) {
      this.setState({
        accountCreated: created,
      });
    }
  },
  getInitialState() {
    return {
      accountCreated: accountStore.state.created,
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
            { this.state.accountCreated ?
              <InfoMessage m='account-created'>
                {'You have created an account with the username "' +
                  this.state.accountCreated.username +
                 '". Please '}
                <InfoMessage__link href={authUrls.login} to='login'>
                  log in
                </InfoMessage__link>
                {'.'}
              </InfoMessage>
            : null}
          </ContentBg>
        </Content>
      );
  }
});

module.exports = GettingStarted;
