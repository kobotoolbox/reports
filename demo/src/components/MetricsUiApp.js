'use strict';

import React from 'react';
import reactMixin from 'react-mixin';
import bem from '../libs/react-create-bem-element';
// import bemRouterLink from '../libs/bemRouterLink';
import sessionStore from '../stores/session';
import authUrls from '../stores/authUrls';
import Reflux from 'reflux';

import GettingStarted from './GettingStarted';

// CSS
require('normalize.css');
require('../styles/main.scss');
require('../styles/MetricsUI.scss');


var MainWrap = bem('main-wrap'),
    Header = bem('header', '<header>'),
    Footer = bem('footer', '<footer>');

class MetricsUiApp extends Reflux.Component {
  constructor (props) {
    super(props);
    this.state = {
      mobileMenuVisible: false,
    };
    this.mapStoreToState(sessionStore, (fromStore) => {
      return {session: fromStore};
    });
  }
  handleClick () {
    this.setState({mobileMenuVisible: !this.state.mobileMenuVisible});
  }
  logout () {
    sessionStore.logout();
  }
  render() {
    return (
      <MainWrap>
        <Header>
          <div id="logo-container">
              <a href="https://www.equitytool.org/"><img src="https://www.equitytool.org/wp-content/uploads/2015/08/EquityToolLogoWhiteOnly.png" alt="Equity Tool" /></a>
          </div>
          <div className="mobile-nav">
            <span className="mob-nav-btn" onClick={this.handleClick.bind(this)}>Menu</span>
          </div>
          <nav className={this.state.mobileMenuVisible ? 'navigation-container nav-menu visible' : 'navigation-container nav-menu not-visible'}>
            <ul id="menu-main" className="menu-ul">
              <li><a href="https://www.equitytool.org/the-equity-tool-2/">About<span className="drop-arrow"></span></a>
                <ul>
                  <li><a href="https://www.equitytool.org/the-equity-tool-2/">The EquityTool</a></li>
                  <li><a href="https://www.equitytool.org/equity/">Equity & Wealth</a></li>
                  <li><a href="https://www.equitytool.org/development/">Development</a></li>
                </ul>
              </li>
              <li><a href="https://www.equitytool.org/demo/">Demo</a></li>
              <li><a href="https://www.equitytool.org/countries/">Countries</a></li>
              <li><a href="https://www.equitytool.org/data-collection-options/">How to Use</a>
                <ul>
                  <li><a href="https://www.equitytool.org/data-collection-options/">Data Collection Options</a></li>
                  <li><a href="https://www.equitytool.org/web-app/">EquityTool Web App</a></li>
                  <li><a href="https://www.equitytool.org/dhis2/">DHIS2</a></li>
                  <li><a href="https://www.equitytool.org/other-platforms/">Other Platforms</a></li>
                  <li><a href="https://www.equitytool.org/interpreting-results/">Interpreting Results</a></li>
                  <li><a href="https://www.equitytool.org/urban-quintiles/">Urban-focused Surveys</a></li>
                </ul>
              </li>
              <li><a href="https://www.equitytool.org/contact-us/">Help</a>
                <ul>
                  <li><a href="https://www.equitytool.org/contact-us/">Contact Us</a></li>
                  <li><a href="https://www.equitytool.org/our-services/">Our Services</a></li>
                  <li><a href="https://www.equitytool.org/faq/">FAQ</a></li>
                </ul>
              </li>
              { !this.state.session.loggedIn &&
                <li><a href={authUrls.register}>Sign Up</a></li>
              }
              { this.state.session.loggedIn ?
                <li><a href={authUrls.logout}>Logout</a></li>
              :
                <li><a href={authUrls.login}>Login</a></li>
              }
            </ul>
          { this.state.session.loggedIn &&
            <div className="account-details">Welcome {this.state.session.username}</div>
          }

          </nav>
        </Header>
        {this.props.children}
        <Footer>
          {'Metrics for Management, 2021'}
        </Footer>
      </MainWrap>
    );
  }
}

export default MetricsUiApp;
