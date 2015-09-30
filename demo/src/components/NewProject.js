'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import Countries from '../libs/metrics-countries';
var Select = require('react-select');
require('../../node_modules/react-select/dist/default.css');

var ReactTooltip = require('react-tooltip');

require('styles/Forms.scss');
require('styles/NewProject.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    FormFields = bem('form-fields'),
    SubmitButton = bem('submit-button', '<button>'),
    FormItem = bem('form-item'),
    InputField = bem('field', '<input>'),
    BackLink = bem('backlink', '<a>');

var NewProject = React.createClass({
  mixins: [
    Navigation,
  ],
  render: function () {
    var effect = 'solid';
    var tooltip = 'If your respondents will all be from urban areas, and you are interested to see how wealthy they are compared to the rest of the urban population, you should check this box.<br/>The equity tool will always tell you how wealthy your clients are relative to the rest of the whole country. Some programs that serve urban clients only are also interested to see how wealthy their clients are relative to the urban population in their country. If you check this box, you will get two sets of results at the end of the survey – you will see which national wealth quintiles your clients are in and also which urban quintiles your clients are in.<br/>Note you should only check this box if all your clients will be from urban areas – the urban results are only relevant to urban clients.';
    return (
        <Content m='new-project'>
          <h2>Create a new project</h2>
          <form>
            <FormFields m='register'>
              <FormItem>
                <InputField name={'projectname'} type='text' m='required' placeholder='Project Name' />
              </FormItem>
              <FormItem>
              <InputField name={'projectdesc'} type='text' m='required' placeholder='Project Description' />
              </FormItem>
              <FormItem m='urban'>
              <InputField name={'urbanfocused'} type='checkbox' value='urbanfocused' id='urbancheckbox' />
              <label htmlFor='urbancheckbox'>This is an urban-focused project</label>
              <span className='field-tooltip' data-tip={tooltip}>?</span>
              <ReactTooltip effect={effect} multiline={true}/>
              </FormItem>
              <FormItem m='country'>
              <Select
                  name="country"
                  options={Countries}
                  placeholder='Country'
              />
              </FormItem>
            </FormFields>
            <SubmitButton>
              Create
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

module.exports = NewProject;