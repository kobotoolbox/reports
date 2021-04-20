'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import {allCountries} from '../libs/metrics-countries';
import actions from '../actions/actions';
import {requireLoggedInMixin} from '../mixins/requireLogins';
import sessionStore from '../stores/session';
import Select from 'react-select';
import alertify from 'alertifyjs';

require('../../node_modules/react-select/dist/default.css');
require('styles/Forms.scss');
require('styles/NewProject.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    FormFields = bem('form-fields'),
    FormItem = bem('form-item'),
    InputField = bem('field', '<input>'),
    BorderedNavlink = bemRouterLink('bordered-navlink'),
    BorderedButton = bem('bordered-button', '<button>');

var NewProject = React.createClass({
  mixins: [
    Navigation,
    requireLoggedInMixin({failTo: 'getting-started'}),
  ],
  getInitialState () {
    return {
      country: null,
      regions: [],
      region: null,
    };
  },
  createNewProject (evt) {
    evt.preventDefault();
    let createButton = evt.target;
    let createButtonInitialText = createButton.innerText;
    createButton.disabled = true;
    createButton.innerText = 'Creating...';
    actions.createTemplate({
      name: this.refs.name.getDOMNode().value,
      country: this.state.region || this.state.country,
      regional: !!this.state.region,
    }).then(() => {
      alertify.success('Survey creation successful!');
      this.transitionTo('project-list');
      actions.listRenderings();
    }, (data) => {
      createButton.innerText = createButtonInitialText;
      createButton.disabled = false;
      if('name' in data.responseJSON) {
        alertify.error(data.responseJSON.name);
      } else {
        alertify.error('Survey creation failed!');
      }
    });
  },
  changeCountry (country) {
    this.setState({
      country: country,
      regions: sessionStore.regions.filter(
        function(r) { return r.country === country; }
      ),
      region: null,
    });
  },
  changeRegion (region) {
    this.setState({
      region: region,
    });
  },
  render: function () {
    var countries = sessionStore.countries || allCountries;
    return (
        <Content m='new-project'>
          <ContentBg>
            <ContentTitle>Create a New Survey</ContentTitle>
            <form>
              <FormFields m='register'>
                <FormItem>
                  <InputField name={'projectname'} type='text' m='required' placeholder='Project Name' ref='name' />
                </FormItem>

                <FormItem m='country'>
                <Select
                    name="country"
                    options={countries}
                    placeholder='Country'
                    value={this.state.country || null}
                    ref='country'
                    onChange={this.changeCountry}
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
                        onChange={this.changeRegion}
                    />
                  </FormItem>
                }
              </FormFields>
              <BorderedButton onClick={this.createNewProject}>
                Create
              </BorderedButton>
              <span> or </span>
              <BorderedNavlink m={'back'} to='project-list'>
                Back
              </BorderedNavlink>
            </form>
          </ContentBg>
        </Content>
      );
  }
});

export default NewProject;
