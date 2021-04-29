import React from 'react';
import Reflux from 'reflux';
import {Redirect} from 'react-router-dom';
import sessionStore from '../stores/session';

export var [RequireLoggedIn, RequireNotLoggedIn] = (function(){
  var requireLoginValue = function(loginBool) {
    class AuthRedirect extends Reflux.Component {
      constructor (props) {
        super(props);
        this.store = sessionStore;
      }
      render () {
        if (this.state.loggedIn !== loginBool) {
          return <Redirect push to={this.props.failTo} />
        }
        return null;
      }
    }
    return AuthRedirect;
  };
  return [requireLoginValue(true), requireLoginValue(false)];
})();
