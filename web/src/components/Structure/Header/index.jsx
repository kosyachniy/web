import { connect } from 'react-redux';
import {
} from '../../redus';

import Header from './Header';


// AppContainer.jsx
const mapStateToProps = state => ({
	online: state.online,
});

const mapDispatchToProps = {
};

const HeaderContainer = connect(
	mapStateToProps,
	mapDispatchToProps
)(Header);

export default HeaderContainer;
