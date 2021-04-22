// converted from "react-identicon": "^1.0.2" (uses ES7, not supported)
import React from 'react';
import md5 from 'md5';
import assign from 'react/lib/Object.assign';

class Identicon extends React.Component {
  constructor () {
    this.displayName = 'Identicon';
  }
  getDefaultProps () {
    return {
      id: '',
      type: 'identicon',
      size: 80,
    };
  },
  propTypes: {
    id: React.PropTypes.any,
    size: React.PropTypes.number,
    type: React.PropTypes.string,
  },
  componentDidMount () {
    this._Props = assign({}, this.props);
    this._idTypeSize = {
      id: this.props.id,
      type: this.props.type,
      size: this.props.size,
    };
    delete this._Props.id;
    delete this._Props.type;
    delete this._Props.size;
  },
  render () {
    var { id, type, size } = this.props;
    var gUrl = `//www.gravatar.com/avatar/${md5(id)}?d=${type}&f=y&s=${size}`;
    return (
        <img src={gUrl} {...this._Props} className='identicon' />
      );
  }
}

export default Identicon;
