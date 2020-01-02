import { connect } from 'react-redux';
import {
	onlineAdd, onlineDelete, onlineReset,
} from '../../redus';

import Body from './Body';


// AppContainer.jsx
const mapStateToProps = state => ({
	online: state.online,
});

const mapDispatchToProps = {
	onlineAdd, onlineDelete, onlineReset,
};

const BodyContainer = connect(
	mapStateToProps,
	mapDispatchToProps
)(Body);

export default BodyContainer;
