import { Module } from '@nestjs/common';
import { AuthModule } from './auth/auth.module';
import { CaslModule } from './casl/casl.module';
import { ConfigModuleSetup } from './externalModules';
import { ThrottlerModuleSetup } from './externalModules/throttle.module';
import { MailModule } from './mail/mail.module';
import { MinioClientModule } from './minio-client/minio-client.module';
import { PostModule } from './post/post.module';
import { PrismaModule } from './prisma/prisma.module';
import { UserModule } from './user/user.module';
import { FileModule } from './file/file.module';

@Module({
	imports: [
		AuthModule,
		UserModule,
		PrismaModule,
		MailModule,
		ConfigModuleSetup,
		ThrottlerModuleSetup,
		CaslModule,
		PostModule,
		MinioClientModule,
		FileModule,
	],
	controllers: [],
	providers: [],
})
export class AppModule {}
