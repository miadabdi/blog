import { ForbiddenError, subject } from '@casl/ability';
import { ForbiddenException, Inject, Injectable, Logger, NotFoundException } from '@nestjs/common';
import { User } from '@prisma/client';
import { CaslAbilityFactory, CaslAction } from '../casl/casl-ability.factory';
import { CategoryService } from '../category/category.service';
import { PRISMA_INJECTION_TOKEN } from '../prisma/prisma.module';
import { PrismaService } from '../prisma/prisma.service';
import { TagService } from '../tag/tag.service';
import { CreatePostDto } from './dto/create-post.dto';
import { DeletePostDto } from './dto/delete-post.dto';
import { GetPostBySlugDto } from './dto/get-post-by-slug.dto';
import { UpdatePostDto } from './dto/update-post.dto';

@Injectable()
export class PostService {
	private logger = new Logger(PostService.name);

	constructor(
		@Inject(PRISMA_INJECTION_TOKEN) private prismaService: PrismaService,
		private caslAbilityFactory: CaslAbilityFactory,
		private tagService: TagService,
		private categoryService: CategoryService,
	) {}

	async createPost(createPostDto: CreatePostDto, user: User) {
		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Create, 'Post');
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		if (createPostDto.coverImageFileId) {
			const file = await this.prismaService.file.findUnique({
				where: {
					id: createPostDto.coverImageFileId,
				},
			});

			if (!file) {
				throw new NotFoundException('Cover image not found');
			}
		}

		if (createPostDto.tags.length > 0) {
			const dbTags = await this.tagService.getTagsById({
				ids: createPostDto.tags,
			});

			for (const tagId of createPostDto.tags) {
				const dbTag = dbTags.find((dbTag) => dbTag.id == tagId);
				if (!dbTag) {
					throw new NotFoundException(`Tag with id ${tagId} is not found.`);
				}
			}
		}

		if (createPostDto.categories.length > 0) {
			const dbCategories = await this.categoryService.getCategoriesById({
				ids: createPostDto.categories,
			});

			for (const categoryId of createPostDto.categories) {
				const dbCategory = dbCategories.find((dbCategory) => dbCategory.id == categoryId);
				if (!dbCategory) {
					throw new NotFoundException(`Category with id ${categoryId} is not found.`);
				}
			}
		}

		const post = await this.prismaService.post.create({
			data: {
				name: createPostDto.name,
				slug: createPostDto.slug,
				bodyObj: createPostDto.bodyObj,
				summary: createPostDto.summary,
				author: {
					connect: { id: user.id },
				},
				categories: {
					create: createPostDto.categories.map((categoryId) => {
						return {
							category: {
								connect: { id: categoryId },
							},
						};
					}),
				},
				tags: {
					create: createPostDto.tags.map((tagId) => {
						return {
							tag: {
								connect: { id: tagId },
							},
						};
					}),
				},
				...(typeof createPostDto.coverImageFileId === 'number'
					? {
							coverImageFile: {
								connect: { id: createPostDto.coverImageFileId },
							},
						}
					: {}),
			},
			include: {
				categories: {
					include: {
						category: true,
					},
				},
				tags: {
					include: {
						tag: true,
					},
				},
			},
		});

		return post;
	}

	async updatePost(updatePostDto: UpdatePostDto, user: User) {
		const post = await this.prismaService.post.findUnique({ where: { id: updatePostDto.id } });

		if (!post) throw new NotFoundException('Post not found');

		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Update, subject('Post', post));
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		if (updatePostDto.coverImageFileId) {
			const file = await this.prismaService.file.findUnique({
				where: {
					id: updatePostDto.coverImageFileId,
				},
			});

			if (!file) {
				throw new NotFoundException('Cover image not found');
			}
		}

		if (updatePostDto.tags.length > 0) {
			const dbTags = await this.tagService.getTagsById({
				ids: updatePostDto.tags,
			});

			for (const tagId of updatePostDto.tags) {
				const dbTag = dbTags.find((dbTag) => dbTag.id == tagId);
				if (!dbTag) {
					throw new NotFoundException(`Tag with id ${tagId} is not found.`);
				}
			}
		}

		if (updatePostDto.categories.length > 0) {
			const dbCategories = await this.categoryService.getCategoriesById({
				ids: updatePostDto.categories,
			});

			for (const categoryId of updatePostDto.categories) {
				const dbCategory = dbCategories.find((dbCategory) => dbCategory.id == categoryId);
				if (!dbCategory) {
					throw new NotFoundException(`Category with id ${categoryId} is not found.`);
				}
			}
		}

		const updatedPost = await this.prismaService.post.update({
			where: { id: updatePostDto.id },
			data: {
				name: updatePostDto.name,
				slug: updatePostDto.slug,
				bodyObj: updatePostDto.bodyObj,
				summary: updatePostDto.summary,
				categories: {
					connectOrCreate: updatePostDto.categories.map((categoryId) => {
						return {
							where: {
								postId_categoryId: {
									categoryId: categoryId,
									postId: updatePostDto.id,
								},
							},
							create: {
								category: {
									connect: { id: categoryId },
								},
							},
						};
					}),
				},
				tags: {
					connectOrCreate: updatePostDto.tags.map((tagId) => {
						return {
							where: {
								postId_tagId: {
									tagId: tagId,
									postId: updatePostDto.id,
								},
							},
							create: {
								tag: {
									connect: { id: tagId },
								},
							},
						};
					}),
				},
				...(typeof updatePostDto.coverImageFileId === 'number'
					? {
							coverImageFile: {
								connect: { id: updatePostDto.coverImageFileId },
							},
						}
					: {}),
			},
			include: {
				categories: {
					include: {
						category: true,
					},
				},
				tags: {
					include: {
						tag: true,
					},
				},
			},
		});

		return updatedPost;
	}

	async getPostBySlug(getPostBySlugDto: GetPostBySlugDto) {
		try {
			return await this.prismaService.post.findFirstOrThrow({
				where: { slug: getPostBySlugDto.slug },
				include: {
					categories: {
						include: { category: true },
					},
					tags: {
						include: { tag: true },
					},
				},
			});
		} catch (err) {
			throw new NotFoundException('No post with this slug found');
		}
	}

	getAllPosts() {
		return this.prismaService.post.findMany({
			include: {
				categories: {
					include: { category: true },
				},
				tags: {
					include: { tag: true },
				},
			},
		});
	}

	async deletePost(deletePostDto: DeletePostDto, user: User) {
		const post = await this.prismaService.post.findUnique({ where: { id: deletePostDto.id } });

		if (!post) throw new NotFoundException('Post not found');

		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Delete, subject('Post', post));
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		return this.prismaService.post.delete({ where: deletePostDto });
	}
}
