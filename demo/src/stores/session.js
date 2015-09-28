import Reflux from 'reflux';

export var sessionStore = Reflux.createStore({
  init () {
    this.state = {
      loggedIn: false,
      fullName: 'your name',
      email: 'your@email.com',
    };
    window.setTimeout((() => {
      console.log('simulating logging in', this);
      this.state.loggedIn = true;
      this.trigger(this.state);
    }), 5000);
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
