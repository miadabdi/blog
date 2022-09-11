import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { ThrottlerModule } from '@nestjs/throttler';
import * as Joi from 'joi';

import { AuthModule } from './auth/auth.module';
import { NodeEnv } from './common/enums';
import { PrismaModule } from './prisma/prisma.module';
import { UserModule } from './user/user.module';

@Module({
	imports: [
		AuthModule,
		UserModule,
		PrismaModule,
		ConfigModule.forRoot({
			envFilePath: '.env',
			isGlobal: true,
			cache: true,
			validationSchema: Joi.object({
				DATABASE_URL: Joi.string().min(1).required(),
				JWT_SECRET: Joi.string().min(1).required(),
				JWT_EXPIRES_IN: Joi.number().min(1).default(90),
				NODE_ENV: Joi.string()
					.valid(...Object.values(NodeEnv))
					.required(),
				PORT: Joi.number().min(1024).default(3000),
				COOKIE_EXPIRES_IN: Joi.number().min(1).default(90),
				THROTTLE_TTL: Joi.number().min(1).default(60),
				THROTTLE_LIMIT: Joi.number().min(1).default(3600),
				COMPRESSION_THRESHOLD: Joi.number().min(1024).max(100000).default(4096),
			}),
		}),
		ThrottlerModule.forRootAsync({
			imports: [ConfigModule],
			inject: [ConfigService],
			useFactory: (config: ConfigService) => ({
				ttl: config.get<number>('THROTTLE_TTL') * 60,
				limit: config.get<number>('THROTTLE_LIMIT'),
			}),
		}),
	],
	controllers: [],
	providers: [],
})
export class AppModule {}
