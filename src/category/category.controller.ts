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
import { CategoryService } from './category.service';
import { CreateCategoryDto, DeleteCategoryDto, GetCategoryDto, UpdateCategoryDto } from './dto';

@UseGuards(ThrottlerGuard)
@Throttle({ default: { limit: 1200, ttl: 60 * 10 } }) // 1200 auth requests for 10 minutes
@Controller({ path: 'category', version: '1' })
// @UseGuards(JwtAuthGuard)
export class CategoryController {
	constructor(private readonly categoryService: CategoryService) {}

	@UseGuards(JwtAuthGuard)
	@HttpCode(HttpStatus.CREATED)
	@Post()
	createCategory(@Body() createCategoryDto: CreateCategoryDto, @GetUser() user: User) {
		return this.categoryService.createCategory(createCategoryDto, user);
	}

	@UseGuards(JwtAuthGuard)
	@HttpCode(HttpStatus.OK)
	@Patch()
	updateCategory(@Body() updateCategoryDto: UpdateCategoryDto, @GetUser() user: User) {
		return this.categoryService.updateCategory(updateCategoryDto, user);
	}

	@UseGuards(JwtAuthGuard)
	@HttpCode(HttpStatus.NO_CONTENT)
	@Delete()
	deleteCategory(@Query() deleteCategoryDto: DeleteCategoryDto, @GetUser() user: User) {
		return this.categoryService.deleteCategory(deleteCategoryDto, user);
	}

	@HttpCode(HttpStatus.OK)
	@Get()
	getCategory(@Query() getCategoryDto: GetCategoryDto) {
		return this.categoryService.getCategory(getCategoryDto);
	}
}
