import { getJsDateFromExcel } from 'excel-date-to-js';
import { getDate } from './date';

export const getExpiresAt = (expiry: string, format: string) => {
  //// return { error: true, message: 'Invalid date.' };
  if (/^\d+$/.test(expiry)) {
    try {
      if (expiry === null || expiry === '') {
        return { error: false, date: null };
      }
      let expires_at = getJsDateFromExcel(parseInt(expiry));
      if (expires_at.toString().includes('NaN')) {
        return { error: true, message: 'Invalid date.' };
      }
      return { error: false, date: getDate(expires_at) };
    } catch (e) {
      return { error: true, message: e.message };
    }
  }
  if (format === 'MM/YY') {
    try {
      if (expiry === null || expiry === '') {
        return { error: false, date: null };
      }
      let parts = expiry.split('/');
      let d = getDate(parts[0] + '/01/' + parts[1]);
      let expires_at = getDate(d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + 0);
      if (expires_at.toString().includes('NaN')) {
        return { error: true, message: 'Invalid date.' };
      }
      return { error: false, date: expires_at };
    } catch (e) {
      return { error: true, message: e.message };
    }
  }
  if (format === 'DD/MM/YYYY') {
    try {
      if (expiry === null || expiry === '') {
        return { error: false, date: null };
      }
      let parts = expiry.split('/');
      let d = getDate(parts[1] + '/' + parts[0] + '/' + parts[2]);
      let expires_at = getDate(d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + 0);
      if (expires_at.toString().includes('NaN')) {
        return { error: true, message: 'Invalid date.' };
      }
      return { error: false, date: expires_at };
    } catch (e) {
      return { error: true, message: e.message };
    }
  }
};
