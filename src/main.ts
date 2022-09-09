import { ValidationPipe, VersioningType } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { HttpAdapterHost, NestFactory } from '@nestjs/core';
import * as compression from 'compression';
import * as cookieParser from 'cookie-parser';
import helmet from 'helmet';
import { AppModule } from './app.module';
import { API_PREFIX, LOG_LEVELS } from './common/constants';
import { AllExceptionsFilter } from './common/exceptions';
import { LoggingInterceptor, TimeoutInterceptor } from './common/interceptors';
import { PrismaService } from './prisma/prisma.service';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    logger: LOG_LEVELS,
  });

  app.use(helmet());
  app.use(compression());
  app.use(cookieParser());

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

  const configService = app.get(ConfigService);

  const port = configService.get<number>('PORT');
  await app.listen(port);

  const prismaService = app.get(PrismaService);
  await prismaService.enableShutdownHooks(app);
}
bootstrap();
