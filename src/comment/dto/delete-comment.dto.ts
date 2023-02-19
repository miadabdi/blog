import { Type } from 'class-transformer';
import { IsInt } from 'class-validator';

export class DeleteCommentDto {
	@IsInt()
	@Type(() => Number)
	id: number;
}
