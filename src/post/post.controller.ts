import { Body, Controller, Post, UseGuards } from '@nestjs/common';
import { User } from '@prisma/client';
import { GetUser } from '../common/decorators';
import { JwtAuthGuard } from '../common/guards';
import { CreatePostDto } from './dto/create-post.dto';
import { PostService } from './post.service';

@Controller('post')
@UseGuards(JwtAuthGuard)
export class PostController {
	constructor(private readonly postService: PostService) {}

	@Post()
	createPost(@Body() createPostDto: CreatePostDto, @GetUser() user: User) {
		return this.postService.createPost(createPostDto, user);
	}
}
