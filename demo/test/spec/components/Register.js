'use strict';

// Uncomment the following lines to use the react test utilities
// import React from 'react/addons';
// const TestUtils = React.addons.TestUtils;

import createComponent from 'helpers/createComponent';
import Register from 'components/Register.js';

describe('Register', () => {
    let RegisterComponent;

    beforeEach(() => {
        RegisterComponent = createComponent(Register);
    });

    it('should have its component name as default className', () => {
        expect(RegisterComponent._store.props.className).toBe('Register');
    });
});
