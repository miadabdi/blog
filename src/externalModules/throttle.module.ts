import { ConfigModule, ConfigService } from '@nestjs/config';
import { ThrottlerModule } from '@nestjs/throttler';

export const ThrottlerModuleSetup = ThrottlerModule.forRootAsync({
	imports: [ConfigModule],
	inject: [ConfigService],
	useFactory: (config: ConfigService) => ({
		ttl: config.get<number>('THROTTLE_TTL') * 60,
		limit: config.get<number>('THROTTLE_LIMIT'),
	}),
});
