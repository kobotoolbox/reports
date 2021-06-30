'use strict';

import React from 'react';
import reactMixin from 'react-mixin';
import Reflux from 'reflux';
import { withRouter } from 'react-router-dom'; // to include history in the props
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import actions from '../actions/actions';
import accountStore from '../stores/account';
import authUrls from '../stores/authUrls';
import {RequireNotLoggedIn} from '../libs/requireLogins';

require('styles/Forms.scss');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    FormFields = bem('form-fields'),
    Inputfield = bem('field', '<input>'),
    InputWrap = bem('field-wrap'),
    InputfieldMessage = bem('field-message'),
    BorderedButton = bem('bordered-button', '<button>'),
    SimpleLink = bemRouterLink('simple-link');

var registration = accountStore.state.registrationForm;

const FIELDS = ['username', 'password', 'password_confirmation',
                'first_name', 'last_name', 'organization', 'email', 'terms'];

const fieldLabels = {
  first_name: 'first name',
  last_name: 'last name',
  password_confirmation: 'password confirmation',
};

class Register extends Reflux.Component {
  constructor (props) {
    super(props);
    registration.state.terms = false;
    this.state = registration.state;
  }
  componentDidMount () {
    this.listenTo(accountStore, this.accountStoreChanged);
  }
  accountStoreChanged (acctState) {
    if (acctState.errors) {
      this.setState(acctState);
    } else {
      console.log('success: ', acctState);
      actions.confirmLogin();
      this.props.history.push('/getting-started');
    }
  }
  formFieldChange (evt) {
    registration.updateField(evt.target, false);
    this.setState(registration.state);
  }
  formFieldBlur (evt) {
    registration.updateField(evt.target, true);
    this.setState(registration.state);
  }
  submitForm (evt) {
    evt.preventDefault();
    FIELDS.forEach((key) => {
      registration.updateField(this.refs[key].props, true);
    });
    if (registration.isValid()) {
      actions.registerAccount(
        registration.getData()
        );
    } else {
      this.setState(registration.state);
    }
  }
  render () {
    return (
        <Content m='register'>
          <RequireNotLoggedIn failTo='/getting-started' />
          <ContentBg>
            <ContentTitle>Sign Up</ContentTitle>
            <form>
              <FormFields m='register'>
                {
                  FIELDS.map((att) => {
                    var error = this.state.errors[att],
                        isBlurred = registration._isBlurred[att];
                    if (att.match(/^terms/)) {
                      return (
                        <InputWrap key={`field-${att}`} m={{
                              error: error,
                            }}>
                          <Inputfield ref={att}
                                name={att}
                                type='checkbox'
                                checked={this.state.terms}
                                m='required'
                                onChange={this.formFieldChange.bind(this)} />
                            <span> By signing up, I agree to the&nbsp;
                              <SimpleLink m='terms' to='/terms' target='_blank'>
                                Terms and Conditions
                              </SimpleLink>
                              .</span>
                          <InputfieldMessage>
                            { error ?
                              error
                            : null }
                          </InputfieldMessage>
                        </InputWrap>
                      );
                    } else {
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
                                onBlur={this.formFieldBlur.bind(this)}
                                onChange={this.formFieldChange.bind(this)} />
                          <InputfieldMessage>
                            { error ?
                              error
                            : null }
                          </InputfieldMessage>
                        </InputWrap>
                      );
                    }
                  })
                }

              </FormFields>
              <BorderedButton m={{
                'create-account': true,
              }}
                onClick={this.submitForm.bind(this)}
              >
                Create Account
              </BorderedButton>
              <span> Already have an account? </span>
              <SimpleLink href={authUrls.login} to='/login'>
                Login here
              </SimpleLink>
            </form>
          </ContentBg>
        </Content>
      );
  }
}

reactMixin(Register.prototype, Reflux.ListenerMixin);

export default withRouter(Register);
