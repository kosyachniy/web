export default (state = [], action) => {
    switch (action.type) {
        case 'POSTS_GET':
            return action.posts

        case 'POSTS_ADD':
            return [
                action.post,
                ...state
            ]

        case 'POSTS_EDIT':
            return state.map(post => {
                if (post.id === action.post.id) {
                    ['title', 'data'].map(el => {
                        if (el in action.post) {
                            post[el] = action.post[el]
                        }

                        return null
                    })
                }

                return post
            })

        case 'POSTS_DELETE':
            return state.filter(note => note.id !== action.id)

        default:
            return state
    }
}
