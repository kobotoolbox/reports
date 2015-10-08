'use strict';

import React from 'react/addons';
import Reflux from 'reflux';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
// import demoReportHtml from './demoReportHtml';
import {Navigation} from 'react-router';
import {requireLoggedInMixin} from '../mixins/requireLogins';
import actions from '../actions/actions';
import {individualRenderingStore} from '../stores/renderings';

require('styles/Report.scss');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    Backlink = bemRouterLink('backlink');

var Report = React.createClass({
  mixins: [
    Navigation,
    requireLoggedInMixin({failTo: 'getting-started'}),
    Reflux.ListenerMixin,
  ],
  componentDidMount () {
    this.listenTo(individualRenderingStore, this.individualRenderingStoreChanged);
    actions.getRendering(this.props.params.id);
  },
  getInitialState () {
    return {
      renderingHtml: 'loading',
    };
  },
  individualRenderingStoreChanged (projId, html) {
    if (this.props.params.id === projId) {
      this.setState({
        renderingHtml: html,
      });
    }
  },
  render: function () {
    return (
        <Content m='report'>
          <ContentBg>
            <ContentTitle>Project Results</ContentTitle>
            <div dangerouslySetInnerHTML={{ __html: this.state.renderingHtml }} />
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
