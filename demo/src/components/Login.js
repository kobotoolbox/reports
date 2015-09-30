
'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';

require('styles/Forms.scss');
require('styles/Login.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    FormFields = bem('form-fields'),
    SubmitButton = bem('submit-button', '<button>'),
    Inputfield = bem('field', '<input>'),
    Navlink = bem('navlink', '<a>'),
    BackLink = bem('backlink', '<a>');

var Login = React.createClass({
  mixins: [
    Navigation,
  ],
  render: function () {
    return (
        <Content m='login'>
          <h2>Login</h2>
          <form>
            <FormFields m='login'>
              <Inputfield name={'uname'} type='text' m='required' placeholder='username' />
              <br/>
              <Inputfield name={'pass'} type='pass' m='required' placeholder='password' />
              <Navlink href={'#/'} m='forgot'>
                forgot?
              </Navlink>
              <br/>
            </FormFields>
            <SubmitButton>
              Log In
            </SubmitButton>
            <p>
              <BackLink href={'#/'}>
                go back
              </BackLink>
            </p>
          </form>
        </Content>
      );
  }
});

module.exports = Login;