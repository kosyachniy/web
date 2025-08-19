export const profileIn = ({
  id,
  login,
  image,
  name,
  surname,
  title,
  phone,
  mail,
  social,
  status,
}) => ({
  type: 'PROFILE_IN',
  id,
  login,
  image,
  name,
  surname,
  title,
  phone,
  mail,
  social,
  status,
});

export const profileOut = () => ({
  type: 'PROFILE_OUT',
});

export const profileUpdate = (profile) => ({
  type: 'PROFILE_UPDATE',
  profile,
});
