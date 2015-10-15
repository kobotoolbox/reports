'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import allCountries from '../libs/metrics-countries';
import actions from '../actions/actions';
import {requireLoggedInMixin} from '../mixins/requireLogins';
import sessionStore from '../stores/session';
import Select from 'react-select';
import ReactTooltip from 'react-tooltip';

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
    };
  },
  createNewProject (evt) {
    evt.preventDefault();
    actions.createTemplate({
      name: this.refs.name.getDOMNode().value,
      urban: this.refs.urban.getDOMNode().checked ? 'true' : 'false',
      country: this.state.country,
    }, {
      onComplete: () => {
        this.transitionTo('project-list');
        actions.listRenderings();
      }
    });
  },
  changeCountry (country) {
    this.setState({
      country: country,
    });
  },
  render: function () {
    var effect = 'solid';
    var tooltip = 'If your respondents will all be from urban areas, and you are interested to see how wealthy they are compared to the rest of the urban population, you should check this box.<br/>The equity tool will always tell you how wealthy your clients are relative to the rest of the whole country. Some programs that serve urban clients only are also interested to see how wealthy their clients are relative to the urban population in their country. If you check this box, you will get two sets of results at the end of the survey – you will see which national wealth quintiles your clients are in and also which urban quintiles your clients are in.<br/>Note you should only check this box if all your clients will be from urban areas – the urban results are only relevant to urban clients.';
    var countries = sessionStore.countries || allCountries;
    return (
        <Content m='new-project'>
          <ContentBg>
            <ContentTitle>Create a New Project</ContentTitle>
            <form>
              <FormFields m='register'>
                <FormItem>
                  <InputField name={'projectname'} type='text' m='required' placeholder='Project Name' ref='name' />
                </FormItem>
                <FormItem m='urban'>
                <InputField name={'urbanfocused'} type='checkbox' value='urbanfocused' id='urbancheckbox' ref='urban' />
                <label htmlFor='urbancheckbox'>This is an urban-focused project</label>
                <span className='field-tooltip' data-tip={tooltip}>?</span>
                <ReactTooltip effect={effect} multiline={true}/>
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
              </FormFields>
              <BorderedButton onClick={this.createNewProject}>
                Create
              </BorderedButton>
              <span> or </span>
              <BorderedNavlink m={'back'} to='project-list'>
                go back
              </BorderedNavlink>
            </form>
          </ContentBg>
        </Content>
      );
  }
});

module.exports = NewProject;
