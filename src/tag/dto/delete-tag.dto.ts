import { PickType } from '@nestjs/swagger';
import { UpdateTagDto } from './update-tag.dto';

export class DeleteTagDto extends PickType(UpdateTagDto, ['id']) {}
