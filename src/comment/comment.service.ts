import { ForbiddenError, subject } from '@casl/ability';
import {
	BadRequestException,
	ForbiddenException,
	Inject,
	Injectable,
	Logger,
	NotFoundException,
} from '@nestjs/common';
import { User } from '@prisma/client';
import { CaslAbilityFactory, CaslAction } from '../casl/casl-ability.factory';
import { PRISMA_INJECTION_TOKEN } from '../prisma/prisma.module';
import { PrismaService } from '../prisma/prisma.service';
import { GetAllCommentsOfPost } from './dto/get-all-comments-by-post.dto';
import { CreateCommentDto, DeleteCommentDto, UpdateCommentDto } from './dto/index';

@Injectable()
export class CommentService {
	private logger = new Logger(CommentService.name);

	constructor(
		@Inject(PRISMA_INJECTION_TOKEN) private prismaService: PrismaService,
		private caslAbilityFactory: CaslAbilityFactory,
	) {}

	async createComment(createCommentDto: CreateCommentDto, user: User) {
		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Create, 'Comment');
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		const post = await this.prismaService.post.findUnique({ where: { id: createCommentDto.postId } });
		if (!post) {
			throw new BadRequestException(`Post with id ${createCommentDto.postId} not found`);
		}

		createCommentDto.authorId = user.id;

		const comment = await this.prismaService.comment.create({
			data: {
				content: createCommentDto.content,
				author: {
					connect: { id: user.id },
				},
				post: {
					connect: { id: createCommentDto.postId },
				},
				...(createCommentDto.replyTo
					? {
							parent: {
								connect: { id: createCommentDto.replyTo },
							},
						}
					: {}),
			},
		});

		return comment;
	}

	async updateComment(updateCommentDto: UpdateCommentDto, user: User) {
		const comment = await this.prismaService.comment.findUnique({ where: { id: updateCommentDto.id } });

		if (!comment) throw new NotFoundException('Comment not found');

		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Update, subject('Comment', comment));
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		const updatedComment = await this.prismaService.comment.update({
			where: { id: updateCommentDto.id },
			data: updateCommentDto,
		});

		return updatedComment;
	}

	getAllComments() {
		return this.prismaService.comment.findMany();
	}

	getAllCommentsOfPost(getAllCommentsOfPost: GetAllCommentsOfPost) {
		return this.prismaService.comment.findMany({ where: { postId: getAllCommentsOfPost.postId } });
	}

	async deleteComment(deleteCommentDto: DeleteCommentDto, user: User) {
		const comment = await this.prismaService.comment.findUnique({ where: { id: deleteCommentDto.id } });

		if (!comment) throw new NotFoundException('Comment not found');

		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Delete, subject('Comment', comment));
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		return this.prismaService.comment.delete({ where: deleteCommentDto });
	}
}
