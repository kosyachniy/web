import { connect } from 'react-redux';

import Online from './Online';


// AppContainer.jsx
const mapStateToProps = state => ({
	online: state.online,
});

const mapDispatchToProps = {
	// profileIn,
};

const OnlineContainer = connect(
	mapStateToProps,
	mapDispatchToProps
)(Online);

export default OnlineContainer;
