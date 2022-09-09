import { LogLevel } from '@nestjs/common';

export const JWT_COOKIE_NAME = 'access_token';
export const JWT_STRATEGY_NAME = 'jwt';
export const ROUTE_TIMEOUT = 30000;
export const LOG_LEVELS = [
  'error',
  'warn',
  'log',
  'debug',
  'verbose',
] as LogLevel[];
export const API_PREFIX = 'api';
