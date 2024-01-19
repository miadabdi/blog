import { INestApplication, Injectable, Logger, OnModuleInit } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
	private readonly logger = new Logger(PrismaService.name);

	constructor(configService: ConfigService) {
		super({
			datasources: {
				db: {
					url: configService.get<string>('DATABASE_URL'),
				},
			},
		});
	}

	async onModuleInit() {
		await this.$connect();
		this.logger.log('Database connected');
	}

	async enableShutdownHooks(app: INestApplication) {
		process.on('beforeExit', async () => {
			await app.close();
		});
	}

	async cleanDB() {
		await this.$transaction([this.user.deleteMany()]);
		this.logger.log('DB data cleaned');
	}
}
