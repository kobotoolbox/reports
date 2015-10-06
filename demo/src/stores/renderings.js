import Reflux from 'reflux';
import actions from '../actions/actions';

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
    this.state = {};
    this.listenTo(actions.listRenderings.completed, this.listRenderingsCompleted);
    this.listenTo(actions.listRenderings.failed, this.listRenderingsFailed);
  },
  listRenderingsCompleted () {
    console.log('list renderings completed');
    this.state.projects = projects;
    this.trigger(this.state);
  },
  listRenderingsFailed () {
    console.log('list renderings failed');
  },
});

export default renderingsStore;
