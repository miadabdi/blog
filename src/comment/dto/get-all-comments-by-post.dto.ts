import { Type } from 'class-transformer';
import { IsInt } from 'class-validator';

export class GetAllCommentsOfPost {
	@IsInt()
	@Type(() => Number)
	postId: number;
}
