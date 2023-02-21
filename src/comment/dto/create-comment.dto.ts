import { Type } from 'class-transformer';
import { IsInt, IsNotEmpty, IsOptional, Length } from 'class-validator';

export class CreateCommentDto {
	@IsNotEmpty()
	@Length(3, 500)
	content: string;

	authorId?: number;

	@IsInt()
	@Type(() => Number)
	postId: number;

	@IsOptional()
	@IsInt()
	@Type(() => Number)
	replyTo: number;
}
