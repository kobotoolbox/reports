import Reflux from 'reflux';
import actions from '../actions/actions';

var accountStore = Reflux.createStore({
  init () {
    this.state = {};
    this.listenTo(actions.registerAccount.completed, this.registerAccountCompleted);
    this.listenTo(actions.registerAccount.failed, this.registerAccountFailed);
  },
  registerAccountCompleted (data) {
    console.log('registerAccountCompleted. data: ', data);
    this.trigger(this.state);
  },
  registerAccountFailed (errors) {
    console.log('registerAccountFailed. errors: ', errors);
    this.trigger({
      errors: errors,
    });
  },
});

export default accountStore;
