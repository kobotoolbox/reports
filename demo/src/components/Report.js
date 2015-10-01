'use strict';

import React from 'react/addons';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import demoReportHtml from './demoReportHtml';

require('styles/Report.scss');

var Content = bem('content'),
    Backlink = bemRouterLink('backlink');

var Report = React.createClass({
  render: function () {
    return (
        <Content m='report'>
          <div dangerouslySetInnerHTML={{ __html: demoReportHtml }} />
          <p>
            <Backlink to='project-list'>
              go back
            </Backlink>
          </p>
        </Content>
      );
  }
});

module.exports = Report;
