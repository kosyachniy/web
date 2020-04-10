import { connect } from 'react-redux';
import {
	changeTheme,
} from '../../redus';

import Header from './Header';


// AppContainer.jsx
const mapStateToProps = state => ({
	system: state.system,
	online: state.online,
	profile: state.profile,
});

const mapDispatchToProps = {
	changeTheme,
};

const HeaderContainer = connect(
	mapStateToProps,
	mapDispatchToProps
)(Header);

export default HeaderContainer;
