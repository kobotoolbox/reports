'use strict';

// Uncomment the following lines to use the react test utilities
// import React from 'react/addons';
// const TestUtils = React.addons.TestUtils;

import createComponent from 'helpers/createComponent';
import GettingStarted from 'components/GettingStarted.js';

describe('GettingStarted', () => {
    let GettingStartedComponent;

    beforeEach(() => {
        GettingStartedComponent = createComponent(GettingStarted);
    });

    it('should have its component name as default className', () => {
        expect(GettingStartedComponent._store.props.className).toBe('GettingStarted');
    });
});
