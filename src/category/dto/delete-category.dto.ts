import { PickType } from '@nestjs/swagger';
import { UpdateCategoryDto } from './update-category.dto';

export class DeleteCategoryDto extends PickType(UpdateCategoryDto, ['id']) {}
