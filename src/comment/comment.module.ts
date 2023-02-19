import { Module } from '@nestjs/common';
import { CaslModule } from '../casl/casl.module';
import { CommentController } from './comment.controller';
import { CommentService } from './comment.service';

@Module({
	imports: [CaslModule],
	controllers: [CommentController],
	providers: [CommentService],
})
export class CommentModule {}
