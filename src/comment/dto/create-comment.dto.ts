import { Type } from 'class-transformer';
import { IsInt, IsNotEmpty, Length } from 'class-validator';

export class CreateCommentDto {
	@IsNotEmpty()
	@Length(3, 500)
	content: string;

	authorId?: number;

	@IsInt()
	@Type(() => Number)
	postId: number;
}
