import { IsArray, IsInt } from 'class-validator';

export class GetCategoriesByIdDto {
	@IsArray()
	@IsInt({ each: true })
	ids: number[];
}
