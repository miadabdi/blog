import { utilities as nestWinstonModuleUtilities, WinstonModule } from 'nest-winston';
import * as winston from 'winston';
import * as winstonDailyRotateFile from 'winston-daily-rotate-file';

const transports = {
	console: new winston.transports.Console({
		level: 'silly',
		format: winston.format.combine(
			winston.format.timestamp({ format: 'YYYY-MM-DD hh:mm:ss.SSS A' }),
			winston.format.ms(),
			nestWinstonModuleUtilities.format.nestLike('Blog', {
				colors: true,
				prettyPrint: true,
			}),
			// winston.format.printf((info) => {
			// 	return `${info.timestamp} [${info.level}] [${info.context ? info.context : info.stack}] ${
			// 		info.message
			// 	}`;
			// }),
			// winston.format.align(),
		),
	}),
	combinedFile: new winstonDailyRotateFile({
		dirname: 'logs',
		filename: 'combined',
		extension: '.log',
		level: 'info',
		format: winston.format.combine(
			winston.format.timestamp({
				format: 'YYYY-MM-DD hh:mm:ss.SSS A',
			}),
			winston.format.errors({ stack: true }),
			winston.format.splat(),
			winston.format.json(),
		),
	}),
	errorFile: new winstonDailyRotateFile({
		dirname: 'logs',
		filename: 'error',
		extension: '.log',
		level: 'error',
		format: winston.format.combine(
			winston.format.timestamp({
				format: 'YYYY-MM-DD hh:mm:ss.SSS A',
			}),
			winston.format.errors({ stack: true }),
			winston.format.splat(),
			winston.format.json(),
		),
	}),
};

export const logger = WinstonModule.createLogger({
	exitOnError: true,
	transports: [transports.console, transports.combinedFile, transports.errorFile],
});
