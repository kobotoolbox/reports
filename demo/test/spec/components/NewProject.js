'use strict';

// Uncomment the following lines to use the react test utilities
// import React from 'react/addons';
// const TestUtils = React.addons.TestUtils;

import createComponent from 'helpers/createComponent';
import NewProject from 'components/NewProject.js';

describe('NewProject', () => {
    let NewProjectComponent;

    beforeEach(() => {
        NewProjectComponent = createComponent(NewProject);
    });

    it('should have its component name as default className', () => {
        expect(NewProjectComponent._store.props.className).toBe('NewProject');
    });
});
