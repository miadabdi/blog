import { PartialType, PickType } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsInt } from 'class-validator';
import { CreateCommentDto } from './create-comment.dto';

export class UpdateCommentDto extends PartialType(PickType(CreateCommentDto, ['content'] as const)) {
	@IsInt()
	@Type(() => Number)
	id: number;
}
