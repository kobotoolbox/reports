import Reflux from 'reflux';
import actions from '../actions/actions';
import $ from 'jquery';

/*
var projects = [
  {name: 'a1', dateCreated: new Date(), submissions: 2, enterDataLink: '1234'},
  {name: 'a2', dateCreated: new Date(), submissions: 3, enterDataLink: '1234'},
  {name: 'a3', dateCreated: new Date(), submissions: 4, enterDataLink: '1234'},
  {name: 'a4', dateCreated: new Date(), submissions: 2, enterDataLink: '1234'},
];
*/

var renderingsStore = Reflux.createStore({
  init () {
    this.state = {
      projects: [],
      syncingProject: false,
    };
    this.listenTo(actions.listRenderings.completed, this.listRenderingsCompleted);
    this.listenTo(actions.listRenderings.failed, this.listRenderingsFailed);
  },
  listRenderingsCompleted (data) {
    this.state.projects = data;
    this.state.projectsLoading = false;
    this.trigger(this.state);
  },
  listRenderingsFailed () {
    this.trigger({
      errorMessage: 'listing renderings failed',
    });
  },
});

var individualRenderingStore = Reflux.createStore({
  init () {
    this.listenTo(actions.getRendering.completed, this.getRenderingCompleted);
  },
  getRenderingCompleted (id, html) {
    this.trigger(id, $('<div>').html(html).find('div').get(0).innerHTML);
  },
});

export default {
  renderingsStore: renderingsStore,
  individualRenderingStore: individualRenderingStore,
};
