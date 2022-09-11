import { ValidationPipe, VersioningType } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { HttpAdapterHost, NestFactory } from '@nestjs/core';
import * as compression from 'compression';
import * as cookieParser from 'cookie-parser';
import helmet from 'helmet';
import * as hpp from 'hpp';
import * as winston from 'winston';
import * as winstonDailyRotateFile from 'winston-daily-rotate-file';
import { AppModule } from './app.module';
import { API_PREFIX } from './common/constants';
import { AllExceptionsFilter } from './common/exceptions';
import { LoggingInterceptor, TimeoutInterceptor } from './common/interceptors';
import { PrismaService } from './prisma/prisma.service';

const transports = {
	console: new winston.transports.Console({
		level: 'silly',
		format: winston.format.combine(
			winston.format.timestamp({
				format: 'YYYY-MM-DD HH:mm:ss',
			}),
			winston.format.colorize({
				colors: {
					info: 'blue',
					debug: 'yellow',
					error: 'red',
				},
			}),
			winston.format.printf((info) => {
				return `${info.timestamp} [${info.level}] [${info.context ? info.context : info.stack}] ${
					info.message
				}`;
			}),
			// winston.format.align(),
		),
	}),
	combinedFile: new winstonDailyRotateFile({
		dirname: 'logs',
		filename: 'combined',
		extension: '.log',
		level: 'info',
	}),
	errorFile: new winstonDailyRotateFile({
		dirname: 'logs',
		filename: 'error',
		extension: '.log',
		level: 'error',
	}),
};
console.log('about to write a log ////////////////////////////////////////');

async function bootstrap() {
	// const logger = WinstonModule.createLogger({
	// 	exitOnError: true,
	// 	levels: LOG_LEVELS,
	// 	format: winston.format.combine(
	// 		winston.format.timestamp({
	// 			format: 'YYYY-MM-DD HH:mm:ss',
	// 		}),
	// 		winston.format.errors({ stack: true }),
	// 		winston.format.splat(),
	// 		winston.format.json(),
	// 	),
	// 	transports: [transports.console, transports.combinedFile, transports.errorFile],
	// });

	console.log('about to write a log');

	const app = await NestFactory.create(AppModule, {
		// bufferLogs: true,
		logger: ['log', 'error', 'warn', 'debug', 'verbose'],
	});

	// app.useLogger(logger);

	const configService = app.get(ConfigService);

	app.use(helmet());
	app.use(
		compression({
			threshold: configService.get<number>('COMPRESSION_THRESHOLD'), // number in bytes
		}),
	);
	app.use(cookieParser());
	app.use(hpp());

	app.enableCors();

	app.useGlobalPipes(
		new ValidationPipe({
			transform: true,
			whitelist: true,
		}),
	);
	app.setGlobalPrefix(API_PREFIX);

	app.enableVersioning({
		type: VersioningType.URI,
		defaultVersion: '1',
	});

	app.useGlobalInterceptors(new LoggingInterceptor(), new TimeoutInterceptor());

	const { httpAdapter } = app.get(HttpAdapterHost);
	app.useGlobalFilters(new AllExceptionsFilter(httpAdapter));

	const port = configService.get<number>('PORT');
	await app.listen(port);

	const prismaService = app.get(PrismaService);
	await prismaService.enableShutdownHooks(app);
}
bootstrap();
