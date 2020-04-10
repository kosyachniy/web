import { connect } from 'react-redux';
import {
} from '../../../redus';

import Footer from './Footer';


// AppContainer.jsx
const mapStateToProps = state => ({
	system: state.system,
});

const mapDispatchToProps = {
};

const FooterContainer = connect(
	mapStateToProps,
	mapDispatchToProps
)(Footer);

export default FooterContainer;
