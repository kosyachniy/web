import { connect } from 'react-redux';

import Auth from './Auth';


// AppContainer.jsx
const mapStateToProps = state => ({
    system: state.system,
});

const AuthContainer = connect(
    mapStateToProps,
)(Auth);

export default AuthContainer;
