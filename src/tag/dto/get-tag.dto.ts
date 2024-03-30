import { IsNotEmpty, IsString } from 'class-validator';

export class GetTagDto {
	@IsString()
	@IsNotEmpty()
	name: string;
}
