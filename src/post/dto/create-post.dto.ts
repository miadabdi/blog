import { Expose, Transform, TransformFnParams, Type } from 'class-transformer';
import {
	Allow,
	ArrayNotEmpty,
	IsArray,
	IsInt,
	IsNotEmpty,
	IsNotEmptyObject,
	IsObject,
	IsOptional,
	IsString,
	Length,
} from 'class-validator';
import slugify from 'slugify';

export class CreatePostDto {
	@IsString()
	@IsNotEmpty()
	@Length(3, 200)
	name: string;

	@Expose()
	@Allow()
	@Transform((param: TransformFnParams) => {
		if (!param.obj.name) return null;

		const slugified = slugify(param.obj.name, {
			replacement: '-', // replace spaces with replacement character, defaults to `-`
			remove: undefined, // remove characters that match regex, defaults to `undefined`
			lower: true, // convert to lower case, defaults to `false`
			strict: true, // strip special characters except replacement, defaults to `false`
			locale: 'vi', // language code of the locale to use
			trim: true, // trim leading and trailing replacement chars, defaults to `true`
		});

		return `${slugified}-${Date.now().toString()}`;
	})
	slug: string;

	@IsString()
	@IsNotEmpty()
	@Length(30, 2000)
	summary: string;

	@IsObject()
	@IsNotEmptyObject()
	@Transform((param: TransformFnParams) => {
		if (typeof param.value === 'string') {
			return JSON.parse(param.value);
		}

		return param.value;
	})
	bodyObj: object;

	@IsOptional()
	@IsInt()
	@Type(() => Number)
	coverImageFileId?: number;

	@IsArray()
	@ArrayNotEmpty()
	@IsInt({ each: true })
	@Type(() => Number)
	categories: number[];
}
