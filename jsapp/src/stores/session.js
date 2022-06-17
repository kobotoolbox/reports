import Reflux from 'reflux-react-16';
import actions from '../actions/actions';

var sessionStore = Reflux.createStore({
  init () {
    this.state = {
      loggedIn: null,
    };
    this.listenTo(actions.confirmLogin.completed, this.confirmLoginCompleted);
    this.listenTo(actions.confirmLogin.failed, this.confirmLoginFailed);
    actions.confirmLogin();

    // function extendFakeCredentials(st){
    //   st.fullName = 'your name';
    //   st.email = 'your@email.com';
    //   st.username = 'yourusername';
    //   st.loggedIn = true;
    // }
    // extendFakeCredentials(this.state);
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
  confirmLoginCompleted (data) {
    if (data.countries) {
      // a country has no parent
      this.countries = data.countries.filter(
        function(c) { return c.parent === null; }
      ).map(function(c){
        return {
          value: c.id,
          label: c.name,
        };
      });
      // a region has a parent
      this.regions = data.countries.filter(
        function(c) { return c.parent !== null; }
      ).map(function(c) {
        return {
          country: c.parent,
          value: c.id,
          label: c.name,
        };
      });
      delete data.countries;
    }
    if (data.username) {
      this.state = Object.assign({
        loggedIn: true,
      }, data);
    } else {
      this.state = Object.assign({
        loggedIn: false,
      }, data);
    }
    this.trigger(this.state);
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
