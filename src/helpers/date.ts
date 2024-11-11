import Timestamp = require('timestamp-nano');
export const getDate = (value) => {
  return new Date(value);
};
export const getCurrentDate = () => {
  return new Date();
  // return new Date(new Date().toLocaleString('en-US', { timeZone: '' }));
};
export const getTime = (value) => {
  return new Date(value).getTime();
};
export const getCurrentTime = () => {
  return new Date().getTime();
};
export const getTimestamp = (value) => {
  return Timestamp.fromDate(new Date(value)).toJSON();
};
export const getCurrentTimestamp = () => {
  return Timestamp.fromDate(new Date()).toJSON();
};

export const isValidDate = (value) => {
  if (
    value &&
    value !== null &&
    value !== '' &&
    !value.toString().includes('NaN') &&
    !value.toString().includes('Invalid Date')
  ) {
    return true;
  }
  return !isNaN(Date.parse(value));
};

export function getFormattedDayDateMonthYearTime(value) {
  if (value === null || value === '') {
    return '';
  }
  const timeLang = 'en-US';
  return new Date(value).toLocaleString(timeLang, {
    weekday: 'short',
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
  });
  // return new Date(value).toLocaleString(timeLang, { timeZone: timeZone, weekday: 'short', day: '2-digit', month: 'short', year: 'numeric', hour: 'numeric', minute: 'numeric' });
}

export function randomDate(start, end) {
  return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()))
    .toISOString()
    .slice(0, 10);
}
