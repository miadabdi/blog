import { IsNotEmpty, IsString, Length } from 'class-validator';

export class GetPostBySlugDto {
	@IsString()
	@IsNotEmpty()
	@Length(3)
	slug: string;
}
