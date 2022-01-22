import { connect } from 'react-redux';
import {
    profileIn,
} from '../../../redus';

import Mail from './Mail';


// AppContainer.jsx
const mapStateToProps = state => ({
    system: state.system,
});

const mapDispatchToProps = {
    profileIn,
};

const MailContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(Mail);

export default MailContainer;
