import { Module } from '@nestjs/common';
import { CaslModule } from '../casl/casl.module';
import { CategoryModule } from '../category/category.module';
import { PrismaModule } from '../prisma/prisma.module';
import { TagModule } from '../tag/tag.module';
import { PostController } from './post.controller';
import { PostService } from './post.service';

@Module({
	imports: [PrismaModule, CaslModule, CategoryModule, TagModule],
	providers: [PostService],
	controllers: [PostController],
})
export class PostModule {}
