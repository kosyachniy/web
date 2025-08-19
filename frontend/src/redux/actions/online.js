export const onlineAdd = (online) => ({
  type: 'ONLINE_ADD',
  count: online.count,
  users: online.users,
});

export const onlineDelete = (online) => ({
  type: 'ONLINE_DELETE',
  count: online.count,
  ids: online.users.map((user) => user.id),
});

export const onlineReset = () => ({
  type: 'ONLINE_RESET',
});
