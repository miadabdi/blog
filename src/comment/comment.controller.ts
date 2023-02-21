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
import { User } from '@prisma/client';
import { GetUser } from '../common/decorators';
import { JwtAuthGuard } from '../common/guards';
import { CommentService } from './comment.service';
import { GetAllCommentsOfPost } from './dto/get-all-comments-by-post.dto';
import { CreateCommentDto, DeleteCommentDto, UpdateCommentDto } from './dto/index';

@Controller('comment')
export class CommentController {
	constructor(private readonly commentService: CommentService) {}

	@Post()
	@UseGuards(JwtAuthGuard)
	createComment(@Body() createCommentDto: CreateCommentDto, @GetUser() user: User) {
		return this.commentService.createComment(createCommentDto, user);
	}

	@Patch()
	@UseGuards(JwtAuthGuard)
	updateComment(@Body() updateCommentDto: UpdateCommentDto, @GetUser() user: User) {
		return this.commentService.updateComment(updateCommentDto, user);
	}

	@Get()
	getAllComments() {
		return this.commentService.getAllComments();
	}

	@Get('by-post')
	getAllCommentsOfPost(@Query() getAllCommentsOfPost: GetAllCommentsOfPost) {
		return this.commentService.getAllCommentsOfPost(getAllCommentsOfPost);
	}

	@HttpCode(HttpStatus.NO_CONTENT)
	@Delete()
	@UseGuards(JwtAuthGuard)
	deleteComment(@Query() deleteCommentDto: DeleteCommentDto, @GetUser() user: User) {
		return this.commentService.deleteComment(deleteCommentDto, user);
	}
}
