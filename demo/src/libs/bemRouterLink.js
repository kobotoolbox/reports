import React from 'react';
import reactMixin from 'react-mixin';
import Router from 'react-router';

import bem from '../libs/react-create-bem-element';

/*
the purpose of this module is to allow you to pass the same
parameters you pass to <Link> and the same class parameters
you pass to bem().

Router.Link example:

  <Link to="report" params={{ id: 3 }}
        className="sample-report sample-report--new sample-report--dynamic">
    Report 3
  <Link>

With this:

  var SampleReport = bemRouterLink('sample-report')
  <SampleReport to="report" params={{ id: 3 }}
        m={['new', 'dynamic']}>
    Report 3
  </SampleReport>
*/

export default function(baseKls) {
  var El = bem(baseKls, '<a>');
  class c extends React.Component {
    componentWillMount () {
      var props = Object.assign({}, this.props);
      if (props.mTo) {
        props.m = props.to = props.mTo;
      }
      if (!props.href) {
        props.href = this.makeHref(props.to, props.params, props.query);
      }
      delete props.to;
      delete props.mTo;
      delete props.params;
      delete props.query;
      this._Props = props;
    }
    render () {
      return <El {...this._Props} />;
    }
  }
  reactMixin(c.prototype, Router.Navigation);
  return c;
}
