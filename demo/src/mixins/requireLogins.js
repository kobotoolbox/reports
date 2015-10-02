import sessionStore from '../stores/session';

export var [requireLoggedInMixin, requireNotLoggedInMixin] = (function(){
  var requireLoginValue = function(loginBool) {
    return function authMixin({failTo, failToParams}) {
      return {
        componentDidMount () {
          this._unsubscribe = sessionStore.listen(this._checkRequireLoginValue);
        },
        componentWillUnmount () {
          this._unsubscribe();
        },
        _checkRequireLoginValue (sessionState) {
          console.log('requiring that login is ', loginBool, sessionState);
          if (sessionState.loggedIn !== loginBool) {
            this.transitionTo(failTo, failToParams);
          }
        },
        statics: {
          willTransitionTo: function (transition, o1, o2, cb) {
            if (loginBool && sessionStore.state.loggedIn === false) {
              transition.redirect(failTo, failToParams);
            } else if (!loginBool && sessionStore.state.loggedIn) {
              transition.redirect(failTo, failToParams);
            }
            cb();
          }
        },
      };
    };
  };
  return [requireLoginValue(true), requireLoginValue(false)];
})();
