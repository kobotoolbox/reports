import Reflux from 'reflux';
import actions from '../actions/actions';

var sessionStore = Reflux.createStore({
  init () {
    this.state = {
      loggedIn: null,
    };
    this.listenTo(actions.confirmLogin.completed, this.confirmLoginCompleted);
    this.listenTo(actions.confirmLigin.failed, this.confirmLoginFailed);
    actions.confirmLogin();

    function extendFakeCredentials(st){
      st.fullName = 'your name';
      st.email = 'your@email.com';
      st.loggedIn = true;
    }
    extendFakeCredentials(this.state);
    /*
    window.setTimeout((() => {
      var willBeLoggedIn = true; //Math.random() < 0.5;
      this.state.loggedIn = willBeLoggedIn;
      if (willBeLoggedIn) {
      }
      console.log('simulating logging in? ', this.state.loggedIn);
      this.trigger(this.state);
      // window.setTimeout(() => {
      //   this.state.loggedIn = !willBeLoggedIn;
      //   console.log('simulating opposite log in: ', this.state.loggedIn);
      //   this.trigger(this.state);
      // }, 20000);
    }), 2000);
    */
  },
  confirmLoginCompleted () {
    console.log('confirm login completed');
  },
  confirmLoginFailed () {
    console.log('confirm login failed');
  },
  logout () {
    this.state.loggedIn = false;
    this.trigger(this.state);
  },
  login () {
    this.state.loggedIn = true;
    this.trigger(this.state);
  }
});

export default sessionStore;
