import { ForbiddenError } from '@casl/ability';
import { ForbiddenException, Inject, Injectable, Logger, NotFoundException } from '@nestjs/common';
import { User } from '@prisma/client';
import { CaslAbilityFactory, CaslAction } from '../casl/casl-ability.factory';
import { PRISMA_INJECTION_TOKEN } from '../prisma/prisma.module';
import { PrismaService } from '../prisma/prisma.service';
import { CreateCategoryDto, DeleteCategoryDto, GetCategoryDto, UpdateCategoryDto } from './dto';
import { GetCategoriesByIdDto } from './dto/get-categories-by-id.dto';

@Injectable()
export class CategoryService {
	private readonly logger = new Logger(CategoryService.name);

	constructor(
		@Inject(PRISMA_INJECTION_TOKEN) private prismaService: PrismaService,
		private caslAbilityFactory: CaslAbilityFactory,
	) {}

	async getCategoriesById(getCategoriesByIdDto: GetCategoriesByIdDto) {
		const categories = await this.prismaService.category.findMany({
			where: {
				id: {
					in: getCategoriesByIdDto.ids,
				},
			},
		});

		return categories;
	}

	async createCategory(createCategoryDto: CreateCategoryDto, user: User) {
		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Create, 'Category');
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		const category = await this.prismaService.category.create({
			data: {
				name: createCategoryDto.name,
				...(typeof createCategoryDto.parentId === 'number'
					? {
							parent: {
								connect: { id: createCategoryDto.parentId },
							},
						}
					: {}),
			},
		});

		return category;
	}

	async updateCategory(updateCategoryDto: UpdateCategoryDto, user: User) {
		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Update, 'Category');
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		const category = await this.prismaService.category.findUnique({ where: { id: updateCategoryDto.id } });

		if (!category) throw new NotFoundException('Category not found');

		const updatedCategory = await this.prismaService.category.update({
			where: { id: updateCategoryDto.id },
			data: updateCategoryDto,
		});

		return updatedCategory;
	}

	async deleteCategory(deleteCategoryDto: DeleteCategoryDto, user: User) {
		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Delete, 'Category');
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		const category = await this.prismaService.category.findUnique({ where: { id: deleteCategoryDto.id } });

		if (!category) throw new NotFoundException('Category not found');

		await this.prismaService.category.delete({
			where: { id: deleteCategoryDto.id },
		});

		return 'ok';
	}

	async getCategory(getCategoryDto: GetCategoryDto) {
		const categories = await this.prismaService.category.findMany({
			where: {
				name: {
					contains: getCategoryDto.name,
				},
			},
		});

		return categories;
	}
}
