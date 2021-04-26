import React from 'react';
import {Link} from 'react-router-dom';

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

export default function(bemBaseClass) {
  class BemRouterLink extends React.Component {
    constructor (frozenProps) {
      const props = {...frozenProps};
      if (props.mTo) {
        // unused but apparently a shortcut for when `m` and `to` are the same
        props.m = props.to = props.mTo;
        delete props.mTo;
      }
      let modifier = props.m;
      delete props.m;

      // BemElementClass is a JS class; bemBaseClass is a CSS class
      const BemElementClass = bem(bemBaseClass, '<a>');
      // Instantiate a temporary BEM element and copy its CSS class names
      const elementWithBemClassNames = new BemElementClass({m: modifier});
      props.className = elementWithBemClassNames.render().props.className;

      super(frozenProps);
      this._Props = props;
    }
    render () {
      return <Link {...this._Props} />;
    }
  }
  return BemRouterLink;
}
