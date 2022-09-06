import { OmitType, PartialType } from '@nestjs/mapped-types';
import { IsOptional, IsString, Length } from 'class-validator';
import { AuthDto } from '../../auth/dto';

export class UpdateUserDto extends PartialType(
  OmitType(AuthDto, ['password'] as const),
) {
  @IsOptional()
  @IsString()
  @Length(3, 50)
  firstName?: string;

  @IsOptional()
  @IsString()
  @Length(3, 50)
  lastName?: string;
}
