import Reflux from 'reflux';

export var sessionStore = Reflux.createStore({
  init () {
    this.state = {
      loggedIn: false,
      fullName: 'your name',
      email: 'your@email.com',
    };
    window.setTimeout((() => {
      var willBeLoggedIn = Math.random() < 0.5;
      this.state.loggedIn = willBeLoggedIn;
      console.log('simulating logging in? ', this.state.loggedIn);
      this.trigger(this.state);
      window.setTimeout(() => {
        this.state.loggedIn = !willBeLoggedIn;
        console.log('simulating opposite log in: ', this.state.loggedIn);
        this.trigger(this.state);
      }, 20000);
    }), 2000);
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
