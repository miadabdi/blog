import { Injectable, Logger } from '@nestjs/common';
import { User } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { CreatePostDto } from './dto/create-post.dto';

@Injectable()
export class PostService {
	private logger = new Logger(PostService.name);

	constructor(private prismaService: PrismaService) {}

	async createPost(createPostDto: CreatePostDto, user: User) {
		const post = await this.prismaService.post.create({
			data: {
				name: createPostDto.name,
				slug: createPostDto.slug,
				bodyObj: createPostDto.bodyObj,
				summary: createPostDto.summary,
				author: {
					connect: { id: user.id },
				},
				coverImageFile: {
					connect: { id: createPostDto.coverImageFileId },
				},
			},
		});

		return post;
	}
}
