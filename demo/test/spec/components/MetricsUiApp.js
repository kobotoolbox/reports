'use strict';

describe('MetricsUiApp', () => {
  let React = require('react/addons');
  let MetricsUiApp, component;

  beforeEach(() => {
    let container = document.createElement('div');
    container.id = 'content';
    document.body.appendChild(container);

    MetricsUiApp = require('components/MetricsUiApp.js');
    component = React.createElement(MetricsUiApp);
  });

  it('should create a new instance of MetricsUiApp', () => {
    expect(component).toBeDefined();
  });
});
