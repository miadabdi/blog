import { Type } from 'class-transformer';
import { IsInt } from 'class-validator';

export class DeletePostDto {
	@IsInt()
	@Type(() => Number)
	id: number;
}
