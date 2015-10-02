
'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import {registration} from './registrationForm';
import actions from '../actions/actions';
import {requireNotLoggedInMixin} from '../mixins/requireLogins';

require('styles/Forms.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    FormFields = bem('form-fields'),
    Inputfield = bem('field', '<input>'),
    InputWrap = bem('field-wrap'),
    InputfieldMessage = bem('field-message'),
    BorderedButton = bem('bordered-button', '<button>'),
    BorderedNavlink = bemRouterLink('bordered-navlink');

function t(str) { return str; }

var Register = React.createClass({
  mixins: [
    Navigation,
    requireNotLoggedInMixin({failTo: 'getting-started'}),
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
  submitForm (evt) {
    evt.preventDefault();
    actions.placeholder('create account');
  },
  render: function () {
    return (
        <Content m='register'>
          <ContentBg>
            <ContentTitle>Register</ContentTitle>
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
                              m='required'
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
              <BorderedButton m={{
                'create-account': true,
              }}
                onClick={this.submitForm}
              >
                Create Account
              </BorderedButton>
              <span> or </span>
              <BorderedNavlink m='back' to='getting-started'>
                go back
              </BorderedNavlink>
            </form>
          </ContentBg>
        </Content>
      );
  }
});

module.exports = Register;
