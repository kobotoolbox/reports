import Reflux from 'reflux';
import actions from '../actions/actions';
import {registration} from '../registrationForm';

var accountStore = Reflux.createStore({
  init () {
    this.state = {
      registrationForm: registration,
    };
    this.listenTo(actions.registerAccount.completed, this.registerAccountCompleted);
    this.listenTo(actions.registerAccount.failed, this.registerAccountFailed);
  },
  registerAccountCompleted (data) {
    console.log('registerAccountCompleted. data: ', data);
    this.trigger(this.state);
  },
  registerAccountFailed (errors) {
    Object.keys(errors).forEach((errKey) => {
      registration.setError(errKey, errors[errKey]);
    });
    this.trigger({
      errors: true,
      registrationForm: registration,
    });
  },
});

export default accountStore;
