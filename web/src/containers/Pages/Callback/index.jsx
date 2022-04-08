import { connect } from 'react-redux';
import {
    profileIn,
} from '../../../redus';

import Callback from './Callback';


// AppContainer.jsx
const mapStateToProps = state => ({
    system: state.system,
});

const mapDispatchToProps = {
    profileIn,
};

const CallbackContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(Callback);

export default CallbackContainer;
