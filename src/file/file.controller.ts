import { Controller, Post, UploadedFile, UseGuards, UseInterceptors } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { JwtAuthGuard } from '../common/guards';
import { SharpPipe } from '../common/pipes/sharp-pipe.pipe';
import { FileService } from './file.service';

@Controller('file')
export class FileController {
	constructor(private fileService: FileService) {}

	@Post('upload-image')
	@UseGuards(JwtAuthGuard)
	@UseInterceptors(FileInterceptor('image'))
	async uploadImage(@UploadedFile(SharpPipe) image: Express.Multer.File) {
		return this.fileService.uploadImage(image);
	}
}
