export const getPure = data => data.replace(/<[^>]*br[^>]*>/g, '\n')
  .replace(/<\/[^>]*p[^>]*>/g, '\n')
  .replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, '')
  .trim();

export const getFirst = data => getPure(data).split('\n')[0];

export const getISO = data => new Date(data * 1000).toISOString()
  .replace(/[.]\d+/, '');

export const getTime = data => {
  const d = new Date(data * 1000);
  const yyyy = d.getFullYear();
  const mm = (`0${d.getMonth() + 1}`).slice(-2);
  const dd = (`0${d.getDate()}`).slice(-2);
  const hh = (`0${d.getHours()}`).slice(-2);
  const min = (`0${d.getMinutes()}`).slice(-2);
  return `${dd}.${mm}.${yyyy} ${hh}:${min}`;
};
