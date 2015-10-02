import Reflux from 'reflux';

var actions = Reflux.createActions({
/*
  register: {
    asyncResult: true,
    children: [],
  },
  login: {
    asyncResult: true,
  },
  generateReport: {
    asyncResult: true,
  },
*/
  placeholder: {
    asyncResult: true,
  }
});

actions.placeholder.listen(function(desc){
  console.log(`placeholder action called: '${desc}'`);
});

export default actions;
