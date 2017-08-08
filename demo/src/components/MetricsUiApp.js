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
    LogoutLink = bemRouterLink('account-link');

var MetricsUiApp = React.createClass({
  mixins: [
    Reflux.connect(sessionStore, 'session'),
  ],
  getInitialState () {
    return {
      session: sessionStore.state,
      mobileMenuVisible: false,
    };
  },
  handleClick: function(){
    this.setState({mobileMenuVisible: !this.state.mobileMenuVisible});
  },
  logout () {
    sessionStore.logout();
  },
  render() {
    return (
      <MainWrap>
        <Header>
          <div id="logo-container">
              <a href="https://www.equitytool.org/"><img src="https://www.equitytool.org/wp-content/uploads/2015/08/EquityToolLogoWhiteOnly.png" alt="Equity Tool" /></a>
          </div>
          <div className="mobile-nav">
            <span className="mob-nav-btn" onClick={this.handleClick}>Menu</span>
          </div>
          <nav className={this.state.mobileMenuVisible ? "navigation-container nav-menu visible" : "navigation-container nav-menu not-visible"}>
            <ul id="menu-main" className="menu-ul">
              <li><a href="https://www.equitytool.org/the-equity-tool-2/">The Equity Tool<span class="drop-arrow"></span></a>
                <ul>
                  <li><a href="https://www.equitytool.org/the-equity-tool-2/">Overview</a></li>
                  <li><a href="https://www.equitytool.org/equity-tool-demonstrations/">Equity Tool Demonstrations</a></li>
                  <li><a href="https://www.equitytool.org/countries-covered-by-the-equity-tool/">Countries covered by the Equity Tool</a></li>
                  <li><a href="https://www.equitytool.org/how-to-use-the-equity-tool/">How to use the Equity Tool</a></li>
                  <li><a href="https://www.equitytool.org/background/">Background</a></li>
                </ul>
              </li>
              <li><a href="https://www.equitytool.org/equity/">About Equity<span class="drop-arrow"></span></a>
                <ul>
                  <li><a href="https://www.equitytool.org/equity/">Equity</a></li>
                  <li><a href="https://www.equitytool.org/wealth-quintiles/">Wealth Quintiles</a></li>
                </ul>
              </li>
              <li><a href="https://www.equitytool.org/sampling/">Survey Tips<span class="drop-arrow"></span></a>
                <ul>
                  <li><a href="https://www.equitytool.org/sampling/">Sampling</a></li>
                  <li><a href="https://www.equitytool.org/principles-of-sampling/">Principles of Sampling</a></li>
                  <li><a href="https://www.equitytool.org/preparing-the-data-collection-team/">Preparing the data collection team</a></li>
                  <li><a href="https://www.equitytool.org/practical-preparations-for-your-survey/">Practical preparations for your survey</a></li>
                </ul>
              </li>
              <li><a href="https://www.equitytool.org/contact-us/">Contact Us</a></li>
            </ul>
          </nav>
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
                sign up
              </AccountLink>
            </AccountDetails>
          }
        </Header>
        <RouteHandler />
        <Footer>
          {'Metrics for Management, 2016'}
        </Footer>
      </MainWrap>
    );
  }
});

module.exports = MetricsUiApp;
