
'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';

require('styles/Forms.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
		FormFields = bem('form-fields'),
		SubmitButton = bem('submit-button', '<button>'),
		Inputfield = bem('field', '<input>'),
		BackLink = bem('backlink', '<a>');

var Register = React.createClass({
  mixins: [
    Navigation,
  ],
  render: function () {
    return (
        <Content m='register'>
          <h2>Register</h2>
          <form>
						<FormFields m='register'>
							<Inputfield name={'uname'} type='text' m='required' placeholder='username' />
							<br/>
							<Inputfield name={'pass'} type='pass' m='required' placeholder='password' />
							<br/>
							<Inputfield name={'name'} type='text' m='required' placeholder='name' />
							<br/>
							<Inputfield name={'org'} type='text' m='required' placeholder='organisation' />
							<br/>
							<Inputfield name={'email'} type='text' m='required' placeholder='email' />
							<br/>
						</FormFields>
						<SubmitButton>
							Create Account
						</SubmitButton>
          </form>
          <p>
						<BackLink href={'#/'}>
							go back
						</BackLink>
					</p>
        </Content>
      );
  }
});

module.exports = Register;
