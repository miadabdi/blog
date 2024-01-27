import { PickType } from '@nestjs/swagger';
import { UpdateCategoryDto } from './update-category.dto';

export class GetCategoryDto extends PickType(UpdateCategoryDto, ['name']) {}
