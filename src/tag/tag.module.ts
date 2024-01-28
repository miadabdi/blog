import { Module } from '@nestjs/common';
import { CaslModule } from '../casl/casl.module';
import { TagController } from './tag.controller';
import { TagService } from './tag.service';

@Module({
	imports: [CaslModule],
	providers: [TagService],
	controllers: [TagController],
})
export class TagModule {}
