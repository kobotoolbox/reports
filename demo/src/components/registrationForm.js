var validators = (function(){
  function _fieldRequired(fieldName, value) {
    if (value.length === 0) {
      return `${fieldName} required`;
    }
  }
  function _fieldRequiredPasswordMatch(fieldName, value) {
    if (value.length === 0) {
      return `${fieldName} required`;
    }
  }

  return {
    first_name: _fieldRequired,
    last_name: _fieldRequired,
    username: _fieldRequired,
    password: _fieldRequiredPasswordMatch,
    password_confirmation: _fieldRequiredPasswordMatch,
    organization: _fieldRequired,
    email: function (fieldName, value, isBlurEvent) {
      if (isBlurEvent && !value.match(/@/)) {
        return 'invalid email address';
      }
    },
  };
})();

class RegistrationForm {
  constructor () {
    this.state = {
      first_name: '',
      last_name: '',
      password: '',
      password_confirmation: '',
      username: '',
      organization: '',
      email: '',
      errors: {},
    };
    this._hasBeenEdited = {};
    this.enabled = true;
    this._isBlurred = {};
  }
  setError (fld, errMsg) {
    this.state.errors[fld] = errMsg;
  }
  updateField(whichField, value, isBlurEvent) {
    if (value) {
      this._hasBeenEdited[whichField] = true;
    }

    var errMsg, validator = validators[whichField];
    if (validator) {
      errMsg = validator.call(this, whichField, value, isBlurEvent);
    }

    this._isBlurred[whichField] = isBlurEvent;

    if (!this._hasBeenEdited[whichField]) {
      return;
    } else if (errMsg) {
      this.state.errors[whichField] = errMsg;
    } else {
      this.state.errors[whichField] = false;
    }
    this.state[whichField] = value;
  }
}

export var registration = new RegistrationForm();
