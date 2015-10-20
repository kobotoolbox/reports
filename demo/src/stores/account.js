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
    this.state.created = data;
    this.trigger(this.state);
  },
  registerAccountFailed (jqxhr) {
    var responseJSON = jqxhr.responseJSON;
    Object.keys(responseJSON).forEach((errKey) => {
      var err = responseJSON[errKey];
      if (err instanceof Array && err.length === 1) {
        err = err[0];
      }
      registration.setError(errKey, err);
    });
    this.trigger({
      errors: responseJSON,
      registrationForm: registration,
    });
  },
});

export default accountStore;
