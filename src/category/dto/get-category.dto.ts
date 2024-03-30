import { IsNotEmpty, IsString } from 'class-validator';

export class GetCategoryDto {
	@IsString()
	@IsNotEmpty()
	name: string;
}
