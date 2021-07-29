import { connect } from 'react-redux';
import {
    postsGet, postsAdd, postsDelete,
} from '../../../redus';

import Grid from './Grid';


// AppContainer.jsx
const mapStateToProps = state => ({
    system: state.system,
    posts: state.posts,
    online: state.online,
});

const mapDispatchToProps = {
    postsGet, postsAdd, postsDelete,
};

const GridContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(Grid);

export default GridContainer;
