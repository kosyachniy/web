import { connect } from 'react-redux';

import Online from './Online';


// AppContainer.jsx
const mapStateToProps = state => ({
    system: state.system,
    online: state.online,
});

const OnlineContainer = connect(
    mapStateToProps,
)(Online);

export default OnlineContainer;
