class RegistrationForm {
  constructor () {
    this.state = {
      name: '',
      password: '',
      username: '',
      organization: '',
      email: '',
      errors: {},
    };
    this._hasBeenEdited = {};
    this.enabled = true;
    this._isBlurred = {};
  }
  _fieldRequired (name, value) {
    return function() {
      if (value.length === 0) {
        return `${name} required`;
      }
    };
  }
  setError (fld, errMsg) {
    this.state.errors[fld] = errMsg;
  }
  updateField(whichField, value, isBlurEvent) {
    if (value) {
      this._hasBeenEdited[whichField] = true;
    }

    var errMsg = {
      name: this._fieldRequired(whichField, value),
      username: this._fieldRequired(whichField, value),
      password: this._fieldRequired(whichField, value),
      organization: this._fieldRequired(whichField, value),
      email: () => {
        if (isBlurEvent && !value.match(/@/)) {
          return 'invalid email address';
        }
      },
    }[whichField](value);

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
