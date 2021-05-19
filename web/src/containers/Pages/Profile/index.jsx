import { connect } from 'react-redux';
import {
    profileUpdate,
} from '../../../redus';

import Profile from './Profile';


// AppContainer.jsx
const mapStateToProps = state => ({
    profile: state.profile,
});

const mapDispatchToProps = {
    profileUpdate,
};

const ProfileContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(Profile);

export default ProfileContainer;
