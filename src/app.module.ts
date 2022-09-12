import { Module } from '@nestjs/common';
import { AuthModule } from './auth/auth.module';
import { ConfigModuleSetup } from './externalModules';
import { ThrottlerModuleSetup } from './externalModules/throttle.module';
import { MailModule } from './mail/mail.module';
import { PrismaModule } from './prisma/prisma.module';
import { UserModule } from './user/user.module';

@Module({
	imports: [AuthModule, UserModule, PrismaModule, MailModule, ConfigModuleSetup, ThrottlerModuleSetup],
	controllers: [],
	providers: [],
})
export class AppModule {}
