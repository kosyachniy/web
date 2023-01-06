export const postsGet = posts => ({
    type: 'POSTS_GET',
    posts,
})

export const postsAdd = post => ({
    type: 'POSTS_ADD',
    post,
})

export const postsEdit = post => ({
    type: 'POSTS_EDIT',
    post,
})

export const postsDelete = id => ({
    type: 'POSTS_DELETE',
    id,
})
