
'use strict';

import React from 'react/addons';
import Reflux from 'reflux';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import actions from '../actions/actions';
import accountStore from '../stores/account';
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

var registration = accountStore.state.registrationForm;

const FIELDS = ['username', 'password', 'password_confirmation',
                'first_name', 'last_name', 'organization', 'email'];

const fieldLabels = {
  first_name: 'first name',
  last_name: 'last name',
  password_confirmation: 'password confirmation',
};

var Register = React.createClass({
  mixins: [
    Navigation,
    requireNotLoggedInMixin({failTo: 'getting-started'}),
    Reflux.ListenerMixin,
  ],
  componentDidMount () {
    this.listenTo(accountStore, this.accountStoreChanged);
  },
  accountStoreChanged (acctState) {
    if (acctState.errors) {
      console.log('errors: ', acctState);
      this.setState(acctState);
    } else {
      console.log('success: ', acctState);
      actions.confirmLogin();
      this.transitionTo('getting-started');
    }
  },
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
    var data = {};
    FIELDS.forEach((key) => {
      data[key] = this.refs[key].getDOMNode().value;
    });
    actions.registerAccount(data);
  },
  render: function () {
    return (
        <Content m='register'>
          <ContentBg>
            <ContentTitle>Register</ContentTitle>
            <form>
              <FormFields m='register'>
                {
                  FIELDS.map((att) => {
                    var error = this.state.errors[att],
                        isBlurred = registration._isBlurred[att];

                    return (
                      <InputWrap key={`field-${att}`} m={{
                            error: error && isBlurred,
                            warning: error && !isBlurred,
                          }}>
                        <Inputfield ref={att}
                              name={att}
                              type={att.match(/^password/) ? 'password' : 'text'}
                              value={this.state[att]}
                              m='required'
                              placeholder={fieldLabels[att] || att}
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
