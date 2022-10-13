import { Module } from '@nestjs/common';
import { PrismaModule } from '../prisma/prisma.module';
import { PostController } from './post.controller';
import { PostService } from './post.service';

@Module({
	imports: [PrismaModule],
	providers: [PostService],
	controllers: [PostController],
})
export class PostModule {}
