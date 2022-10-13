import { Module } from '@nestjs/common';
import { CaslModule } from '../casl/casl.module';
import { PrismaModule } from '../prisma/prisma.module';
import { PostController } from './post.controller';
import { PostService } from './post.service';

@Module({
	imports: [PrismaModule, CaslModule],
	providers: [PostService],
	controllers: [PostController],
})
export class PostModule {}
