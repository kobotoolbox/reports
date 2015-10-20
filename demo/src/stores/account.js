import Reflux from 'reflux';
import actions from '../actions/actions';
import {registration} from '../components/registrationForm';

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
  registerAccountFailed (jqxhr) {
    var responseJSON = jqxhr.responseJSON;
    if (jqxhr) {
      throw new Error('Whats wrong?');
    }
    Object.keys(responseJSON).forEach((errKey) => {
      registration.setError(errKey, responseJSON[errKey]);
    });
    this.trigger({
      errors: responseJSON,
      registrationForm: registration,
    });
  },
});

export default accountStore;
