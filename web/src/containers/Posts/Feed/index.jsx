import { connect } from 'react-redux';
import {
    postsGet, postsAdd, postsDelete,
} from '../../../redus';

import Feed from './Feed';


// AppContainer.jsx
const mapStateToProps = state => ({
    posts: state.posts,
    online: state.online,
});

const mapDispatchToProps = {
    postsGet, postsAdd, postsDelete,
};

const FeedContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(Feed);

export default FeedContainer;
