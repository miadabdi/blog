import { INestApplication, Injectable, Logger, OnModuleInit } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Prisma, PrismaClient } from '@prisma/client';

export type PrismaService = ReturnType<BasePrismaService['withExtensions']>;
const queryLogger = new Logger('QueryLogger');

@Injectable()
export class BasePrismaService extends PrismaClient implements OnModuleInit {
	private readonly logger = new Logger(BasePrismaService.name);

	constructor(configService: ConfigService) {
		super({
			datasources: {
				db: {
					url: configService.get<string>('DATABASE_URL'),
				},
			},
			log: [
				{
					emit: 'event',
					level: 'query',
				},
			],
		});

		this.$on('query' as never, async (e: Prisma.QueryEvent) => {
			this.logger.debug('Query: ' + e.query);
			this.logger.debug('Params: ' + e.params);
			this.logger.debug('Duration: ' + e.duration + 'ms');
		});
	}

	withExtensions() {
		return this.$extends({
			query: {
				$allModels: {
					async $allOperations({ operation, model, args, query }) {
						const start = performance.now();
						const result = await query(args);
						const end = performance.now();
						const time = end - start;
						queryLogger.debug(`${model}.${operation} took ${time.toFixed(0)} ms`);
						return result;
					},
				},
			},
			result: {
				user: {
					fullName: {
						needs: { firstName: true, lastName: true },
						compute(user) {
							return `${user.firstName} ${user.lastName}`;
						},
					},
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
