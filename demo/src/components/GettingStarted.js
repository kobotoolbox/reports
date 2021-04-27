'use strict';

import React from 'react';
import reactMixin from 'react-mixin';
import {Redirect} from 'react-router-dom';
import bem from '../libs/react-create-bem-element';
import sessionStore from '../stores/session';
import bemRouterLink from '../libs/bemRouterLink'; // !
import Reflux from 'reflux';
import accountStore from '../stores/account';
import authUrls from '../stores/authUrls';

require('styles/GettingStarted.scss');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentWrap = bem('content-wrap'),
    ContentTitle = bem('content-title', '<h2>'),
    InfoMessage = bem('info-message'),
    InfoMessage__link = bem('info-message__link', '<a>'),
    BorderedNavlink = bemRouterLink('bordered-navlink'),
    BorderedNavlinkExternal = bem('bordered-navlink', '<a>');

class GettingStarted extends Reflux.Component {
  constructor (props) {
    super(props);

    // https://github.com/reflux/refluxjs/tree/master/docs/components#manually-mapping-states-with-thismapstoretostate
    this.mapStoreToState(accountStore, (fromStore) => {
      return {accountCreated: fromStore.created};
    });
    this.mapStoreToState(sessionStore, (fromStore) => {
      return {session: fromStore};
    });
  }

  render () {
    if (this.state.session?.loggedIn) {
      return <Redirect push to='/project-list' />;
    }
    return (
        <Content m='getting-started'>
          <ContentBg>
            { this.state.session?.loggedIn ?
              <ContentWrap>
                <ContentTitle>EquityTool Surveys</ContentTitle>
                <p>Create a new survey or a view a list of your current surveys.</p>
                <p>For more information about how to use the tool, click <a href="https://www.equitytool.org/data-collection-options/">here</a>.</p>
                <div>
                  <p>
                    <BorderedNavlink m='new-project' to='/new-project'>
                      New survey
                    </BorderedNavlink>
                    <span> or </span>
                    <BorderedNavlink m='projects' to='/project-list'>
                      Survey list
                    </BorderedNavlink>
                  </p>
                </div>
              </ContentWrap>
            :
            <ContentWrap>
              <ContentTitle>Getting Started with the EquityTool</ContentTitle>
              <p>Create a free account to begin measuring the wealth distribution of your program beneficiaries. After registration, you will immediately be able to log in to the EquityTool to set up a survey, and begin collecting data.</p>
              <p>For more information about how to use the tool, click <a href="https://www.equitytool.org/data-collection-options/">here</a>.</p>
              <div className='getting-started__buttons'>
                <BorderedNavlink to='/register' m='register'>
                  Create account
                </BorderedNavlink>
                <span> or </span>
                <BorderedNavlinkExternal href={authUrls.login} m='login'>
                  Log in
                </BorderedNavlinkExternal>
              </div>
            </ContentWrap>
            }
            { this.state.accountCreated ?
              <InfoMessage m='account-created'>
                {'You have created an account with the username "' +
                  this.state.accountCreated.username +
                 '". Please '}
                <InfoMessage__link href={authUrls.login} to='/login'>
                  log in
                </InfoMessage__link>
                {'.'}
              </InfoMessage>
            : null}
          </ContentBg>
        </Content>
      );
  }
}

export default GettingStarted;
