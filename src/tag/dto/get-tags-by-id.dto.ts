import { IsArray, IsInt } from 'class-validator';

export class GetTagsByIdDto {
	@IsArray()
	@IsInt({ each: true })
	ids: number[];
}
