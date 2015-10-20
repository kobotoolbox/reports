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
    console.log('jqxhr', jqxhr, jqxhr.responseJSON);
    var errors = JSON.parse(jqxhr.responseJSON);
    Object.keys(errors).forEach((errKey) => {
      registration.setError(errKey, errors[errKey]);
    });
    this.trigger({
      errors: errors,
      registrationForm: registration,
    });
  },
});

export default accountStore;
