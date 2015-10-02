'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import sessionStore from '../stores/session';
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
    AccountButton = bem('account-button', '<button>'),
    AccountLink = bemRouterLink('account-link'),
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
                <code>{this.state.session.fullName}</code>
              </AccountDetail>
              <AccountButton onClick={this.logout}>
                Log out
              </AccountButton>
            </AccountDetails>
          :
            <AccountDetails>
              <AccountLink m='login' to='login'>
                login
              </AccountLink>
              <AccountLink m='register' to='register'>
                register
              </AccountLink>
            </AccountDetails>
          }
        </Header>
        <RouteHandler />
        <Footer>
          {'footer attribution, etc.'}
        </Footer>
      </MainWrap>
    );
  }
});

module.exports = MetricsUiApp;
