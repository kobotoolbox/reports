'use strict';

// Uncomment the following lines to use the react test utilities
// import React from 'react/addons';
// const TestUtils = React.addons.TestUtils;

import createComponent from 'helpers/createComponent';
import ProjectList from 'components/ProjectList.js';

describe('ProjectList', () => {
    let ProjectListComponent;

    beforeEach(() => {
        ProjectListComponent = createComponent(ProjectList);
    });

    it('should have its component name as default className', () => {
        expect(ProjectListComponent._store.props.className).toBe('ProjectList');
    });
});
