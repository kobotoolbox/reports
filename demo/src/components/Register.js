
'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import {registration} from './registrationForm';

require('styles/Forms.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    FormFields = bem('form-fields'),
    SubmitButton = bem('submit-button', '<button>'),
    Inputfield = bem('field', '<input>'),
    InputWrap = bem('field-wrap'),
    InputfieldMessage = bem('field-message'),
    BackLink = bem('backlink', '<a>');

function t(str) { return str; }

var Register = React.createClass({
  mixins: [
    Navigation,
  ],
  getInitialState () {
    return registration.state;
  },
  formFieldChange (evt) {
    var _et = evt.target;
    registration.updateField(_et.name, _et.value, false);
    this.setState(registration.state);
  },
  formFieldBlur (evt) {
    var _et = evt.target;
    registration.updateField(_et.name, _et.value, true);
    this.setState(registration.state);
  },
  render: function () {
    return (
        <Content m='register'>
          <h2>Register</h2>
          <form>
            <FormFields m='register'>
              {
                ['username', 'password', 'name', 'organization', 'email'].map((att) => {
                  var error = this.state.errors[att],
                      isBlurred = registration._isBlurred[att];

                  return (
                    <InputWrap key={`field-${att}`} m={{
                          error: error && isBlurred,
                          warning: error && !isBlurred,
                        }}>
                      <Inputfield ref={att}
                            name={att}
                            type={att === 'password' ? 'password' : 'text'}
                            value={this.state[att]}
                            m={{
                              required: true,
                            }}
                            placeholder={t(att)}
                            onBlur={this.formFieldBlur}
                            onChange={this.formFieldChange} />
                      <InputfieldMessage>
                        { error ?
                          error
                        : null }
                      </InputfieldMessage>
                    </InputWrap>
                  );
                })
              }
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
