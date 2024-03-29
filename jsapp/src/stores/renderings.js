import Reflux from 'reflux-react-16';
import actions from '../actions/actions';
import $ from 'jquery';
import alertify from 'alertifyjs';

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
    this.listenTo(actions.deleteRendering.completed, this.deleteRenderingCompleted);
    this.listenTo(actions.deleteRendering.failed, this.deleteRenderingFailed);
  },
  listRenderingsCompleted (data) {
    data = data.sort((a, b) => a.name.localeCompare(b.name));
    this.state.projects = data;
    this.state.projectsLoading = false;
    this.trigger(this.state);
  },
  listRenderingsFailed () {
    this.trigger({
      errorMessage: 'listing renderings failed',
    });
  },
  deleteRenderingCompleted () {
    this.state.projects = [];
    this.state.projectsLoading = true;
    this.state.modalIsOpen = false;
    this.trigger(this.state);
    actions.listRenderings();
  },
  deleteRenderingFailed () {
    this.state.modalIsOpen = false;
    alertify.error('failed to delete survey');
    this.trigger(this.state);
  }
});

var individualRenderingStore = Reflux.createStore({
  init () {
    this.listenTo(actions.getRendering.completed, this.getRenderingCompleted);
  },
  getRenderingCompleted (id, html) {
    this.trigger(id, $('<div>').html(html).find('div').get(0).innerHTML);
  },
});

export {
  renderingsStore,
  individualRenderingStore,
};
