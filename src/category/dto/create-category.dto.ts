import { Type } from 'class-transformer';
import { IsInt, IsOptional, IsString, Length, Min } from 'class-validator';

export class CreateCategoryDto {
	@IsString()
	@Length(3, 50)
	name: string;

	@IsOptional()
	@IsInt()
	@Min(0)
	@Type(() => Number)
	parentId?: number;
}
