import { connect } from 'react-redux';
import {
	postsGet, postsAdd, postsDelete,
} from '../redus';

import Posts from './Posts';


// AppContainer.jsx
const mapStateToProps = state => ({
	posts: state.posts,
});

const mapDispatchToProps = {
	postsGet, postsAdd, postsDelete,
};

const PostsContainer = connect(
	mapStateToProps,
	mapDispatchToProps
)(Posts);

export default PostsContainer;
