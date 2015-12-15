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
    ContentWrap = bem('content-wrap'),
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
            { this.state.session.loggedIn ?
              <ContentWrap>
                <ContentTitle>EquityTool Surveys</ContentTitle>
                <p>Create a new survey or a view a list of your current surveys.</p>
                <p>For more information about how to use the tool, click <a href="http://www.equitytool.org/how-to-use-the-equity-tool/">here</a>.</p>
                <div>
                  <p>
                    <BorderedNavlink m='new-project' to='new-project'>
                      New survey
                    </BorderedNavlink>
                    <span> or </span>
                    <BorderedNavlink m='projects' to='project-list'>
                      Survey list
                    </BorderedNavlink>
                  </p>
                </div>
              </ContentWrap>
            :
            <ContentWrap>
              <ContentTitle>Getting Started with the EquityTool</ContentTitle>
              <p>Create a free account to begin measuring the wealth distribution of your program beneficiaries. After registration, you will immediately be able to log in to the EquityTool to set up a survey, and begin collecting data.</p>
              <p>For more information about how to use the tool, click <a href="http://www.equitytool.org/how-to-use-the-equity-tool/">here</a>.</p>
              <div className='getting-started__buttons'>
                <BorderedNavlink href={authUrls.register} m='register'>
                  Create account
                </BorderedNavlink>
                <span> or </span>
                <BorderedNavlink href={authUrls.login} to='login'>
                  Log in
                </BorderedNavlink>
              </div>
            </ContentWrap>
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
