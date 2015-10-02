'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import demoReportHtml from './demoReportHtml';
import {Navigation} from 'react-router';
import {requireLoggedInMixin} from '../mixins/requireLogins';

require('styles/Report.scss');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    Backlink = bemRouterLink('backlink');

var Report = React.createClass({
  mixins: [
    Navigation,
    requireLoggedInMixin({failTo: 'getting-started'}),
  ],
  render: function () {
    return (
        <Content m='report'>
          <ContentBg>
            <ContentTitle>Project Results</ContentTitle>
            <div dangerouslySetInnerHTML={{ __html: demoReportHtml }} />
            <p>
              <Backlink to='project-list'>
                go back
              </Backlink>
            </p>
          </ContentBg>
        </Content>
      );
  }
});

module.exports = Report;