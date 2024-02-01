import { ValidationPipe, VersioningType } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { HttpAdapterHost, NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import * as compression from 'compression';
import * as cookieParser from 'cookie-parser';
import helmet from 'helmet';
import * as hpp from 'hpp';
import { AppModule } from './app.module';
import { API_PREFIX } from './common/constants';
import { AllExceptionsFilter } from './common/exceptions';
import { PrismaClientExceptionFilter } from './common/exceptions/prisma-known-exceptions.filter';
import { LoggingInterceptor, TimeoutInterceptor } from './common/interceptors';
import { PRISMA_INJECTION_TOKEN } from './prisma/prisma.module';
import { logger } from './winston';

async function bootstrap() {
	const app = await NestFactory.create(AppModule, {
		logger,
	});

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
	app.useGlobalFilters(new PrismaClientExceptionFilter(httpAdapter));
	app.useGlobalFilters(new AllExceptionsFilter(httpAdapter));

	const port = configService.get<number>('PORT');
	await app.listen(port);

	const prismaService = app.get(PRISMA_INJECTION_TOKEN);
	prismaService.enableShutdownHooks(app);
	app.enableShutdownHooks();

	// await prismaService.enableShutdownHooks(app);

	const config = new DocumentBuilder()
		.setTitle('Blog Apis')
		.setDescription('Introducing all APIs of blog')
		.setVersion('1.0')
		.addTag('blog')
		.build();
	const document = SwaggerModule.createDocument(app, config);
	SwaggerModule.setup('api', app, document);
}
bootstrap();
