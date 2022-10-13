import { ForbiddenError } from '@casl/ability';
import { ForbiddenException, Injectable, Logger } from '@nestjs/common';
import { User } from '@prisma/client';
import { CaslAbilityFactory, CaslAction } from '../casl/casl-ability.factory';
import { PrismaService } from '../prisma/prisma.service';
import { CreatePostDto } from './dto/create-post.dto';

@Injectable()
export class PostService {
	private logger = new Logger(PostService.name);

	constructor(private prismaService: PrismaService, private caslAbilityFactory: CaslAbilityFactory) {}

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
				...(typeof createPostDto.coverImageFileId === 'number'
					? {
							coverImageFile: {
								connect: { id: createPostDto.coverImageFileId },
							},
					  }
					: {}),
			},
		});

		return post;
	}
}
