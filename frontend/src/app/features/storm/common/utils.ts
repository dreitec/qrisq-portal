import moment from 'moment';
import { WindDirectionAndDegrees } from './constants';

function toCDT(utc: string): string {
  return moment.utc(utc).utcOffset(-5).format('ddd MMM D YYYY, hA');
}

function toIssuedDate(utc: string): string {
  const date = new Date();
  const offset = date.getTimezoneOffset() / 60;
  const timezone = new Date().toString().match(/\(([A-Z\s].*)\)/)[1];
  return `${moment.utc(utc).utcOffset(-offset).format('MMM D, hh:mm A')} ${timezone.replace(/[^A-Z]/g, '')}`;
}

function toDefaultDate(date: Date): string {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  return `${year}-${month > 9 ? month : '0' + month.toString()}-${day > 9 ? day : '0' + day.toString()}`;
}

export function getESRISurgeLevelColor(depth: number) {
  if (depth < 1) {
    return '#004343';
  }
  if (depth < 1.5) {
    return '#00fefe';
  }
  if (depth < 2) {
    return '#00d0a2';
  }
  if (depth < 2.5) {
    return '#00a245';
  }
  if (depth < 3) {
    return '#ffff00';
  }
  if (depth < 3.5) {
    return '#ffe600';
  }
  if (depth < 4) {
    return '#ffd300';
  }
  if (depth < 4.5) {
    return '#ffbf00';
  }
  if (depth < 5) {
    return '#ffab00';
  }
  if (depth < 5.5) {
    return '#ff9300';
  }
  if (depth < 6) {
    return '#ff7f00';
  }
  if (depth < 6.5) {
    return '#ff6b00';
  }
  if (depth < 7) {
    return '#ff5600';
  }
  if (depth < 7.5) {
    return '#ff3d00';
  }
  if (depth < 8) {
    return '#ff2900';
  }
  if (depth < 8.5) {
    return '#ff1400';
  }
  if (depth < 9) {
    return '#ff0000';
  }
  if (depth < 9.5) {
    return '#e50000';
  }
  if (depth < 10) {
    return '#d00000';
  }
  if (depth < 10.5) {
    return '#bb0000';
  }
  if (depth < 11) {
    return '#a70000';
  }
  if (depth < 11.5) {
    return '#8d0000';
  }
  if (depth < 12) {
    return '#820082';
  }
  if (depth < 12.5) {
    return '#8c098c';
  }
  if (depth < 13) {
    return '#961296';
  }
  if (depth < 13.5) {
    return '#a31da3';
  }
  if (depth < 14) {
    return '#ad27ad';
  }
  if (depth < 14.5) {
    return '#b730b7';
  }
  if (depth < 15) {
    return '#c139c1';
  }
  if (depth < 15.5) {
    return '#ce44ce';
  }
  if (depth < 16) {
    return '#d84dd8';
  }
  if (depth < 16.5) {
    return '#e256e2';
  }
  if (depth >= 16.5) {
    return '#e256e2';
  }
}

export const TimeUtils = { toCDT, toDefaultDate, toIssuedDate };

export function getWindDirection(degree: string) {
  let direction = '';

  WindDirectionAndDegrees.forEach(item => {
    if (item.degreeFrom > item.degreeTo) {
      if ((Number(degree) >= item.degreeFrom) || (Number(degree) <= item.degreeTo)) {
        direction = item.direction;
        return;
      }
    } else {
      if ((Number(degree) >= item.degreeFrom) && (Number(degree) < item.degreeTo)) {
        direction = item.direction;
        return;
      }
    }
  });
  
  return direction;
}

export const getBillingStatus = (start, end) => {
  const nowDate = new Date().toISOString().split('T')[0];
  const startDate = new Date(start).toISOString().split('T')[0];
  const endDate = end ? new Date(end).toISOString().split('T')[0] : '';

  if (nowDate < startDate) {
    return 0;
  } else {
    if (endDate) {
      if (nowDate > endDate) {
        return -1;
      }
    }
    return 1;
  }
};
