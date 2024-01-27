import { ForbiddenError, subject } from '@casl/ability';
import { ForbiddenException, Injectable, Logger, NotFoundException } from '@nestjs/common';
import { User } from '@prisma/client';
import { CaslAbilityFactory, CaslAction } from '../casl/casl-ability.factory';
import { PrismaService } from '../prisma/prisma.service';
import { CreatePostDto } from './dto/create-post.dto';
import { DeletePostDto } from './dto/delete-post.dto';
import { GetPostBySlugDto } from './dto/get-post-by-slug.dto';
import { UpdatePostDto } from './dto/update-post.dto';

@Injectable()
export class PostService {
	private logger = new Logger(PostService.name);

	constructor(
		private prismaService: PrismaService,
		private caslAbilityFactory: CaslAbilityFactory,
	) {}

	async createPost(createPostDto: CreatePostDto, user: User) {
		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Create, 'Post');
		} catch (err: any) {
			throw new ForbiddenException(err.message);
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
