import { connect } from 'react-redux';
import {
    profileOut, searching,
} from '../../../redus';

import Header from './Header';


// AppContainer.jsx
const mapStateToProps = state => ({
    system: state.system,
    online: state.online,
    profile: state.profile,
});

const mapDispatchToProps = {
    profileOut,
    searching,
};

const HeaderContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(Header);

export default HeaderContainer;
