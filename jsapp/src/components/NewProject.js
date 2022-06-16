'use strict';

import React from 'react';
import Reflux from 'reflux-react-16';
import reactMixin from 'react-mixin';
import { withRouter } from 'react-router-dom';
import history from 'history/hash';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import {allCountries} from '../libs/metrics-countries';
import actions from '../actions/actions';
import {RequireLoggedIn} from '../libs/requireLogins';
import sessionStore from '../stores/session';
import Select from 'react-select';
import alertify from 'alertifyjs';

require('styles/Forms.scss');
require('styles/NewProject.scss');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    FormFields = bem('form-fields'),
    FormItem = bem('form-item'),
    InputField = bem('field', '<input>'),
    BorderedNavlink = bemRouterLink('bordered-navlink'),
    BorderedButton = bem('bordered-button', '<button>');

class NewProject extends Reflux.Component {
  constructor (props) {
    super(props);
    this.state = {
      name: '',
      country: null,
      regions: [],
      region: null,
    };
  }
  createNewProject (evt) {
    evt.preventDefault();
    let createButton = evt.target;
    let createButtonInitialText = createButton.innerText;
    createButton.disabled = true;
    createButton.innerText = 'Creating...';
    actions.createTemplate.triggerAsync({
      name: this.refs.name.props.value,
      country: this.state.region?.value || this.state.country.value,
      regional: !!this.state.region?.value,
    }).then(() => {
      alertify.success('Survey creation successful!');
      this.props.history.push('/project-list');
      actions.listRenderings();
    }, (data) => {
      createButton.innerText = createButtonInitialText;
      createButton.disabled = false;
      if(data.responseJSON && 'name' in data.responseJSON) {
        alertify.error(data.responseJSON.name);
      } else {
        alertify.error('Survey creation failed!');
      }
    });
  }
  changeName (evt) {
    this.setState({
      name: evt.target.value,
    });
  }
  changeCountry (country) {
    this.setState({
      country: country,
      regions: sessionStore.regions.filter(
        function(r) { return r.country === country.value; }
      ),
      region: null,
    });
  }
  changeRegion (region) {
    this.setState({
      region: region,
    });
  }
  render () {
    var countries = sessionStore.countries || allCountries;
    return (
        <Content m='new-project'>
          <RequireLoggedIn failTo='/getting-started' />
          <ContentBg>
            <ContentTitle>Create a New Survey</ContentTitle>
            <form>
              <FormFields m='register'>
                <FormItem>
                  <InputField
                    name={'projectname'}
                    type='text'
                    m='required'
                    placeholder='Project Name'
                    ref='name'
                    value={this.state.name}
                    onChange={this.changeName.bind(this)}
                  />
                </FormItem>

                <FormItem m='country'>
                <Select
                    name="country"
                    options={countries}
                    placeholder='Country'
                    value={this.state.country || null}
                    ref='country'
                    onChange={this.changeCountry.bind(this)}
                />
                </FormItem>

                { !!this.state.regions.length &&
                  <FormItem m='region'>
                    <Select
                        name="region"
                        options={this.state.regions}
                        placeholder='Region (optional)'
                        value={this.state.region || null}
                        ref='country'
                        onChange={this.changeRegion.bind(this)}
                    />
                  </FormItem>
                }
              </FormFields>
              <BorderedButton onClick={this.createNewProject.bind(this)}>
                Create
              </BorderedButton>
              <span> or </span>
              <BorderedNavlink m={'back'} to='/project-list'>
                Back
              </BorderedNavlink>
            </form>
          </ContentBg>
        </Content>
      );
  }
}

export default withRouter(NewProject);
