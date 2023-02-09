export const getPure = data => data.replace(/<[^>]*br[^>]*>/g, '\n')
  .replace(/<\/[^>]*p[^>]*>/g, '\n')
  .replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, '')
  .trim();

export const getFirst = data => getPure(data).split('\n')[0];

export const getISO = data => new Date(data * 1000).toISOString()
  .replace(/[.]\d+/, '');
