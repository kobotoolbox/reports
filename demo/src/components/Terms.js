'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';

require('styles/Terms.scss');

let {
  Navigation,
} = require('react-router');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentWrap = bem('content-wrap'),
    ContentTitle = bem('content-title', '<h2>');

var Terms = React.createClass({
  mixins: [
    Navigation,
  ],
  render: function () {
    return (
        <Content m='terms'>
          <ContentBg>
            <ContentWrap>
              <ContentTitle>Terms and Conditions</ContentTitle>
              <p>I understand that Metrics for Management has created the online and mobile-based EquityTool based on analysis for the simplification of the Demographic and Health Survey wealth asset questions led by PSI. </p>
              <p>By creating an account on this site, I acknowledge that an account will be made for me at KoBoToolbox, the survey platform used for the EquityTool, and I agree to the <a href="https://www.kobotoolbox.org/terms">KoBoToolbox Terms of Service</a>. </p>
              <p>I also acknowledge that this EquityTool account and access to detailed data and survey features are available through KoBoToolbox. I recognize that I am the owner of data collected using the EquityTool and permit Metrics for Management to collect anonymous, aggregated use statistics. I understand that Metrics for Management will not have access to the data I have collected through this account.</p>
            </ContentWrap>
          </ContentBg>
        </Content>
      );
  }
});

module.exports = Terms;
