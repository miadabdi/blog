import { ForbiddenError, subject } from '@casl/ability';
import { ForbiddenException, Injectable, Logger, NotFoundException } from '@nestjs/common';
import { User } from '@prisma/client';
import { CaslAbilityFactory, CaslAction } from '../casl/casl-ability.factory';
import { PrismaService } from '../prisma/prisma.service';
import { CreateCommentDto, DeleteCommentDto, UpdateCommentDto } from './dto/index';

@Injectable()
export class CommentService {
	private logger = new Logger(CommentService.name);

	constructor(private prismaService: PrismaService, private caslAbilityFactory: CaslAbilityFactory) {}

	async createComment(createCommentDto: CreateCommentDto, user: User) {
		const ability = this.caslAbilityFactory.createForUser(user);
		try {
			ForbiddenError.from(ability).throwUnlessCan(CaslAction.Create, 'Comment');
		} catch (err: any) {
			throw new ForbiddenException(err.message);
		}

		const comment = await this.prismaService.comment.create({
			data: {
				content: createCommentDto.content,
				author: {
					connect: { id: user.id },
				},
				post: {
					connect: { id: createCommentDto.postId },
				},
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
