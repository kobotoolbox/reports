'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import sessionStore from '../stores/session';
import authUrls from '../stores/authUrls';
import Reflux from 'reflux';

let {
  RouteHandler,
} = require('react-router');

// CSS
require('normalize.css');
require('../styles/main.scss');
require('../styles/MetricsUI.scss');


var MainWrap = bem('main-wrap'),
    Header = bem('header', '<header>'),
    Footer = bem('footer', '<footer>'),
    AccountDetails = bem('account-details'),
    AccountDetail = bem('account-detail', '<span>'),
    AccountLink = bemRouterLink('account-link'),
    LogoutLink = bemRouterLink('account-link'),
    Logo = bem('logo', '<span>');

var MetricsUiApp = React.createClass({
  mixins: [
    Reflux.connect(sessionStore, 'session'),
  ],
  getInitialState () {
    return {
      session: sessionStore.state,
    };
  },
  logout () {
    sessionStore.logout();
  },
  render() {
    return (
      <MainWrap>
        <Header>
          <Logo />
          { this.state.session.loggedIn ?
            <AccountDetails>
              <AccountDetail>
                Welcome
                <code>{this.state.session.username}</code>
              </AccountDetail>
              <LogoutLink m='logout' href={authUrls.logout}>
                log out
              </LogoutLink>
            </AccountDetails>
          :
            <AccountDetails>
              <AccountLink m='login' href={authUrls.login}>
                login
              </AccountLink>
              <AccountLink m='register' href={authUrls.register}>
                register
              </AccountLink>
            </AccountDetails>
          }
        </Header>
        <RouteHandler />
        <Footer>
          {'Metrics for Management, 2015'}
        </Footer>
      </MainWrap>
    );
  }
});

module.exports = MetricsUiApp;
