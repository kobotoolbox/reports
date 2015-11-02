const PASSWORD_MISMATCH_MESSAGE = 'password and confirmation must match';

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
    var isC = fieldName === 'password_confirmation',
        otherP = isC ? this.state.password : this.state.password_confirmation;
    var bothDefined = value && otherP;
    if (bothDefined && value !== otherP) {
      return PASSWORD_MISMATCH_MESSAGE;
    } else {
      // if no error, then we can reset password related errors
      this.state.errors[isC ? 'password' : 'password_confirmation'] = false;
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
    this.enabled = true;
    this._isBlurred = {};
  }
  setError (fld, errMsg) {
    this.state.errors[fld] = errMsg;
  }
  isValid () {
    for (var key in this.state.errors) {
      if (this.state.errors[key]) {
        return false;
      }
    }
    return true;
  }
  getData () {
    var data = {};
    Object.keys(this.state).forEach((key) => {
      if (key !== 'errors') {
        data[key] = this.state[key];
      }
    });
    return data;
  }
  updateField(whichField, value, isBlurEvent) {
    var errMsg, validator = validators[whichField];
    if (validator) {
      errMsg = validator.call(this, whichField, value, isBlurEvent);
    }

    this._isBlurred[whichField] = isBlurEvent;

    if (errMsg) {
      this.state.errors[whichField] = errMsg;
    } else {
      this.state.errors[whichField] = false;
    }
    this.state[whichField] = value;
  }
}

export var registration = new RegistrationForm();
