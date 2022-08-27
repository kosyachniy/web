import { connect } from 'react-redux';
import {
    changeLang,
    changeTheme,
} from '../../../redus';

import Footer from './Footer';


// AppContainer.jsx
const mapStateToProps = state => ({
    system: state.system,
});

const mapDispatchToProps = {
    changeLang,
    changeTheme,
};

const FooterContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(Footer);

export default FooterContainer;
