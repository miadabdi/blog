import { Module } from '@nestjs/common';
import { CaslModule } from '../casl/casl.module';
import { CategoryController } from './category.controller';
import { CategoryService } from './category.service';

@Module({
	imports: [CaslModule],
	providers: [CategoryService],
	controllers: [CategoryController],
	exports: [CategoryService],
})
export class CategoryModule {}
