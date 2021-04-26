'use strict';

import React from 'react';
import reactMixin from 'react-mixin';
import Reflux from 'reflux';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import {RequireLoggedIn} from '../mixins/requireLogins';
import actions from '../actions/actions';
import {individualRenderingStore} from '../stores/renderings';

require('styles/Report.scss');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    BorderedNavlink = bemRouterLink('bordered-navlink'),
    ProjectLink = bem('project-link', '<a>'),
    UrbanToggle = bem('urban-toggle', '<div>');

class Report extends Reflux.Component {
  constructor (props) {
    this.state = {
      renderingHtml: 'loading',
      urbanVisible: false
    };
  }
  componentDidMount () {
    this.listenTo(individualRenderingStore, this.individualRenderingStoreChanged);
    actions.getRendering(this.props.params.id);
  }
  individualRenderingStoreChanged (projId, html) {
    if (this.props.params.id === projId) {
      this.setState({
        renderingHtml: html,
      });
    }
  }
  toggleUrbanState () {
      this.setState({
        urbanVisible: !this.state.urbanVisible,
      });

  }
  render () {
    return (
        <Content m='report'>
          <RequireLoggedIn failTo='/getting-started' />
          <ContentBg className={this.state.urbanVisible ? 'urban-visible' : 'urban-hidden'}>
            <div className="rendering" dangerouslySetInnerHTML={{ __html: this.state.renderingHtml }} />
            {this.state.renderingHtml !== 'loading' &&
              <UrbanToggle onClick={this.toggleUrbanState.bind(this)}>
                {this.state.urbanVisible ?
                  <div className="bordered-navlink">Hide Urban Results <i className="fa fa-chevron-up" /></div>
                :
                  <div className="bordered-navlink">Show Urban Results <i className="fa fa-chevron-down" /></div>
                }
              </UrbanToggle>
            }
            {this.state.renderingHtml !== 'loading' &&
              <div className="project-links">
                <ProjectLink
                  className="bordered-navlink"
                  href={'/rendering/' + this.props.params.id + '.pdf?show_urban=' + this.state.urbanVisible}
                >
                  download PDF
                </ProjectLink>
                <ProjectLink
                  className="bordered-navlink"
                  href={'/rendering/' + this.props.params.id + '.docx?show_urban=' + this.state.urbanVisible}
                >
                  download DOC
                </ProjectLink>
              </div>
            }
            <div className="project-footer">
              <BorderedNavlink to='project-list'>
                <i className="fa fa-chevron-left" />
                go back
              </BorderedNavlink>
            </div>
          </ContentBg>
        </Content>
      );
  }
}

reactMixin(Report.prototype, Reflux.ListenerMixin);

export default Report;
