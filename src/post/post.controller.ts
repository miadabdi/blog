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
import { CreatePostDto } from './dto/create-post.dto';
import { DeletePostDto } from './dto/delete-post.dto';
import { GetPostBySlugDto } from './dto/get-post-by-slug.dto';
import { UpdatePostDto } from './dto/update-post.dto';
import { PostService } from './post.service';

@Controller('post')
export class PostController {
	constructor(private readonly postService: PostService) {}

	@Post()
	@UseGuards(JwtAuthGuard)
	createPost(@Body() createPostDto: CreatePostDto, @GetUser() user: User) {
		return this.postService.createPost(createPostDto, user);
	}

	@Patch()
	@UseGuards(JwtAuthGuard)
	updatePost(@Body() updatePostDto: UpdatePostDto, @GetUser() user: User) {
		return this.postService.updatePost(updatePostDto, user);
	}

	@Get('/by-slug')
	getPostBySlug(@Query() getPostBySlugDto: GetPostBySlugDto) {
		return this.postService.getPostBySlug(getPostBySlugDto);
	}

	@Get()
	getAllPosts() {
		return this.postService.getAllPosts();
	}

	@HttpCode(HttpStatus.NO_CONTENT)
	@Delete()
	@UseGuards(JwtAuthGuard)
	deletePost(@Query() deletePostDto: DeletePostDto, @GetUser() user: User) {
		return this.postService.deletePost(deletePostDto, user);
	}
}
