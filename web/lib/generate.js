export default (length = 32) => {
  const symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'.split('');
  const token = [];

  for (let i = 0; i < length; i += 1) {
    const j = (Math.random() * (symbols.length - 1)).toFixed(0);
    token[i] = symbols[j];
  }

  return token.join('');
};
