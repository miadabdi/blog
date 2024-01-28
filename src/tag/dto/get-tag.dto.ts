import { PickType } from '@nestjs/swagger';
import { UpdateTagDto } from './update-tag.dto';

export class GetTagDto extends PickType(UpdateTagDto, ['name']) {}
