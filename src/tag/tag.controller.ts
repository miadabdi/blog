import {
	Body,
	Controller,
	Delete,
	Get,
	HttpCode,
	HttpStatus,
	Patch,
	Post,
	Query,
	UseGuards,
} from '@nestjs/common';
import { Throttle, ThrottlerGuard } from '@nestjs/throttler';
import { User } from '@prisma/client';
import { GetUser } from '../common/decorators';
import { JwtAuthGuard } from '../common/guards';
import { CreateTagDto, DeleteTagDto, GetTagDto, UpdateTagDto } from './dto';
import { GetTagsByIdDto } from './dto/get-tags-by-id.dto';
import { TagService } from './tag.service';

@UseGuards(ThrottlerGuard)
@Throttle({ default: { limit: 1200, ttl: 60 * 10 } }) // 1200 auth requests for 10 minutes
@Controller({ path: 'tag', version: '1' })
// @UseGuards(JwtAuthGuard)
export class TagController {
	constructor(private readonly tagService: TagService) {}

	@UseGuards(JwtAuthGuard)
	@HttpCode(HttpStatus.CREATED)
	@Post()
	createTag(@Body() createTagDto: CreateTagDto, @GetUser() user: User) {
		return this.tagService.createTag(createTagDto, user);
	}

	@UseGuards(JwtAuthGuard)
	@HttpCode(HttpStatus.OK)
	@Patch()
	updateTag(@Body() updateTagDto: UpdateTagDto, @GetUser() user: User) {
		return this.tagService.updateTag(updateTagDto, user);
	}

	@UseGuards(JwtAuthGuard)
	@HttpCode(HttpStatus.NO_CONTENT)
	@Delete()
	deleteTag(@Query() deleteTagDto: DeleteTagDto, @GetUser() user: User) {
		return this.tagService.deleteTag(deleteTagDto, user);
	}

	@HttpCode(HttpStatus.OK)
	@Get()
	getTag(@Query() getTagDto: GetTagDto) {
		return this.tagService.getTag(getTagDto);
	}

	@HttpCode(HttpStatus.OK)
	@Get()
	getTagsById(@Query() getTagsByIdDto: GetTagsByIdDto) {
		return this.tagService.getTagsById(getTagsByIdDto);
	}
}
