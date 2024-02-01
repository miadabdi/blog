import { Global, Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { BasePrismaService, PrismaService } from './prisma.service';

export const PRISMA_INJECTION_TOKEN = 'PrismaService';

@Global()
@Module({
	providers: [
		{
			provide: PRISMA_INJECTION_TOKEN,
			useFactory(configService: ConfigService): PrismaService {
				return new BasePrismaService(configService).withExtensions();
			},
			inject: [ConfigService],
		},
	],
	exports: [PRISMA_INJECTION_TOKEN],

	// providers: [PrismaService],
	// exports: [PrismaService],
})
export class PrismaModule {}
