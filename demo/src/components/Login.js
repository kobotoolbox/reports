
'use strict';

import React from 'react';
import reactMixin from 'react-mixin';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import actions from '../actions/actions';
import {requireNotLoggedInMixin} from '../mixins/requireLogins';

require('styles/Forms.scss');
require('styles/Login.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    FormFields = bem('form-fields'),
    BorderedButton = bem('bordered-button', '<button>'),
    Inputfield = bem('field', '<input>'),
    Navlink = bemRouterLink('navlink');

class Login extends React.Component {
  login (evt) {
    evt.preventDefault();
    actions.placeholder('login');
  }
  render () {
    return (
        <Content m='login'>
          <ContentBg>
            <ContentTitle>Login</ContentTitle>
            <form>
              <FormFields m='login'>
                <Inputfield name={'uname'} type='text' m='required' placeholder='username' />
                <br/>
                <Inputfield name={'password'} type='password' m='required' placeholder='password' />
                <Navlink href='#forgot' m='forgot' className='disabled'>
                  forgot?
                </Navlink>
                <br/>
              </FormFields>
              <BorderedButton onClick={this.login}>
                Log in
              </BorderedButton>
              <span> No account yet? </span>
              <SimpleLink href={authUrls.register} m='register'>
                Create one here
              </SimpleLink>
            </form>
          </ContentBg>
        </Content>
      );
  }
}

reactMixin(Login.prototype,  Navigation);
reactMixin(Login.prototype,  requireNotLoggedInMixin({failTo: 'getting-started'}));

export default Login;
